// server.cpp: 定义控制台应用程序的入口点。
//
#include "cube\fd.h"
#include "db.h"

int main()
{
	svr::db mydb;
	mydb.connect("10.0.0.8", "test", "test", "mysql");
	/*cube::server<svr::sessionapi> server;
	server.start(80);

	while (true) {
		::Sleep(1000);
	}*/

    return 0;
}

