/*
*	net - net service module
*/
#pragma once
#include <map>
#include <list>
#include "cc.h"
#include "sa.h"
#include "io.h"
#include "os.h"

BEGIN_CUBE_NAMESPACE
//iocp operation
typedef enum io_opt { IO_SEND, IO_RECV } io_opt;

//iocp session context with overlapped structure class
class ioctxt {
public:
	OVERLAPPED overlapped;
	void  *ptr;
	io_opt opt;
	WSABUF buf;

public:
	ioctxt(char *data, int sz, bool copydata = true) : ioctxt(0, data, sz, copydata){}
	ioctxt(void *ptr, char *data, int sz, bool copydata = true) :  opt(IO_SEND) {
		ptr = ptr;
		buf.len = sz;
		if (copydata) {
			buf.buf = new char[sz];
			memcpy(buf.buf, data, sz);
		} else {
			buf.buf = data;
		}
		
		memset(&overlapped, 0, sizeof(overlapped));
	}

	ioctxt(int sz) : ioctxt(0, sz) {}
	ioctxt(int sz, void *ptr) : opt(IO_RECV) {
		ptr = ptr;
		buf.len = sz;
		buf.buf = new char[sz];
		memset(&overlapped, 0, sizeof(overlapped));
	}

	~ioctxt() {
		delete[](buf.buf);
		buf.len = 0;
	}
};

//iocp service session class
class session {
public:
	//make service can access private member
	friend class service;
	/*
	*	constructor & destructor
	*/
	session() {}
	virtual ~session() {
		free();
	}

	/*
	*	recalled when the connection has build, the @arg is the
	*parameter passed when the accepter started or specified by the
	*connector's connect method.
	*return:
	*	0--success, other--failed, session will be destroyed
	*/
	virtual int on_open(void *arg);

	/*
	*	recalled when the the data has been sent
	*@param transfered: in, data has transfered
	*return:
	*	0--success, other--failed, session will be destroyed
	*/
	virtual int on_send(int transfered);

	/*
	*	recalled when the has been received.
	*@param data: in, pointer to received data
	*@param transfered: in, data has transfered
	*return:
	*	0--success, other--failed, session will be destroyed
	*/
	virtual int on_recv(char *data, int transfered);

	/*
	*	recalled when the handler will be destroyed.
	*return:
	*	always 0
	*/
	virtual int on_close();

protected:
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

private:
	/*
	*	open the new session
	*@param s: in, socket of new session
	*@return:
	*	void
	*/
	void open(socket s);


	/*
	*	close current session
	*@return:
	*	void
	*/
	void close();

	/*
	*	free uncompleted io's relate context
	*/
	void free();

private:
	/*
	*	recall for iocp service when there is a completion send event
	*@param context: in, context of the event
	*@param transfered: in, data transfered in bytes
	*@return:
	*	0--success, other--failed, session will be destroyed
	*/
	int on_send(ioctxt *context, int transfered);

	/*
	*	recall for iocp service when there is a completion recv event
	*@param context: in, context of the event
	*@param transfered: in, data transfered in bytes
	*@return:
	*	0--success, other--failed, session will be destroyed
	*/
	int on_recv(ioctxt *context, int transfered);

public:
	/*
	*	 get the socket handle
	*/
	socket_t handle();

private:
	//socket of session
	socket _socket;

	//pending io context has sent to the completion port
	std::mutex _mutex;
	std::list<ioctxt*> _contexts;
};

//iocp service class
class service : public runnable {
	//service exceptions
	typedef std::exception ewarn;
	typedef std::exception efatal;

public:
	service() : _stopped(true), _stop(true), _arg(0) {

	}

	virtual ~service() {
		free();
	}


	/*
	*	start iocp service
	*@param workers: in, concurrent thread number for io completion port, better the same with cpu cores
	*@param arg: in, argument pass to session with @on_open recall
	*@return:
	*	0 for success, otherwise throw exceptions
	*/
	int start(int workers = os::get_cpu_cores());
	int start(void *arg, int workers = os::get_cpu_cores());

	/*
	*	dispatch a new session to iocp service
	*@param sock: in, new socket
	*@param s: in, new session for the socket
	*@return:
	*	0 for success, otherwise <0
	*/
	int dispatch(session *s);
	int dispatch(socket sock, session *s);

	/*
	*	discard an existing session in the service
	*@param s: in, sessionto discard
	*@return:
	*	always 0
	*/
	int discard(socket_t s);
	int discard(session *s);

	/*
	*	stop iocp service
	*@return:
	*	always 0
	*/
	int stop();

public:
	/*
	*	worker to do the queued complete events
	*/
	virtual void run();

private:
	/*
	*	free sessions
	*/
	void free();

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

//tcp server class
template<class sessionimpl>
class server : public runnable {
public:
	server() : _stopped(true), _stop(true) {}
	virtual ~server() {}

	/*
	*	start server with listen port and argument pass to new session
	*@param port: in, listen port
	*@param arg: in, argument pass to new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port, void* arg = 0) {
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
	int start(uint ip, ushort port, void *arg = 0) {
		//step1: start iocp service
		if (_service.start(arg) != 0)
			return -1;

		//step2: start listen on the port
		_socket = socket::listen(ip, port, socket::mode::OVERLAPPED | socket::mode::REUSEADDR);

		//step3: start accept thread
		_stop = false;
		if (_thread.start(this) != 0)
			return -1;
		_stopped = false;

		return 0;
	}

	/*
	*	stop server
	*@return:

	*/
	int stop() {
		//step1: close listen socket
		closesocket(_sock);
		_sock = INVALID_SOCKET;

		//step2: stop accept thread
		_stop = true;
		_thread.join();
		_stopped = true;

		//step3: stop iocp service
		_service.stop();

		return 0;
	}

public:
	/*
	*	accept new connections
	*/
	void run() {
		while (!_stop) {
			try {
				//wait for new connection
				socket sock = _socket.accept(50, 0);

				//create new session for connection
				session *s = new sessionimpl();

				//dispatch new session to iocp service
				_service.dispatch(sock, s);

			} catch (const socket::ewouldblock& ) {}
		}
	}
private:
	//listen socket
	socket _socket;

	//accept thread
	bool _stopped;
	volatile bool _stop;
	thread _thread;

	//service for server
	service _service;
};

//tcp client class
template<class sessionimpl>
class client {
public:
	client() {}

	virtual ~client() {}

	int start(void *arg = 0) {
		//start iocp service
		_service.start(arg);

		return 0;
	}

	int connect(uint ip, ushort port) {
		try {
			//connect to remote service
			socket sock = socket::connect(ip, port);

			//create new session for connection
			session *s = new sessionimpl();

			//dispatch new session to iocp service
			_service.dispatch(sock, s);

		} catch (const socket::ewouldblock &e) {
		}

		return 0;
	}

	/*stop accepter*/
	int stop() {
		//stop iocp service
		_service.stop();

		return 0;
	}

private:
	//service for client
	service _service;
};

//class for initialize windows socket everiment
class netinit {
public:
	netinit() {
		/*start up windows socket environment*/
		WORD wsaversion;
		WSADATA wsadata;
		wsaversion = MAKEWORD(2, 2);

		int err = WSAStartup(wsaversion, &wsadata);
		if (err != 0) { //startup windows socket environment failed.
			throw std::exception(sa::last_error().c_str());
		}
	}

	virtual ~netinit() {
		/*clean the windows socket environment*/
		WSACleanup();
	}
};

END_CUBE_NAMESPACE
