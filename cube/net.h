#pragma once
#include <WinSock2.h>
#include <thread>

#include "cube.h"

BEGIN_CUBE_NAMESPACE

//iocp operation
typedef enum { IOCP_SEND, IOCP_RECV, IOCP_INVALID } iocp_opt;

//self defined overlapped structure for iocp
typedef struct overlapped
{
	OVERLAPPED _overlapped;
	SOCKET _sock;
	iocp_opt _opt;
	WSABUF _buf;

	overlapped(SOCKET sock, const char *data, int send_sz) : _sock(sock), _opt(IOCP_SEND)
	{
		_buf.len = send_sz;
		_buf.buf = new char[send_sz];
		memcpy(_buf.buf, data, send_sz);
		memset(&_overlapped, 0, sizeof(_overlapped));
	}

	overlapped(SOCKET sock, int recv_sz) : _sock(sock), _opt(IOCP_RECV)
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

template<class session_impl>
class service
{
public:
	service() : _iocp(INVALID_HANDLE_VALUE), _thread(NULL)
	{

	}

	virtual ~service()
	{
		if (_iocp != INVALID_HANDLE_VALUE)
		{
			CloseHandle(_iocp);
			_iocp = INVALID_HANDLE_VALUE;
		}
	}

	/*
	*	start service
	*@return:
	*	0 for success, otherwise <0
	*/
	int start()
	{
		/*create io complete port*/
		_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, 0);
		if (_iocp == NULL)
			return -1; //create iocp failed.

					   /*start worker thread*/
		_worker_stop = false;
		_hdl = (HANDLE)_beginthreadex(NULL, 0, work_thread, this, 0, &_thread_id);
		if (_hdl == NULL)
		{
			_worker_stop = true;
			return -1; //start worker thread failed.
		}
		return 0;
	}

	//serve new session
	int serve(session *s)
	{
		return 0;
	}

	//stop iocp service
	int stop()
	{
		return 0;
	}

private:
	//iocp server thread
	static unsigned __stdcall serve_thread(void *arg)
	{

	}

private:
	//iocp handler
	HANDLE _iocp;
	//sessions of service
	map<uint, session_impl*> _sessions;

	//thread of service
	std::thread *_thread;
	//stop flag for worker thread
	bool _stop;
};

template<class session_impl>
class server
{
public:
	server() : _sock(INVALID_SOCKET), _port(0)
	{

	}

	virtual ~server()
	{
		if (_sock != INVALID_SOCKET)
		{
			closesocket(_sock);
			_sock = INVALID_SOCKET;
			_port = 0;
		}
	}

	int start()
	{
		return 0;
	}

	int accept(ushort port)
	{
		return 0;
	}

	/*stop accepter*/
	int stop()
	{
		return 0;
	}

private:
	//listen socket
	SOCKET _sock;
	//listen port
	ushort _port;

	//service for server
	service<session_impl> _service;
};

template<class session_impl>
class client
{
public:
	client()
	{

	}

	virtual ~client()
	{

	}

	int start()
	{
		return 0;
	}

	int connect(uint ip, ushort port)
	{
		return 0;
	}

	/*stop accepter*/
	int stop()
	{
		return 0;
	}

private:
	//service for client
	service<session_impl> _service;
};
END_CUBE_NAMESPACE
