#pragma once
#include <WinSock2.h>
#include <map>
#include <list>
#include "cc.h"

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

public:
	/*
	*	open the new session
	*@param s: in, socket of new session
	*@param ip: in, remote ip address of new session
	*@param port: in, remote port of new session
	*@return:
	*	void
	*/
	void open(SOCKET s, uint ip, ushort port);

	/*
	*	close current session
	*@return:
	*	void
	*/
	void close();

	//session address information
	SOCKET socket() { return _socket; }
	uint ip() {	return _ip;	}
	ushort port() {	return _port; }

protected:
	/*
	*	make an asynchronize iocp send operation with data @buf which size is @sz
	*@param buf: in, data to send
	*@param sz: in, data size in bytes
	*@return:
	*	0 for success, otherwise <0
	*/
	int send(const char *buf, int sz);

	/*
	*	make an asynchronize iocp receive operation with size @sz
	*@param sz: in, data size in bytes want to receive
	*@return:
	*	0 for success, otherwise <0
	*/
	int recv(int sz);

private:
	//socket of the relate handler
	SOCKET _socket;
	//remote peer ip
	unsigned int _ip;
	//remote peer port
	unsigned short _port;
};

class service : public runnable
{
public:
	service() : _iocp(INVALID_HANDLE_VALUE)
	{

	}

	virtual ~service()
	{

	}

	/*
	*	start service with specified workers(concurrent threads for io completion port)
	*@param workers: in, concurrent thread number for io completion port, better the same with cpu cores
	*@param error: out, error message when start service failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(int workers = 0, std::string *error = 0)
	{
		/*create io complete port*/
		_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, 0);
		if (_iocp == NULL)
		{
			safe_assign<std::string>(error, sys::getlasterror());
			return -1; //create iocp failed.
		}

		/*start worker threads*/
		if (_threads.start(this, workers, error) != 0)
			return -1;

		return 0;
	}

	/*
	*	accept and serve a new incoming session
	*@param s: in, new incoming session
	*@param error: out, error message when serve the new session
	*@return:
	*	0 for success, otherwise <0
	*/
	int accept(session *s, std::string *error = 0)
	{
		//first bind the new session to completion port
		if (CreateIoCompletionPort((HANDLE)s->socket(), _iocp, (ULONG_PTR)s, 0) == NULL)
		{
			safe_assign<std::string>(error, sys::getlasterror());
			return -1;
		}

		//notify the session with connection opened event
		if (s->on_open(0) != 0)
		{
			//close session first
			s->close();
			//notify the session with connection closed event
			s->on_close();
		}


		return 0;
	}

	/*
	*	discard an existing session in the service
	*/
	int discard(session *s)
	{
		return 0;
	}

	//stop iocp service
	int stop()
	{
		//close all handles refer to the iocp


		//close the iocp handle
		if (_iocp != INVALID_HANDLE_VALUE)
		{
			CloseHandle(_iocp);
			_iocp = INVALID_HANDLE_VALUE;
		}
		return 0;
	}

public:
	/*
	*	process session
	*/
	void loop()
	{
		session *s = NULL; // session 
		DWORD transfered = 0; // data transfered
		overlapped_t *olp = NULL; // overlapped object

		/*process the handlers in the iocp*/
		if(GetQueuedCompletionStatus(_iocp, &transfered, (PULONG_PTR)&s, (LPOVERLAPPED*)&olp, 0))
		{
			if (transfered == 0)
			{//socket closed
			}
			else
			{
				int err = 0;
				if (olp->_opt == IOCP_SEND)
					err = hd->on_send(transfered);
				else if (olp->_opt == IOCP_RECV)
					err = hd->on_recv(olp->_buf.buf, transfered);
				else
					; // nerver happped
			}
		}
		else
		{
			int err = WSAGetLastError();
			if (err != WSA_WAIT_TIMEOUT)
			{
				worker->remove(olp->_sock);
				delete olp;
			}
		}
	}

private:
	//iocp handler
	HANDLE _iocp;
	//sessions of service
	std::map<SOCKET, session*> _sessions;

	//thread pool for service
	threads _threads;
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
