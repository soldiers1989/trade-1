#include "sa.h"

BEGIN_CUBE_NAMESPACE
std::string sa::last_error() {
	return last_error(WSAGetLastError());
}

std::string sa::last_error(int error_code) {
	HLOCAL LocalAddress = NULL;

	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_FROM_SYSTEM, NULL, error_code, 0, (PTSTR)&LocalAddress, 0, NULL);
	std::string error((const char*)LocalAddress);

	LocalFree(LocalAddress);

	return error;
}

int sa::last_error_code() {
	return WSAGetLastError();
}

timeval sa::mktime(int msecs) {
	struct timeval tm;
	tm.tv_sec = msecs / 1000;
	tm.tv_usec = (msecs % 1000) * 1000;
	return tm;
}

socket socket::listen(ushort port, int modes) {
	return listen(INADDR_ANY, port, modes);
}

socket socket::listen(uint ip, ushort port, int modes) {
	//create listen socket
	socket_t sock = create(modes);

	//set socket options and controls
	try {
		setmodes(sock, modes);
	} catch (const std::exception& e) {
		::closesocket(sock);
		throw e;
	}

	//bind socket to listen port
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(ip);
	addr.sin_port = htons(port);
	int err = ::bind(sock, (struct sockaddr*)&addr, sizeof(addr));
	if (err == SOCKET_ERROR) {
		::closesocket(sock);
		throw efatal(sa::last_error().c_str());
	}

	//start listen on socket
	if (::listen(sock, SOMAXCONN) == SOCKET_ERROR) {
		::closesocket(sock);
		throw efatal(sa::last_error().c_str());
	}

	//listen on specified ip/port success, return listen socket
	return socket(sock, ip, port);
}

socket socket::connect(uint ip, ushort port, int modes) {
	//create connect socket
	socket_t sock = create(modes);

	//connect to remote ip:port
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(ip);
	addr.sin_port = htons(port);
	if (WSAConnect(sock, (struct sockaddr*)&addr, sizeof(addr), 0, 0, 0, 0) != 0) {
		::closesocket(sock);
		throw ewarn(sa::last_error().c_str());
	}

	//set socket options/controls
	try {
		setmodes(sock, modes);
	} catch (const std::exception& e) {
		::closesocket(sock);
		throw e;
	}

	//connect success, return new connected socket
	return socket(sock, ip, port);
}

socket socket::accept(int modes) {
	//store for remote address
	struct sockaddr_in remote;
	int addrlen = sizeof(remote);
	memset(&remote, 0, addrlen);
	socket_t sock = WSAAccept(_socket, (struct sockaddr*)&remote, &addrlen, 0, 0);
	if (sock == INVALID_SOCKET) {
		if (sa::last_error_code() == WSAEWOULDBLOCK)
			throw ewouldblock();
		else
			throw efatal(sa::last_error().c_str());
	}

	//set socket options/controls
	setmodes(sock, modes);

	return socket(sock, ntohl(remote.sin_addr.s_addr), ntohs(remote.sin_port));
}
socket socket::accept(int waitmsecs, int modes) {
	//select new connection event
	fd_set readfds;
	FD_ZERO(&readfds);
	fd_set exptfds;
	FD_ZERO(&exptfds);
	FD_SET(_socket, &readfds);
	FD_SET(_socket, &exptfds);

	struct timeval timeout = sa::mktime(waitmsecs);
	int fds = select(0, &readfds, NULL, &exptfds, &timeout);
	if (fds == 0)
		throw etimeout();

	if (FD_ISSET(_socket, &exptfds)) {
		throw efatal("exception on listen socket.");
	}

	if (fds == SOCKET_ERROR) {
		throw efatal(sa::last_error().c_str());
	}

	//store for remote address
	struct sockaddr_in remote;
	int addrlen = sizeof(remote);
	memset(&remote, 0, addrlen);
	socket_t sock = WSAAccept(_socket, (struct sockaddr*)&remote, &addrlen, 0, 0);
	if (sock == INVALID_SOCKET) {
		if (sa::last_error_code() == WSAEWOULDBLOCK)
			throw ewouldblock();
		else
			throw efatal(sa::last_error().c_str());
	}

	//set socket options/controls
	setmodes(sock, modes);

	return socket(sock, ntohl(remote.sin_addr.s_addr), ntohs(remote.sin_port));
}

int socket::send(const char *buf, int len, std::string *error/* = 0*/) {
	return send(buf, len, 0, error);
}

int socket::send(const char *buf, int len, int flags, std::string *error/* = 0*/) {
	int snd = ::send(_socket, buf, len, flags);
	if (snd == SOCKET_ERROR) {
		safe_assign<std::string>(error, sa::last_error());
		return -1;
	}

	return snd;
}

int socket::send(LPWSABUF wsabuf, LPWSAOVERLAPPED overlapped, std::string *error/* = 0*/) {
	return send(wsabuf, 1, overlapped, error);
}

int socket::send(LPWSABUF wsabufs, int bufcount, LPWSAOVERLAPPED overlapped, std::string *error/* = 0*/) {
	if (WSASend(_socket, wsabufs, bufcount, 0, 0, overlapped, 0) == SOCKET_ERROR) {
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING) {
			safe_assign<std::string>(error, sa::last_error(eno));
			return -1;
		}
	}

	return 0;
}

int socket::recv(char *buf, int len, std::string *error/* = 0*/) {
	return recv(buf, len, 0, error);
}

int socket::recv(char *buf, int len, int flags, std::string *error/* = 0*/) {
	int rcv = ::recv(_socket, buf, len, flags);
	if (rcv == SOCKET_ERROR) {
		safe_assign<std::string>(error, sa::last_error());
		return -1;
	}

	return rcv;
}

int socket::recv(LPWSABUF wsabuf, LPWSAOVERLAPPED overlapped, std::string *error/* = 0*/) {
	return recv(wsabuf, 1, overlapped, error);
}

int socket::recv(LPWSABUF wsabufs, int bufcount, LPWSAOVERLAPPED overlapped, std::string *error/* = 0*/) {
	DWORD flag = 0;
	if (WSARecv(_socket, wsabufs, 1, 0, &flag, overlapped, 0) == SOCKET_ERROR) {
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING) {
			safe_assign<std::string>(error, sa::last_error(eno));
			return -1;
		}
	}

	return 0;
}

void socket::close() {
	if (_socket != INVALID_SOCKET) {
		::closesocket(_socket);
		_socket = INVALID_SOCKET;
	}
}

void socket::setmodes(socket_t s, int modes) {
	if (modes & mode::REUSEADDR) {
		int on = 1;
		if (::setsockopt(s, SOL_SOCKET, SO_REUSEADDR, (const char*)&on, sizeof(on)) != 0)
			throw efatal(sa::last_error().c_str());
	}

	if (modes & mode::NONBLOCK) {
		unsigned long on = 1;
		if (::ioctlsocket(s, FIONBIO, &on) != 0)
			throw efatal(sa::last_error().c_str());
	}
}

socket_t socket::create(int modes) {
	socket_t sock = INVALID_SOCKET;
	//create socket with specified flags
	if (modes & mode::OVERLAPPED) {
		//create overlapped socket
		sock = WSASocketW(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
	} else {
		//create normal socket
		sock = WSASocketW(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, 0);
	}
	if (sock == INVALID_SOCKET)
		throw efatal(sa::last_error().c_str());

	//new created socket
	return sock;
}

socket_t socket::handle() {
	return _socket;
}

END_CUBE_NAMESPACE
