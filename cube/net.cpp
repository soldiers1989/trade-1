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

int session::on_send(io_context *context, uint transfered)
{
	return -1;
}

int session::on_recv(io_context *context, uint transfered)
{
	return -1;
}

int session::on_close()
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

int session::send(io_context *context, std::string *error/* = 0*/)
{
	std::lock_guard<std::mutex> lock(_mutex);
	if (WSASend(_socket, &(context->_buf), 1, 0, 0, &(context->_overlapped), NULL) == SOCKET_ERROR)
	{
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING)
		{
			safe_assign<std::string>(error, sys::geterrormsg(eno));
			return -1;
		}
	}

	//add to pending context list
	_contexts.push_back(context);
	
	return 0;
}

int session::recv(io_context *context, std::string *error/* = 0*/)
{
	std::lock_guard<std::mutex> lock(_mutex);
	DWORD flag = 0;
	if (WSARecv(_socket, &(context->_buf), 1, 0, &flag, &(context->_overlapped), NULL) == SOCKET_ERROR)
	{
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING) {
			safe_assign<std::string>(error, sys::geterrormsg(eno));
			return -1;
		}
	}

	//add to pending context list
	_contexts.push_back(context);

	return 0;
}

int session::_on_send(io_context *context, uint transfered)
{
	std::lock_guard<std::mutex> lock(_mutex);
	//remove from pending context
	_contexts.remove(context);

	return on_send(context, transfered);
}

int session::_on_recv(io_context *context, uint transfered)
{
	std::lock_guard<std::mutex> lock(_mutex);
	//remove from pending context
	_contexts.remove(context);

	return on_recv(context, transfered);
}
END_CUBE_NAMESPACE
