#pragma once
#include <WinSock2.h>
#include <Windows.h>

#include <thread>

#include "cube.h"

BEGIN_CUBE_NAMESPACE

//iocp operation
typedef enum { IOCP_SEND, IOCP_RECV, IOCP_INVALID } iocp_opt;

//self defined overlapped structure for iocp
typedef struct overlapped
{
	OVERLAPPED _overlapped;
	WSABUF _buf;
	iocp_opt _opt;
	SOCKET _sock;

	overlapped(const char *data, int send_sz, SOCKET sock) :_opt(IOCP_SEND), _sock(sock)
	{
		_buf.len = send_sz;
		_buf.buf = new char[send_sz];
		memcpy(_buf.buf, data, send_sz);
		memset(&_overlapped, 0, sizeof(_overlapped));
	}

	overlapped(int recv_sz, SOCKET sock) :_opt(IOCP_RECV), _sock(sock)
	{
		_buf.len = recv_sz;
		_buf.buf = new char[recv_sz];
		memset(&_overlapped, 0, sizeof(_overlapped));
	}

	~overlapped()
	{
		delete[](_buf.buf);
		_buf.len = 0;
		_opt = IOCP_INVALID;
	}
}overlapped_t;

//session class
class session
{
public:
	session();
	virtual ~session();

	/*
	*	recalled when the connection has build, the @arg is the
	*parameter passed when the accepter started or specified by the
	*connector's connect method.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_open(void *arg);

	/*
	*	recalled when the the data has send out, with send size @sz_send.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_send(int sz_send);

	/*
	*	recalled when the the @data with size @sz_recv has received.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_recv(const char *data, int sz_recv);

	/*
	*	recalled when there is error happened on the connection, @err
	*is the errno return by the system.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_error(int err);

	/*
	*	recalled when the handler will be destroyed.
	*return:
	*	0--success, other--failed
	*/
	virtual int on_close();

	/*
	*	recalled when the timer has triggered.
	*return:
	*	0--success, other--failed
	*/
	virtual int on_timeout();

protected:
	/*make an asynchronize iocp send operation with data @buf which size is @sz*/
	int send(const char *buf, int sz);

	/*make an asynchronize iocp receive operation with size @sz*/
	int recv(int sz);

private:
	//socket of the relate handler
	SOCKET _sock;
	//remote peer ip
	unsigned int _ip;
	//remote peer port
	unsigned short _port;

	//service belong to
	void *_service;
};

template<class session>
class service
{
public:
	service()
	{

	}

	virtual ~service()
	{

	}

	//stop iocp service
	int start();

	//serve new session
	int serve(session *s);

	//stop iocp service
	int stop();

private:
	//iocp server thread
	static unsigned __stdcall serve_thread(void *arg);

private:
	//iocp handler
	HANDLE _iocp;
	//sessions of service
	map<uint, session*> _sessions;

	//thread of service
	std::thread *_thread;
	//stop flag for worker thread
	bool _stop;
};

template<class session>
class server
{
public:
	server()
	{

	}

	virtual ~server()
	{

	}

	int start();

	int accept(ushort port);

	/*stop accepter*/
	int stop();

private:
	//listen socket
	SOCKET _listen_sock;
	//listen port
	ushort _listen_port;

	//service for server
	service<session> _service;
};

template<class session>
class client
{
public:
	client()
	{

	}

	virtual ~client()
	{

	}

	int start();

	int connect(uint ip, ushort port);

	/*stop accepter*/
	int stop();

private:
	//service for client
	service<session> _service;
};
END_CUBE_NAMESPACE
