#include "cube\log\log.h"
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
	_workers.start(workers, this);

	//start looper thread
	_looper.start(this);

	//setup tick trigger
	_tick_time_interval = 1; // tick every 1s
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

		//close session socket
		s->close();

		//free session object
		delete s;
	}

	//add to sessions
	_sessions.insert(std::pair<socket_t, session*>(s->handle(), s));

	return 0;
}

//stop iocp service
int service::stop() {
	//close all sessions
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<socket_t, session*>::iterator iter = _sessions.begin(), iterend = _sessions.end();
	while (iter != iterend) {
		session *s = iter->second;
		//notify session the close event
		s->on_close();

		//close session socket, so it can unbind from iocp port
		s->close();

		//process next session
		iter++;
	}
	_sessions.clear();

	//close iocp
	_iocp.close();

	//stop looper
	_looper.stop();

	//stop workers
	_workers.stop();

	return 0;
}

int service::discard(session *s) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<socket_t, session*>::iterator iter = _sessions.find(s->handle());
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

void service::tick() {
	std::lock_guard<std::mutex> lock(_mutex);
	//tick all session
	::time_t now = ::time(0);
	std::map<socket_t, session*>::iterator iter = _sessions.begin(), iterend = _sessions.end();
	while (iter != iterend) {
		session *s = iter->second;
		if (s->on_tick(now) != 0) {
			//remove from session map
			_sessions.erase(iter++);

			//notify session close
			s->on_close();

			//close socket
			s->close();

			//free session !NOTE: free in worker ioloop!
			//delete s;
		} else {
			iter++;
		}
	}
}

void service::free() {
	// free all sessions
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<socket_t, session*>::iterator iter = _sessions.begin(), iterend = _sessions.end();
	while (iter != iterend) {
		delete iter->second;
	}
	_sessions.clear();
}

void service::run() {
	//wait for tick timeout
	std::this_thread::sleep_for(std::chrono::seconds(_tick_time_interval));
	//tick all session
	tick();
}

void service::ioloop() {
	//process complete io request until stop
	iores res = _iocp.pull(1000);

	//current completed io session
	session *s = (session *)res.completionkey;

	//process current io completed session
	if (res.error == 0) {
		//get sepcial data from completion data
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
		if (res.error == ERROR_ABANDONED_WAIT_0) {
			// iocp handle closed
			log::error("iocp: iocp handle closed, errno %d", res.error);
		} else {
			if (res.error != WAIT_TIMEOUT) {
				//free session object
				delete s;

				log::error("iocp: other error with errno %d", res.error);
			}
		}
	}
}
END_CUBE_NET_NS
