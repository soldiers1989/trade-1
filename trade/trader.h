#pragma once
#include "broker.h"
BEGIN_TRADE_NAMESPACE
class trader
{
public:
	trader() {}
	~trader() {}
	
	/*
	*	initialize trader
	*@param brokerdir: in, brokers configure directory
	*@param workdir: in, working directory for trader
	*@return:
	*	0 for success, otherwise <0
	*/
	int init(const std::string &brokerdir, const std::string &workdir);

	/*
	*	destroy trader
	*/
	int destroy();

private:
	//supported brokers
	brokers _brokers;
};
END_TRADE_NAMESPACE
