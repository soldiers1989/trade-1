#include "net.h"
BEGIN_CUBE_NAMESPACE
session::session() :_socket(INVALID_SOCKET), _ip(0), _port(0)
{

}

session::session(SOCKET s, uint ip, ushort port) : _socket(s), _ip(ip), _port(port)
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

session* session::create(SOCKET s, uint ip, ushort port)
{
	return new session(s, ip, port);
}

int session::send(const char *buf, int sz)
{
	DWORD snt = 0;
	overlapped_t *olp = new overlapped_t(_socket, buf, sz);
	if (WSASend(_socket, &(olp->_buf), 1, &snt, 0, &(olp->_overlapped), NULL) == SOCKET_ERROR)
	{
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING)
		{
			delete olp;
			return -1;
		}
	}
	
	return (int)snt;
}

int session::recv(int sz)
{
	DWORD rcv = 0, flag = 0;
	overlapped_t *olp = new overlapped_t(_socket, sz);
	if (WSARecv(_sock, &(olp->_buf), 1, &rcv, &flag, &(olp->_overlapped), NULL) == SOCKET_ERROR)
	{
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING)
		{
			delete olp;
			return -1;
		}
	}

	return (int)rcv;
}
END_CUBE_NAMESPACE
