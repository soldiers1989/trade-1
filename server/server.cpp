// server.cpp: 定义控制台应用程序的入口点。
//
#include "sessionapi.h"

int main()
{
	cube::server<svr::sessionapi> server;
	server.start(8000);

	while (true) {
		::Sleep(1000);
	}

    return 0;
}

