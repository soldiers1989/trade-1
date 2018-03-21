#pragma once
#include "cube\type.h"
#include "cube\net\service.h"
BEGIN_CUBE_SVC_NS
//tcp client class
template<class sessionimpl>
class tcp_client {
public:
	tcp_client() {}
	virtual ~tcp_client() {}

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
			net::session *s = new sessionimpl();

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
	net::service _service;
};
END_CUBE_SVC_NS
