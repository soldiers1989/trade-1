// server.cpp: 定义控制台应用程序的入口点。
//
#include "sessionapi.h"
#include "cube\sa.h"

int listen() {
	/*create socket*/
	SOCKET _listen_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);//WSASocketW(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
	if (_listen_sock == INVALID_SOCKET)
		return -1; //create socket failed

				   /*set reuse address*/
	int on = 1;
	if (setsockopt(_listen_sock, SOL_SOCKET, SO_REUSEADDR, (const char*)&on, sizeof(on)) != 0)
		return -1;

	/*bind socket to listen port*/
	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	addr.sin_port = htons(8888);
	int err = ::bind(_listen_sock, (struct sockaddr*)&addr, sizeof(addr));
	if (err == SOCKET_ERROR)
		return -1; //bind socket failed.

				   /*listen on socket*/
	err = listen(_listen_sock, SOMAXCONN);
	if (err == SOCKET_ERROR)
		return -1; //listen on socket failed.

	return 0;
}

int main()
{
	listen();
	/*cube::socket::listen(8787, 0);

	cube::server<svr::sessionapi> server;
	server.start(8000);
	*/
	while (true) {
		::Sleep(1000);
	}

    return 0;
}

