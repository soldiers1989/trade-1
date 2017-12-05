/*
*	net - net service module
*/
#pragma once
#include <WinSock2.h>
#include <map>
#include <list>
#include "cc.h"
#include "sa.h"
#include "io.h"

BEGIN_CUBE_NAMESPACE

//iocp operation
typedef enum io_opt { IO_SEND, IO_RECV } io_opt;

//self defined overlapped structure for iocp
typedef struct io_context {
	OVERLAPPED overlapped;
	io_opt opt;
	WSABUF buf;

	io_context(char *data, int sz, bool copydata = true) :  opt(IO_SEND) {
		buf.len = sz;
		if (copydata) {
			buf.buf = new char[sz];
			memcpy(buf.buf, data, sz);
		} else {
			buf.buf = data;
		}
		
		memset(&overlapped, 0, sizeof(overlapped));
	}

	io_context(int sz) : opt(IO_RECV) {
		buf.len = sz;
		buf.buf = new char[sz];
		memset(&overlapped, 0, sizeof(overlapped));
	}

	~io_context() {
		delete[](buf.buf);
		buf.len = 0;
	}
} io_context_t;

//session class
class session {
public:
	//make service can access private member
	friend class service;
	/*
	*	constructor & destructor
	*/
	session() {}
	virtual ~session() {}

	/*
	*	recalled when the connection has build, the @arg is the
	*parameter passed when the accepter started or specified by the
	*connector's connect method.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_open(void *arg);

	/*
	*	recalled when the the data has send out, with send size @sz_send.
	*@param context: in, context of send opertation
	*@param transfered: in, data has transfered
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_send(int sz);

	/*
	*	recalled when the the @data with size @sz_recv has received.
	*@param context: in, context of receive opertation
	*@param transfered: in, data has transfered
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_recv(char *data, int sz);

	/*
	*	recalled when the handler will be destroyed.
	*return:
	*	0--success, other--failed
	*/
	virtual int on_close();

protected:
	/*
	*	open the new session
	*@param s: in, socket of new session
	*@param ip: in, remote ip address of new session
	*@param port: in, remote port of new session
	*@return:
	*	void
	*/
	void open(socket_t s, uint ip, ushort port);

	/*
	*	make an asynchronize iocp send operation with data @buf which size is @sz
	*@param buf: in, data to send
	*@param sz: in, data size in bytes
	*@param error: out, error message when start service failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int send(char *data, int sz, std::string *error = 0);

	/*
	*	make an asynchronize iocp receive operation with size @sz
	*@param sz: in, data size in bytes want to receive
	*@return:
	*	0 for success, otherwise <0
	*/
	int recv(int sz, std::string *error = 0);

	/*
	*	close current session
	*@return:
	*	void
	*/
	void close();

	int on_send();
	int on_recv();

private:
	//socket of session
	socket _socket;

	//pending io context has sent to the completion port
	std::mutex _mutex;
	std::list<io_context*> _contexts;
};

class service : public runnable {
public:
	service() : _iocp(INVALID_HANDLE_VALUE), _stopped(true), _stop(true), _arg(0) {

	}

	virtual ~service() {

	}

	int start(int workers, std::string *error = 0) {
		return start(workers, 0, error);
	}

	/*
	*	start service with specified workers(concurrent threads for io completion port)
	*@param workers: in, concurrent thread number for io completion port, better the same with cpu cores
	*@param error: out, error message when start service failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(int workers, void *arg = 0, std::string *error = 0) {
		std::lock_guard<std::mutex> lock(_mutex);
		if (!_stopped)
			return 0;

		_arg = arg;

		/*create io complete port*/
		_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, 0);
		if (_iocp == NULL) {
			safe_assign<std::string>(error, sa::last_error());
			return -1; //create iocp failed.
		}

		/*start worker threads*/
		_stop = false;
		if (_threads.start(this, workers, error) != 0)
			return -1;
		_stopped = false;

		return 0;
	}

	/*
	*	accept and serve a new incoming session
	*@param s: in, new incoming session
	*@param error: out, error message when serve the new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int dispatch(session *s, std::string *error = 0) {
		std::lock_guard<std::mutex> lock(_mutex);
		//first bind the new session to completion port
		if (CreateIoCompletionPort((HANDLE)s->socket(), _iocp, (ULONG_PTR)s, 0) == NULL) {
			safe_assign<std::string>(error, sa::last_error());
			return -1;
		}

		//notify the session with connection opened event
		if (s->_on_open(_arg) != 0) {
			//notify the session with connection closed event
			s->_on_close();
			return -1;
		}

		//add to sessions
		_sessions.insert(std::pair<SOCKET, session*>(s->socket(), s));

		return 0;
	}

	/*
	*	discard an existing session in the service
	*/
	int discard(session *s) {
		std::lock_guard<std::mutex> lock(_mutex);
		//notify the session with connection closed event
		s->_on_close();
		//remove session from sessions
		_sessions.erase(s->socket());
		//free session object
		delete s;

		return 0;
	}

	//stop iocp service
	int stop() {
		std::lock_guard<std::mutex> lock(_mutex);
		if (_stopped)
			return 0;

		//close all handles refer to the iocp
		std::map<SOCKET, session*>::iterator iter = _sessions.begin(), iterend = _sessions.end();
		while (iter != iterend) {
			iter->second->_on_close();
			delete iter->second;
			iter++;
		}
		_sessions.clear();

		//close the iocp handle
		if (_iocp != INVALID_HANDLE_VALUE) {
			CloseHandle(_iocp);
			_iocp = INVALID_HANDLE_VALUE;
		}

		//stop threads
		_stop = true;
		_threads.join();
		_stopped = true;

		return 0;
	}

public:
	/*
	*	process session
	*/
	void run() {
		//process complete io request until stop
		while (!_stop) {
			iocp_res res = _iocp.pull();
			if (res.error == 0) {
				res.completionkey
				switch (context->_opt) {
				case IO_SEND:
					err = session->on_send(context, transfered);
					break;
				case IO_RECV:
					err = session->on_recv(context, transfered);
					break;
				default:
					err = 0;
					break;
				}
			} else {
				if (res.error == ERROR_ABANDONED_WAIT_0)
					break; // iocp handle closed
			}
		}
	}

private:
	//iocp of service
	iocp _iocp;

	//service worker threads
	threads _threads;
	//stopped flag for service
	bool _stopped;
	//stop flag for thread
	volatile bool _stop;

	//argument for new session
	void *_arg;

	//sessions of service
	std::mutex _mutex;
	std::map<socket_t, session*> _sessions;
};

template<class session_impl>
class server : public runnable {
public:
	server() : _sock(INVALID_SOCKET), _port(0), _stopped(true), _stop(true) {

	}

	virtual ~server() {

	}

	/*
	*	start server with listen port and argument pass to new session
	*@param port: in, listen port
	*@param arg: in, argument pass to new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port, void* arg = NULL) {
		return start(INADDR_ANY, port, arg);
	}

	/*
	*	start server with listen port and argument pass to new session
	@param ip: in, listen ip
	*@param port: in, listen port
	*@param arg: in, argument pass to new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(uint ip, ushort port, void *arg = NULL) {
		/*local bind ip and port for listen*/
		_ip = ip;
		_port = port;

		//start service
		if (_service.start(2, arg) != 0)
			return -1; //start service faild

		//start listen on socket
		_sock = socket::listen(ip, port);
		if (_sock == INVALID_SOCKET)
			return -1; //listen failed

		//start accept thread
		_stop = false;
		if (_thread.start(this) != 0)
			return -1;
		_stopped = false;

		return 0;
	}

	/*stop accepter*/
	int stop() {
		if (_stopped)
			return 0;
		//close listen socket
		closesocket(_sock);
		_sock = INVALID_SOCKET;

		//stop accept thread
		_stop = true;
		_thread.join();
		_stopped = true;

		//stop service
		_service.stop();

		return 0;
	}

public:
	/*
	*	accept new connections
	*/
	void run() {
		//new connect socket information
		struct sockaddr_in remote;
		int addr_len = sizeof(remote);
		memset(&remote, 0, addr_len);

		//accept new socket
		while (!_stop) {
			SOCKET s = WSAAccept(_sock, (struct sockaddr*)&remote, &addr_len, 0, 0);
			if (s != INVALID_SOCKET) {
				session *ns = new session_impl(s, ntohl(remote.sin_addr.s_addr), ntohs(remote.sin_port));
				_service.dispatch(ns);
			} else {
				int err = WSAGetLastError();
				if (err == WSAEWOULDBLOCK)
					::Sleep(1000);
				else
					throw std::exception(sys::geterrormsg(err).c_str());
			}
		}
	}

private:
	//listen socket
	SOCKET _sock;
	//local ip
	uint _ip;
	//listen port
	ushort _port;

	//accept thread
	bool _stopped;
	volatile bool _stop;
	thread _thread;

	//service for server
	service _service;
};

template<class session_impl>
class client {
public:
	client() {

	}

	virtual ~client() {

	}

	int start(void *arg = 0) {
		//start worker service
		_service.start(arg);

		return 0;
	}

	int connect(uint ip, ushort port) {
		//connect to remote service
		SOCKET sock = socket::connect(ip, port);
		if (sock == INVALID_SOCKET)
			return -1;

		/*add to worker service*/
		session *ns = new session_impl(sock, ip, port);
		_service.dispatch(ns);

		return 0;
	}

	/*stop accepter*/
	int stop() {
		//stop worker service
		_service.stop();
		return 0;
	}

private:
	//service for client
	service _service;
};

class netinit {
public:
	netinit() {
		/*start up windows socket environment*/
		WORD wsaversion;
		WSADATA wsadata;
		wsaversion = MAKEWORD(2, 2);

		int err = WSAStartup(wsaversion, &wsadata);
		if (err != 0) { //startup windows socket environment failed.
			throw sa::last_exception();
		}
	}

	virtual ~netinit() {
		/*clean the windows socket environment*/
		WSACleanup();
	}
};

//for initialize the windows socket environment
static netinit _g_netsvc_init;

END_CUBE_NAMESPACE
