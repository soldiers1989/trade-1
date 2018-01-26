// server.cpp: 定义控制台应用程序的入口点。
//
#include "svcmgr.h"
#include "cube\str.h"
#include "tapi\dbm.h"
int main()
{
	//set manage service
	svr::mgr::service::start();

	while(1)
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    return 0;
}

