#pragma once
#include <map>
#include "cube\cc\looper.h"
#include "cube\sys\cpu.h"
#include "cube\net\iocp.h"
#include "cube\net\session.h"
BEGIN_CUBE_NET_NS
//iocp service class
class service : public cc::task {
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
	int start(int workers = sys::get_cpu_cores());
	int start(void *arg, int workers = sys::get_cpu_cores());

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
	cc::loopers _loopers;

	//argument for new session
	void *_arg;

	//sessions of service
	std::mutex _mutex;
	std::map<socket_t, session*> _sessions;
};
END_CUBE_NET_NS
