#include "net.h"
BEGIN_CUBE_NAMESPACE
session::session() :_socket(INVALID_SOCKET), _ip(0), _port(0)
{

}

session::~session(void)
{
	if (_socket != INVALID_SOCKET)
	{
		closesocket(_socket);
		_socket = INVALID_SOCKET;
	}
}

int session::on_open(void *arg)
{
	return -1;
}

int session::on_send(int sz_send)
{
	return -1;
}

int session::on_recv(const char*data, int sz_recv)
{
	return -1;
}

int session::on_close()
{
	return -1;
}

int session::on_error(int err)
{
	return -1;
}

int session::on_timeout()
{
	return -1;
}

void session::open(SOCKET s, uint ip, ushort port)
{
	_socket = s;
	_ip = ip;
	_port = port;
}

void session::close()
{
	if (_socket != INVALID_SOCKET)
	{
		closesocket(_socket);
		_socket = INVALID_SOCKET;
	}
}

int session::send(const char *buf, int sz)
{
	overlapped_t *olp = new overlapped_t(_socket, buf, sz);
	if (WSASend(_socket, &(olp->_buf), 1, 0, 0, &(olp->_overlapped), NULL) == SOCKET_ERROR)
	{
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING)
		{
			delete olp;
			return -1;
		}
	}
	
	return 0;
}

int session::recv(int sz)
{
	DWORD flag = 0;
	overlapped_t *olp = new overlapped_t(_socket, sz);
	if (WSARecv(_socket, &(olp->_buf), 1, 0, &flag, &(olp->_overlapped), NULL) == SOCKET_ERROR)
	{
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING)
		{
			delete olp;
			return -1;
		}
	}

	return 0;
}
END_CUBE_NAMESPACE
