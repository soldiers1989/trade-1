#include "net.h"
BEGIN_CUBE_NAMESPACE
session::session() :_sock(INVALID_SOCKET), _ip(0), _port(0)
{

}

session::~session(void)
{
	if (_sock != INVALID_SOCKET)
		closesocket(_sock);
	_sock = INVALID_SOCKET;
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

int session::send(const char *buf, int sz)
{
	DWORD snt = 0;
	overlapped_t *olp = new overlapped_t(buf, sz, _sock);
	if (WSASend(_sock, &(olp->_buf), 1, &snt, 0, &(olp->_overlapped), NULL) == SOCKET_ERROR)
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
	DWORD rcv = 0;
	DWORD flag = 0;
	overlapped_t *olp = new overlapped_t(sz, _sock);
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
