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
#include "http.h"

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
	ioctxt(const char *data, int sz) : ioctxt(0, data, sz){}
	ioctxt(void *ptr, const char *data, int sz) :  opt(IO_SEND) {
		ptr = ptr;
		buf.len = sz;
		buf.buf = new char[sz];
		memcpy(buf.buf, data, sz);
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
	int send(const char *data, int sz, std::string *error = 0);

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

	/*
	*	get peer name: ip:port
	*/
	std::string name();

	/*
	*	get remote peer socket
	*/
	const socket& peer();
private:
	//socket of session
	socket _socket;

	//pending io context has sent to the completion port
	std::mutex _mutex;
	std::list<ioctxt*> _contexts;
};

//iocp service class
class service : public task {
	//service exceptions
	typedef std::exception ewarn;
	typedef std::exception efatal;

public:
	service() : _arg(0) {

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
	void run();

private:
	/*
	*	free sessions
	*/
	void free();

private:
	//iocp of service
	iocp _iocp;

	//loopers of service
	loopers _loopers;
	
	//argument for new session
	void *_arg;

	//sessions of service
	std::mutex _mutex;
	std::map<socket_t, session*> _sessions;
};

BEGIN_TCP_NAMESPACE
//tcp server class
template<class sessionimpl>
class server : public task {
public:
	server(){}
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
	int start(ulong ip, ushort port, void *arg = 0) {
		//step1: start iocp service
		if (_service.start(arg) != 0)
			return -1;

		//step2: start listen on the port
		_socket = socket::listen(ip, port, socket::mode::OVERLAPPED | socket::mode::REUSEADDR);

		//step3: start accept looper thread
		_looper.start(this);

		return 0;
	}

	/*
	*	stop server
	*@return:

	*/
	int stop() {
		//step1: close listen socket
		_socket.close();

		//step2: stop accept looper thread
		_looper.stop();

		//step3: stop iocp service
		_service.stop();

		return 0;
	}

public:
	/*
	*	accept new connections
	*/
	void run() {
		try {
			//wait for new connection
			socket sock = _socket.accept(50, 0);

			//create new session for connection
			session *s = new sessionimpl();

			//dispatch new session to iocp service
			_service.dispatch(sock, s);

		} catch (const socket::ewouldblock& ) {}
	}

private:
	//listen socket
	socket _socket;

	//thread looper
	looper _looper;

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

	int connect(ulong ip, ushort port) {
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
END_TCP_NAMESPACE

BEGIN_HTTP_NAMESPACE
//http servlet class
class servlet {
public:
	servlet() {}
	virtual ~servlet() {}

	/*
	*	handle http get request
	*@param req: in, client request
	*@param resp: in/out, service response
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int handle_get(request &req, response &resp) {
		return -1;
	}

	/*
	*	handle http post request
	*@param req: in, client request
	*@param resp: in/out, service response
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int handle_post(request &req, response &resp) {
		return -1;
	}
};

//http servlets class
class servlets {
public:
	servlets() {}
	virtual ~servlets() {}

	/*
	*	mount path with relate servlet
	*@param path: in, servlet relate path
	*@param servlet: in, servlet for path
	*@return:
	*	void
	*/
	void mount(const std::string &path, servlet *servlet);

	/*
	*	handle request, set response with process result
	*@param req: in, request object
	*@param resp: in/out, response object
	*@return:
	*	0 for success, otherwise <0 means interval error
	*/
	int handle(request &req, response &resp);

private:
	//registered servlets
	std::map<std::string, std::shared_ptr<servlet>> _servlets;
};

//http session class
class session : public cube::session {
	const int BUFSZ = 4096;
public:
	session() : _servlets(0) {}
	virtual ~session() {}

	int on_open(void *arg);
	int on_send(int transfered);
	int on_recv(char *data, int transfered);
	int on_close();

private:
	//relate servlets
	servlets *_servlets;

	//session request
	request _request;
	//session response
	response _response;
};

//http server class
class server {
public:
	server() {}
	virtual ~server() {}

	/*
	*	start http server on specified port
	*@param port: in, local http service port
	*@param servlets: in, servlets for processing request
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port, servlets *servlets);

	/*
	*	stop http server
	*@return:
	*	void
	*/
	void stop();
	
private:
	//http server
	tcp::server<session> _server;
};

END_HTTP_NAMESPACE

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
