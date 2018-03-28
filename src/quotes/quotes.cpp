// quotes.cpp: 定义控制台应用程序的入口点。
//
#include "cube\net\init.h"
#include "quotes\service.h"

int main()
{
	//start service
	quotes::service::start();
	//wait for exit 
	quotes::service::wait();
	//stop service
	quotes::service::stop();
    return 0;
}
