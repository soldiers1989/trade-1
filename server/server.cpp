// server.cpp: 定义控制台应用程序的入口点。
//
#include "cube\fd.h"
int main()
{
	const char *path = "C:\\zd_zxjtzq\\base.dbf";
	cube::filestat fs;
	int err = cube::fd::stat(path, fs);

	size_t sz = 0;
	err = cube::fd::size(path, sz);

	std::vector<std::string> results = cube::fd::dirs("C:\\Workspace\\Project\\trade");

	/*cube::server<svr::sessionapi> server;
	server.start(80);

	while (true) {
		::Sleep(1000);
	}*/

    return 0;
}

