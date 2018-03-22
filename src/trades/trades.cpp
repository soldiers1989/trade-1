// trades.cpp: 定义控制台应用程序的入口点。
//
#include "cube\net\init.h"
#include "trades\service.h"

int main()
{
	//start service
	trades::service::start();
	//wait for exit 
	trades::service::wait();
	//stop service
	trades::service::stop();

    return 0;
}

