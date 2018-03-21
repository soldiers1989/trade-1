#pragma once
#include <mutex>
#include "cube\net\socket.h"
#include "cube\net\context.h"
BEGIN_CUBE_NET_NS
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
END_CUBE_NET_NS
