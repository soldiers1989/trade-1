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
BEGIN_NET_NAMESPACE
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
	*	recalled when the timer
	*/
	virtual int on_timer(int id);

	/*
	*	recalled when the handler will be destroyed.
	*return:
	*	always 0
	*/
	virtual void on_close();
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
END_NET_NAMESPACE
END_CUBE_NAMESPACE
