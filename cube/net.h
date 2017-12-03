#pragma once
#include <WinSock2.h>
#include <map>
#include <list>
#include "cc.h"

BEGIN_CUBE_NAMESPACE

//iocp operation
typedef enum io_opt{ IO_SEND, IO_RECV } io_opt;

//self defined overlapped structure for iocp
typedef struct io_context
{
	OVERLAPPED _overlapped;
	SOCKET _sock;
	io_opt _opt;
	WSABUF _buf;

	io_context(SOCKET sock, const char *data, int send_sz) : _sock(sock), _opt(IO_SEND)
	{
		_buf.len = send_sz;
		_buf.buf = new char[send_sz];
		memcpy(_buf.buf, data, send_sz);
		memset(&_overlapped, 0, sizeof(_overlapped));
	}

	io_context(SOCKET sock, int recv_sz) : _sock(sock), _opt(IO_RECV)
	{
		_buf.len = recv_sz;
		_buf.buf = new char[recv_sz];
		memset(&_overlapped, 0, sizeof(_overlapped));
	}

	~io_context()
	{
		delete[](_buf.buf);
		_buf.len = 0;
	}
} io_context;

class socket
{
public:
	static int set_reuseaddr(SOCKET s);
	static int set_nonblock(SOCKET s);
	static int bind(SOCKET s, uint ip, ushort port);
	static SOCKET listen(uint ip, ushort port, bool nonblk = true);
	static SOCKET connect(uint ip, ushort port, bool nonblk = true);
};

//session class
class session
{
public:
	//make service can access private member
	friend class service;
	/*
	*	constructor & destructor
	*/
	session(SOCKET s, uint ip, uint port);
	virtual ~session();

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
	virtual int on_send(io_context *context, uint transfered);

	/*
	*	recalled when the the @data with size @sz_recv has received.
	*@param context: in, context of receive opertation
	*@param transfered: in, data has transfered
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_recv(io_context *context, uint transfered);

	/*
	*	recalled when the handler will be destroyed.
	*return:
	*	0--success, other--failed
	*/
	virtual int on_close();

public:
	//session address information
	SOCKET socket() { return _socket; }
	uint ip() {	return _ip;	}
	ushort port() {	return _port; }

protected:
	/*
	*	make an asynchronize iocp send operation with data @buf which size is @sz
	*@param buf: in, data to send
	*@param sz: in, data size in bytes
	*@param error: out, error message when start service failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int send(io_context *context, std::string *error = 0);

	/*
	*	make an asynchronize iocp receive operation with size @sz
	*@param sz: in, data size in bytes want to receive
	*@return:
	*	0 for success, otherwise <0
	*/
	int recv(io_context *context, std::string *error = 0);

private:
	/*
	*	open the new session
	*@param s: in, socket of new session
	*@param ip: in, remote ip address of new session
	*@param port: in, remote port of new session
	*@return:
	*	void
	*/
	void _open(SOCKET s, uint ip, ushort port);

	/*
	*	close current session
	*@return:
	*	void
	*/
	void _close();

	/*
	*	notify session closed
	*/
	int _on_open(void *arg);

	/*
	*	recalled when the the data has send out, with send size @sz_send.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	int _on_send(io_context *context, uint transfered);

	/*
	*	recalled when the the @data with size @sz_recv has received.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	int _on_recv(io_context *context, uint transfered);

	/*
	*	notify session closed
	*/
	int _on_close();

private:
	//socket of the relate handler
	SOCKET _socket;
	//remote peer ip
	unsigned int _ip;
	//remote peer port
	unsigned short _port;

	//pending io context has sent to the completion port
	std::mutex _mutex;
	std::list<io_context*> _contexts;
};

class service : public runnable
{
public:
	service() : _iocp(INVALID_HANDLE_VALUE), _stopped(true), _stop(true)
	{

	}

	virtual ~service()
	{

	}

	/*
	*	start service with specified workers(concurrent threads for io completion port)
	*@param workers: in, concurrent thread number for io completion port, better the same with cpu cores
	*@param error: out, error message when start service failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(int workers = 0, std::string *error = 0)
	{
		std::lock_guard<std::mutex> lock(_mutex);
		if (!_stopped)
			return 0;

		/*create io complete port*/
		_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, 0);
		if (_iocp == NULL)
		{
			safe_assign<std::string>(error, sys::getlasterror());
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
	int dispatch(session *s, std::string *error = 0)
	{
		std::lock_guard<std::mutex> lock(_mutex);
		//first bind the new session to completion port
		if (CreateIoCompletionPort((HANDLE)s->socket(), _iocp, (ULONG_PTR)s, 0) == NULL)
		{
			safe_assign<std::string>(error, sys::getlasterror());
			return -1;
		}

		//notify the session with connection opened event
		if (s->_on_open(0) != 0)
		{
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
	int discard(session *s)
	{
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
	int stop()
	{
		std::lock_guard<std::mutex> lock(_mutex);
		if (_stopped)
			return 0;

		//close all handles refer to the iocp
		std::map<SOCKET, session*>::iterator iter = _sessions.begin(), iterend = _sessions.end();
		while (iter != iterend)
		{
			iter->second->_on_close();
			delete iter->second;
			iter++;
		}
		_sessions.clear();

		//close the iocp handle
		if (_iocp != INVALID_HANDLE_VALUE)
		{
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
	void run()
	{
		session *session = NULL; // session 
		DWORD transfered = 0; // data transfered
		io_context *context = NULL; // overlapped object

		//process complete io request until stop
		while (!_stop)
		{
			if (GetQueuedCompletionStatus(_iocp, &transfered, (PULONG_PTR)&session, (LPOVERLAPPED*)&context, 0))
			{
				if (transfered == 0)
					discard(session); //socket closed
				else
				{
					int err = 0;
					switch (context->_opt)
					{
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

					if (err != 0)
						discard(session); //something wrong with process io
				}
			}
			else
			{
				int err = WSAGetLastError();
				if (err != WSA_WAIT_TIMEOUT)
					discard(session); // session closed
			}
		}
	}

private:
	//iocp handler
	HANDLE _iocp;
	//service worker threads
	threads _threads;
	//stopped flag for service
	bool _stopped;
	//stop flag for thread
	volatile bool _stop;

	//sessions of service
	std::mutex _mutex;
	std::map<SOCKET, session*> _sessions;
};

template<class session_impl>
class server : public runnable
{
public:
	server() : _sock(INVALID_SOCKET), _port(0), _stopped(true), _stop(true)
	{

	}

	virtual ~server()
	{

	}

	/*
	*	start server with listen port and argument pass to new session
	*@param port: in, listen port
	*@param arg: in, argument pass to new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port, void* arg = NULL)
	{
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
	int start(uint ip, ushort port, void *arg = NULL)
	{
		/*local bind ip and port for listen*/
		_ip = ip;
		_port = port;
		_arg = arg;

		//start service
		if (_service.start() != 0)
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
	int stop()
	{
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
	void run()
	{
		//new connect socket information
		struct sockaddr_in remote;
		int addr_len = sizeof(remote);
		memset(&remote, 0, addr_len);

		//accept new socket
		while (!_stop)
		{
			SOCKET s = WSAAccept(_sock, (struct sockaddr*)&remote, &addr_len, 0, 0);
			if (s != INVALID_SOCKET)
			{
				session *ns = new session_impl(s, ntohl(remote.sin_addr.s_addr), ntohs(remote.sin_port);
				_service.dispatch(ns);
			}
			else
			{
				int err = WSAGetLastError();
				if(err != WSA_WAIT_TIMEOUT)
					break;	//something wrong with listen socket
			}
		}
	}

private:
	//listen socket
	SOCKET _sock;
	//listen port
	ushort _port;

	//accept thread
	bool _stopped;
	volatile bool _stop;
	thread _thread;

	//service for server
	service<session_impl> _service;
};

template<class session_impl>
class client
{
public:
	client()
	{

	}

	virtual ~client()
	{

	}

	int start()
	{
		//start worker service
		_service.start();

		return 0;
	}

	int connect(uint ip, ushort port)
	{
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
	int stop()
	{
		//stop worker service
		_service.stop();
		return 0;
	}

private:
	//service for client
	service<session_impl> _service;
};
END_CUBE_NAMESPACE
