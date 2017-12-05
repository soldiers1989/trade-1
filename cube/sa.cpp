#include "sa.h"
#include <WinSock2.h>

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

std::exception sa::last_exception() {
	return std::exception(last_error().c_str());
}

std::exception sa::last_exception(int error_code) {
	return std::exception(last_error(error_code).c_str());
}

int sa::set_reuse_addr(socket_t s) {
	int on = 1;
	if (::setsockopt(s, SOL_SOCKET, SO_REUSEADDR, (const char*)&on, sizeof(on)) != 0)
		return -1;
	return 0;
}

int sa::set_nonblock(socket_t s) {
	unsigned long io_mode = 1;
	if (::ioctlsocket(s, FIONBIO, &io_mode) != 0)
		return -1;
	return 0;
}

int sa::bind(socket_t s, uint ip, ushort port) {
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

socket_t sa::listen(uint ip, ushort port, bool nonblk/* = true*/) {
	/*create listen socket*/
	socket_t sock = WSASocketW(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
	if (sock == INVALID_SOCKET)
		return INVALID_SOCKET; //create socket failed

							   /*set reuse address*/
	if (set_reuse_addr(sock) != 0) {
		closesocket(sock);
		return INVALID_SOCKET;
	}

	/*set listen socket to nonblock mode*/
	if (nonblk && set_nonblock(sock) != 0) {
		closesocket(sock);
		return INVALID_SOCKET;
	}

	/*bind socket to listen port*/
	if (bind(sock, ip, port) == SOCKET_ERROR) {
		closesocket(sock);
		return INVALID_SOCKET; //bind socket failed.
	}
	/*listen on socket*/
	if (::listen(sock, SOMAXCONN) == SOCKET_ERROR) {
		closesocket(sock);
		return INVALID_SOCKET; //listen on socket failed
	}

	return sock;
}

socket_t sa::connect(uint ip, ushort port, bool nonblk/* = true*/) {
	/*create socket*/
	SOCKET sock = WSASocketW(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
	if (sock == INVALID_SOCKET)
		return INVALID_SOCKET; //create socket failed

	/*bind remote address*/
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(ip);
	addr.sin_port = htons(port);

	/*connect to remote*/
	if (WSAConnect(sock, (struct sockaddr*)&addr, sizeof(addr), NULL, NULL, NULL, NULL) != 0) {
		int eno = WSAGetLastError();
		if (eno != WSAEWOULDBLOCK) {
			closesocket(sock);
			return INVALID_SOCKET;
		}
	}

	// set non block
	if (nonblk && set_nonblock(sock) != 0) {
		closesocket(sock);
		return INVALID_SOCKET;
	}

	return sock;
}

void socket::open(socket_t socket, uint ip, ushort port){
	_socket = socket;
	_ip = ip;
	_port = port;
}

int socket::send(void *buf, void *overlapped, std::string *error/* = 0*/) {
	if (WSASend(_socket, (LPWSABUF)&buf, 1, 0, 0, (LPWSAOVERLAPPED)&overlapped, 0) == SOCKET_ERROR) {
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING) {
			safe_assign<std::string>(error, sa::last_error(eno));
			return -1;
		}
	}

	return 0;
}

int socket::recv(void *buf, void *overlapped, std::string *error/* = 0*/) {
	DWORD flag = 0;
	if (WSARecv(_socket, (LPWSABUF)&buf, 1, 0, &flag, (LPWSAOVERLAPPED)&overlapped, 0) == SOCKET_ERROR) {
		int eno = WSAGetLastError();
		if (eno != WSA_IO_PENDING) {
			safe_assign<std::string>(error, sa::last_error(eno));
			return -1;
		}
	}

	return 0;
}

void socket::close() {
	closesocket(_socket);
}
END_CUBE_NAMESPACE
