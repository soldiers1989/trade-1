// server.cpp: 定义控制台应用程序的入口点。
//
#include "cube\fd.h"
int main()
{
	std::vector<cube::findres> results = cube::fd::find("C:\\Workspace\\Project\\Test\\test\\*", cube::fd::DIR);

	/*cube::server<svr::sessionapi> server;
	server.start(80);

	while (true) {
		::Sleep(1000);
	}*/

    return 0;
}

