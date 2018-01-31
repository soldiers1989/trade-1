/*
*	svr - server module, including udp/tcp/http servers
*/
#pragma once
#include "net.h"
#include "http.h"
BEGIN_CUBE_NAMESPACE
BEGIN_TCP_NAMESPACE
//tcp server class
template<class sessionimpl>
class server : public task {
public:
	server() {}
	virtual ~server() {}

	/*
	*	start server with listen port and argument pass to new session
	*@param port: in, listen port
	*@param workers: in, worker thread number for session 
	*@param arg: in, argument pass to new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port, void* arg = 0) {
		return start(INADDR_ANY, port, arg);
	}

	int start(ushort port, int workers, void* arg = 0) {
		return start(INADDR_ANY, port, workers,  arg);
	}

	/*
	*	start server with listen port and argument pass to new session
	@param ip: in, listen ip
	*@param port: in, listen port
	*@param workers: in, worker thread number for session
	*@param arg: in, argument pass to new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ulong ip, ushort port, void *arg = 0) {
		return start(ip, port, 0, arg);
	}

	int start(ulong ip, ushort port, int workers, void *arg = 0) {
		//step1: start iocp service
		if (workers > 0) {
			if (_service.start(arg, workers) != 0)
				return -1;
		} else {
			if (_service.start(arg) != 0)
				return -1;
		}
		

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
			net::session *s = new sessionimpl();

			//dispatch new session to iocp service
			_service.dispatch(sock, s);

		} catch (const socket::ewouldblock&) {}
	}

private:
	//listen socket
	socket _socket;

	//thread looper
	looper _looper;

	//service for server
	net::service _service;
};
END_TCP_NAMESPACE

BEGIN_HTTP_NAMESPACE
//http servlet class
class servlet {
public:
	servlet() {}
	virtual ~servlet() {}

	/*
	*	handle http request
	*@param req: in, client request
	*@param resp: in/out, service response
	*@return:
	*	void
	*/
	virtual void handle(const request &req, response &resp) = 0;
};

//http applet class
class applet {
public:
	app() {}
	virtual ~app() {}

	/*
	*	handle request, set response with process result
	*@param req: in, request object
	*@param resp: in/out, response object
	*@return:
	*	void
	*/
	void handle(const request &req, response &resp);

	/*
	*	mount path with relate servlet
	*@param path: in, servlet relate path
	*@param servlet: in, servlet for path
	*@return:
	*	void
	*/
	void mount(const std::string &method, const std::string &path, servlet *servlet);

private:
	//registered servlets, <method, <path, servlet>>
	std::map<std::string, std::map<std::string, std::shared_ptr<servlet>>> _servlets;
};

//http session class
class session : public net::session {
	//session send & recv buffer size
	static const int BUFSZ = 4096;
public:
	session() : _applet(0) {}
	virtual ~session() {}

	int on_open(void *arg);
	int on_send(int transfered);
	int on_recv(char *data, int transfered);
	void on_close();

private:
	//relate applet
	applet *_applet;

	//session request stream
	rqstream _req;
	//session response stream
	rpstream _resp;
};

//http server class
class server {
public:
	server() {}
	virtual ~server() {}

	/*
	*	start http server on specified port
	*@param port: in, local http service port
	*@param workers: in, workers for http session
	*@param servlets: in, servlets for processing request
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port, int workers, applet *applet);

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
END_CUBE_NAMESPACE
