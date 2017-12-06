/*
*	sa - socket api module
*/
#pragma once
#include "cube.h"
#include <WinSock2.h>

//socket handle
#define socket_t uint

BEGIN_CUBE_NAMESPACE
class sa {
public:
	static std::string last_error();
	static std::string last_error(int error_code);
	static int last_error_code();
	static timeval mktime(int msecs);
};

class socket {
public:
	//flags/options/controls for socket
	typedef enum mode {
		OVERLAPPED = 0x00000001,
		REUSEADDR = 0x00000002,
		NONBLOCK = 0x00000004
	} mode_t;

	//exceptions of socket operaiton
	typedef std::exception ewarn;
	typedef std::exception efatal;
	typedef std::exception etimeout;
	typedef std::exception ewouldblock;

public:
	socket() : _socket(INVALID_SOCKET) {}
	virtual ~socket() {
		close();
	}
	
	/*
	*	listen on specified local ip/port for incoming connections
	*@param ip: in, local ip address
	*@param port: in, local tcp port
	*@param modes: in, flag/option/control of socket
	*@return:
	*	new socket when succeed, otherwise throw exceptions
	*/
	static socket listen(ushort port, int modes);
	static socket listen(uint ip, ushort port, int modes);

	/*
	*	connect to remote service with specified ip/port
	*@param ip: in, remote ip address
	*@param port: in, remote tcp port
	*@return:
	*	new socket when succeed, otherwise throw exceptions
	*/
	static socket connect(uint ip, ushort port, int modes);

	/*
	*	accept new incoming connection from the listen socket
	*@param waitmsecs: in, timeout for waiting new connection in million seconds
	*@param modes: in, socket options/control codes
	*@return:
	*	new connect in socket, or throw 
	*/
	socket accept(int modes);
	socket accept(int waitmsecs, int modes);

	/*
	*	send data to remote using send call
	*@param buf: in, pointer to a buffer containing the data to be transmitted
	*@param len: in, data to be send in @buf in bytes
	*@param flags: in, specify the way the call is made
	*@param error: in/out, error message when this is an error
	*@return:
	*	bytes send, throw exception when there is an error
	*/
	int send(const char* buf, int len, std::string *error = 0);
	int send(const char *buf, int len, int flags, std::string *error = 0);

	/*
	*	send data to remote using WSASend call
	*@param wsabuf: in, pointer to a WSABUF structure
	*@param wsabufs: in, pointer to and array of WSABUF structures
	*@param bufcount: in, number of WSABUF in @wsabufs
	*@param overlapped: in, pointer to a WSAOVERLAPPED structure
	*@param error: in/out, error message when this is an error
	*@return:
	*	0 for success, otherwise <0 and error will be set
	*/
	int send(LPWSABUF wsabuf, LPWSAOVERLAPPED overlapped, std::string *error = 0);
	int send(LPWSABUF wsabufs, int bufcount, LPWSAOVERLAPPED overlapped, std::string *error = 0);

	/*
	*	receive data from remote
	*@param buf: out, pointer to a buffer save the transmitted data
	*@param len: in, input buffer size in bytes
	*@param flags: in, specify the way the call is made
	*@return:
	*	bytes received, throw exception when there is an error
	*/
	int recv(char *buf, int len, std::string *error = 0);
	int recv(char *buf, int len, int flags, std::string *error = 0);

	/*
	*	receiving data from remote using WSARecv call
	*@param wsabuf: in, pointer to a WSABUF structure
	*@param wsabufs: in, pointer to and array of WSABUF structures
	*@param bufcount: in, number of WSABUF in @wsabufs
	*@param overlapped: in, pointer to a WSAOVERLAPPED structure
	*@param error: in/out, error message when this is an error
	*@return:
	*	0 for success, otherwise <0 and error will be set
	*/
	int recv(LPWSABUF wsabuf, LPWSAOVERLAPPED overlapped, std::string *error = 0);
	int recv(LPWSABUF wsabufs, int bufcount, LPWSAOVERLAPPED overlapped, std::string *error = 0);

	/*
	*	close socket
	*/
	void close();

private:
	socket(socket_t s, uint ip, ushort port) : _socket(s), _ip(ip), _port(port) {}

	/*
	*	set socket options/controls with specified modes
	*@param s: in, socket to set
	*@param modes: in, socket options/control codes
	*@return:
	*	void, throw exception when there is an error
	*/
	static void setmodes(socket_t s, int modes);

	/*
	*	create a socket by specified mode
	*@param modes: in, modes of socket
	*@return:
	*	created socket, otherwise throw an exception when there is an error
	*/
	static socket_t create(int modes);

public:
	/*
	*	get the socket
	*/
	socket_t handle();

private:
	//socket of connection
	socket_t _socket;

	//remote ip of socket
	uint _ip;
	//remote port of socket
	ushort _port;
};
END_CUBE_NAMESPACE
