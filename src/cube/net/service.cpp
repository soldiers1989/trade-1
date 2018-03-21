#include "cube\sys\error.h"
#include "cube\net\service.h"
BEGIN_CUBE_NET_NS
///////////////////////////////////////////////////////////service class//////////////////////////////////////////////////////////////
int service::start(int workers) {
	return start(0, workers);
}

int service::start(void *arg, int workers) {
	//argument pass to new session
	_arg = arg;

	//start worker threads
	_loopers.start(this, workers);

	return 0;
}

int service::dispatch(socket sock, session *s) {
	std::lock_guard<std::mutex> lock(_mutex);
	//bind session with the socket
	s->open(sock);

	//first bind the new session to completion port
	_iocp.bind((HANDLE)s->handle(), (ULONG_PTR)s);

	//notify the session with connection opened event
	if (s->on_open(_arg) != 0) {
		//notify the session with connection closed event
		s->on_close();

		//free session object
		delete s;
	}

	//add to sessions
	_sessions.insert(std::pair<socket_t, session*>(s->handle(), s));

	return 0;
}

int service::dispatch(session *s) {
	std::lock_guard<std::mutex> lock(_mutex);
	//first bind the new session to completion port
	_iocp.bind((HANDLE)s->handle(), (ULONG_PTR)s);

	//notify the session with connection opened event
	if (s->on_open(_arg) != 0) {
		//notify the session with connection closed event
		s->on_close();

		//close socket
		s->close();

		//free session object
		delete s;
	}

	//add to sessions
	_sessions.insert(std::pair<socket_t, session*>(s->handle(), s));

	return 0;
}

int service::discard(socket_t s) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<socket_t, session*>::iterator iter = _sessions.find(s);
	if (iter != _sessions.end()) {
		//remove session from service
		session *s = iter->second;
		_sessions.erase(iter);

		//notify session close
		s->on_close();

		//close socket
		s->close();

		//free session
		delete s;
	}

	return 0;
}

int service::discard(session *s) {
	std::lock_guard<std::mutex> lock(_mutex);
	//notify the session with connection closed event
	s->on_close();

	//close socket
	s->close();

	//remove session from sessions
	_sessions.erase(s->handle());

	//free session object
	delete s;

	return 0;
}

//stop iocp service
int service::stop() {
	//close all sessions
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<SOCKET, session*>::iterator iter = _sessions.begin(), iterend = _sessions.end();
	while (iter != iterend) {
		session *s = iter->second;
		//close session socket, so it can unbind from iocp port
		s->close();

		//notify session the close event
		s->on_close();

		//process next session
		iter++;
	}
	_sessions.clear();

	//close iocp
	_iocp.close();

	//stop loopers
	_loopers.stop();

	return 0;
}

void service::free() {
	// free all sessions
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<SOCKET, session*>::iterator iter = _sessions.begin(), iterend = _sessions.end();
	while (iter != iterend) {
		delete iter->second;
	}
	_sessions.clear();
}

void service::run() {
	//process complete io request until stop
	iores res = _iocp.pull(50);
	if (res.error == 0) {
		//get sepcial data from completion data
		session *s = (session*)res.completionkey;
		ioctxt *context = (ioctxt*)res.overlapped;

		//notify session with completed events
		int err = 0;
		switch (context->opt) {
		case IO_SEND:
			err = s->on_send(context, res.transfered);
			break;
		case IO_RECV:
			err = s->on_recv(context, res.transfered);
			break;
		default:
			err = 0;
			break;
		}

		//process error recall result
		if (err != 0) {
			//discard session from service
			discard(s);
		}
	} else {
		if (res.error == ERROR_ABANDONED_WAIT_0)
			; // iocp handle closed
		else {
			if (res.error != WAIT_TIMEOUT) {
				//fatal error with iocp
				throw efatal(sys::last_error(res.error).c_str());
			}
		}
	}
}
END_CUBE_NET_NS
