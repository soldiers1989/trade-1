#include "net.h"

BEGIN_CUBE_NAMESPACE
BEGIN_NET_NAMESPACE
//for initialize the windows socket environment
static const netinit _g_netsvc_init;

///////////////////////////////////////////////////////////session class//////////////////////////////////////////////////////////////
int session::on_open(void *arg) {
	return -1;
}

int session::on_send(int transfered) {
	return -1;
}

int session::on_recv(char *data, int transfered) {
	return -1;
}

int session::on_timer(int id) {
	return -1;
}

void session::on_close() {
}

void session::open(socket s) {
	_socket = s;
}

int session::send(const char *data, int sz, std::string *error/* = 0*/) {
	//create a new context object
	ioctxt *context = new ioctxt(this, data, sz);

	//post a send data request
	int err = _socket.send(&context->buf, &context->overlapped, error);
	if (err != 0) {
		delete context;
		return -1;
	}

	//add to pending context list
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.push_back(context);

	return 0;
}

int session::recv(int sz, std::string *error/* = 0*/) {
	//create a new context object
	ioctxt *context = new ioctxt(sz, this);

	//post a receive data request
	int err = _socket.recv(&context->buf, &context->overlapped, error);
	if (err != 0) {
		delete context;
		return -1;
	}

	//add to pending context list
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.push_back(context);

	return 0;
}

void session::close() {
	_socket.close();
}

void session::free() {
	std::lock_guard<std::mutex> lock(_mutex);
	std::list<ioctxt*>::iterator iter = _contexts.begin(), iterend = _contexts.end();
	while (iter != iterend) {
		delete *iter;
		iter++;
	}
	_contexts.clear();
}

int session::on_send(ioctxt *context, int transfered) {
	//notify data has been sent event
	int err = on_send(transfered);

	//remove completed context
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.remove(context);

	//free context object
	delete context;

	//return error flag
	return err;
}

int session::on_recv(ioctxt *context, int transfered) {
	//notify data has been sent event
	int err = on_recv(context->buf.buf, transfered);

	//remove completed context
	std::lock_guard<std::mutex> lock(_mutex);
	_contexts.remove(context);

	//free context object
	delete context;

	//return error flag
	return err;
}

socket_t session::handle() {
	return _socket.handle();
}

std::string session::name() {
	return _socket.peeraddr().name();
}

const socket& session::peer() {
	return _socket;
}

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
				throw efatal(os::last_error(res.error).c_str());
			}
		}
	}
}
END_NET_NAMESPACE
END_CUBE_NAMESPACE
