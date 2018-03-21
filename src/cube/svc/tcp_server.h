#pragma once
#include "cube\type.h"
#include "cube\cc\looper.h"
#include "cube\net\socket.h"
#include "cube\net\service.h"
BEGIN_CUBE_SVC_NS
////////////////////////////////////////////////////tcp server//////////////////////////////////////////////
//tcp server class
template<class sessionimpl>
class tcp_server : public cc::task {
public:
	tcp_server() {}
	virtual ~tcp_server() {}

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
		return start(INADDR_ANY, port, workers, arg);
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
		_socket = net::socket::listen(ip, port, net::socket::mode::OVERLAPPED | net::socket::mode::REUSEADDR);

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
			net::socket sock = _socket.accept(50, 0);

			//create new session for connection
			net::session *s = new sessionimpl();

			//dispatch new session to iocp service
			_service.dispatch(sock, s);

		} catch (const net::socket::ewouldblock&) {}
	}

private:
	//listen socket
	net::socket _socket;

	//thread looper
	cc::looper _looper;

	//service for server
	net::service _service;
};
END_CUBE_SVC_NS

