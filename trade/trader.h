#pragma once
#include "trade.h"
#include "broker.h"
#include <map>
BEGIN_TRADE_NAMESPACE
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
	std::map<std::string, trade*> _accounts;
};
END_TRADE_NAMESPACE
