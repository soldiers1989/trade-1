// server.cpp: 定义控制台应用程序的入口点。
//
#include "svcmgr.h"
#include "cube\str.h"

int main()
{
	svr::mgr::service::start(80);

	while(1)
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    return 0;
}

