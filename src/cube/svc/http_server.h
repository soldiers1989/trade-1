#pragma once
#include "cube\type.h"
#include "cube\http\applet.h"
#include "cube\svc\tcp_server.h"
BEGIN_CUBE_SVC_NS
//http configure
class http_config {
public:
	static int max_idle_time;
};

//http session class
class http_session : public net::session {
	//session send & recv buffer size
	static const int BUFSZ = 16*1024;
public:
	http_session() : _applet(0), _max_idle_interval(http_config::max_idle_time), _last_active_time(~0) {}
	virtual ~http_session() {}

	int on_open(void *arg);
	int on_send(int transfered);
	int on_recv(char *data, int transfered);
	int on_tick(::time_t now);
	void on_close();

private:
	//relate applet
	http::applet *_applet;

	//session request
	http::request _request;
	//session response
	http::response _response;

	//response data & transfered
	std::string _respdata;
	int _transfered;

	//idle control for session
	::time_t _last_active_time;
	int _max_idle_interval;
};

//http server class
class http_server {
public:
	http_server() {}
	virtual ~http_server() {}

	/*
	*	start http server on specified port
	*@param port: in, local http service port
	*@param workers: in, workers for http session
	*@param servlets: in, servlets for processing request
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port, int workers, http::applet *applet);

	/*
	*	stop http server
	*@return:
	*	void
	*/
	void stop();

private:
	//http server
	tcp_server<http_session> _server;
};
END_CUBE_SVC_NS
