// server.cpp: 定义控制台应用程序的入口点。
//
#include "svcmgr.h"
#include "cube\str.h"

int main()
{
	const char* s = "get    /   http/1.2";
	std::vector<std::string> res2 = cube::str::split(s, ' ');
	std::vector<std::string> res0 = cube::str::splits(s, " ");
	std::vector<std::string> res1 = cube::str::splits(s, strlen(s), " ");
	//std::vector<std::string> res3 = cube::str::split(s, ' ', false);

	svr::service_manager::instance()->start(80);

	while(1)
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    return 0;
}

