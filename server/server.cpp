// server.cpp: 定义控制台应用程序的入口点。
//
#include "cube\fd.h"
int main()
{
	std::vector<std::string> results = cube::fd::dirs("C:\\Workspace\\Project\\trade");

	/*cube::server<svr::sessionapi> server;
	server.start(80);

	while (true) {
		::Sleep(1000);
	}*/

    return 0;
}

