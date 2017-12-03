#include "net.h"
BEGIN_CUBE_NAMESPACE

int socket::set_reuseaddr(SOCKET s)
{
	int on = 1;
	if (::setsockopt(s, SOL_SOCKET, SO_REUSEADDR, (const char*)&on, sizeof(on)) != 0)
		return -1;
	return 0;
}
int socket::set_nonblock(SOCKET s)
{
	unsigned long io_mode = 1;
	if (::ioctlsocket(s, FIONBIO, &io_mode) != 0)
		return -1;
	return 0;
}

int socket::bind(SOCKET s, uint ip, ushort port)
{
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(ip);
	addr.sin_port = htons(port);
	int err = ::bind(s, (struct sockaddr*)&addr, sizeof(addr));
	if (err == SOCKET_ERROR)
		return -1; //bind socket failed.
	return 0;
}

SOCKET socket::listen(uint ip, ushort port, bool nonblk/* = true*/)
{
	/*create listen socket*/
	SOCKET sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
	if (sock != INVALID_SOCKET &&)
		return INVALID_SOCKET; //create socket failed

							   /*set reuse address*/
	if (socket::set_reuseaddr(sock) != 0)
	{
		closesocket(sock);
		return INVALID_SOCKET;
	}

	/*set listen socket to nonblock mode*/
	if (nonblk && socket::set_nonblock(sock) != 0)
	{
		closesocket(sock);
		return INVALID_SOCKET;
	}

	/*bind socket to listen port*/
	if (socket::bind(sock, ip, port) == SOCKET_ERROR)
	{
		closesocket(sock);
		return INVALID_SOCKET; //bind socket failed.
	}
	/*listen on socket*/
	if (::listen(sock, SOMAXCONN) == SOCKET_ERROR)
	{
		closesocket(sock);
		return INVALID_SOCKET; //listen on socket failed
	}

	return sock;
}

SOCKET socket::connect(uint ip, ushort port, bool nonblk/* = true*/)
{
	/*create socket*/
	SOCKET sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
	if (sock == INVALID_SOCKET)
		return INVALID_SOCKET; //create socket failed

	/*bind remote address*/
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(ip);
	addr.sin_port = htons(port);

	/*connect to remote*/
	if (WSAConnect(sock, (struct sockaddr*)&addr, sizeof(addr), NULL, NULL, NULL, NULL) != 0)
	{
		int eno = WSAGetLastError();
		if (eno != WSAEWOULDBLOCK)
		{
			closesocket(sock);
			return INVALID_SOCKET;
		}
	}

	// set non block
	if (nonblk && socket::set_nonblock(sock) != 0)
	{
		closesocket(sock);
		return INVALID_SOCKET;
	}

	return sock;
}

session::session(SOCKET s, uint ip, ushort port) :_socket(s), _ip(ip), _port(port)
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

void session::_open(SOCKET s, uint ip, ushort port)
{
	_socket = s;
	_ip = ip;
	_port = port;
}

void session::_close()
{
	if (_socket != INVALID_SOCKET)
	{
		closesocket(_socket);
		_socket = INVALID_SOCKET;
	}
}

int session::_on_open(void *arg)
{
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

int session::_on_close()
{
	return 0;
}
END_CUBE_NAMESPACE
