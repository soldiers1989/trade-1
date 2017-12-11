#pragma once
#include "broker.h"
#include "trade\trade.h"
#include <map>
BEGIN_SERVICE_NAMESPACE
class trader
{
public:
	trader() {}
	~trader() {}
	
	/*
	*	initialize trader
	*@param workdir: in, working directory for trader
	*@return:
	*	0 for success, otherwise <0
	*/
	int init(const std::string &workdir);

	/*
	*	destroy trader
	*/
	int destroy();

private:
	//supported brokers
	brokers _brokers;

	//online accounts, <account name, trade object>
	std::map<std::string, trade::trade*> _accounts;
};
END_SERVICE_NAMESPACE
