/*
*	sa - socket api module
*/
#pragma once
#include "cube.h"

//socket handle
#define socket_t uint

BEGIN_CUBE_NAMESPACE
class sa {
public:
	static std::string last_error();
	static std::string last_error(int error_code);
	static std::exception last_exception();
	static std::exception last_exception(int error_code);

public:
	static int set_reuse_addr(socket_t socket);
	static int set_nonblock(socket_t socket);
	static int bind(socket_t socket, uint ip, ushort port);
	static socket_t listen(uint ip, ushort port, bool nonblk = true);
	static socket_t connect(uint ip, ushort port, bool nonblk = true);
};

class socket {
public:
	socket() {}
	virtual ~socket() {}

	void open(socket_t socket, uint ip, ushort port);

	int send(void *buf, void *overlapped, std::string *error = 0);

	int recv(void *buf, void *overlapped, std::string *error = 0);

	void close();

private:
	//socket of connection
	socket_t _socket;

	//remote ip of socket
	uint _ip;
	//remote port of socket
	ushort _port;
};
END_CUBE_NAMESPACE
