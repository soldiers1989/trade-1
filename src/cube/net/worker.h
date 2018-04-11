#pragma once
#include "cube\cc\looper.h"
BEGIN_CUBE_NET_NS
class service;
class workers : public cc::task{
public:
	workers() {}
	virtual ~workers() {}

	/*
	*	start workers
	*/
	void start(int num, service *service);

	/*
	*	stop workers
	*/
	void stop();
public:
	/*
	*	worker to do the queued complete events
	*/
	void run();

private:
	//net service
	service *_service;
	//loopers of worker
	cc::loopers _loopers;
};

END_CUBE_NET_NS
