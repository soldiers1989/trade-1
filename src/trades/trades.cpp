// trades.cpp: 定义控制台应用程序的入口点。
//

#include "service.h"
#include "cube\net\init.h"

int main()
{
	//start service
	service::start();
	//wait for exit 
	service::wait();
	//stop service
	service::stop();

    return 0;
}

