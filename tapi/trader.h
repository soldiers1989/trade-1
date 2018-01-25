/*
*	trader - trade data access module
*/
#pragma once
#include "broker.h"
#include "trade\trade.h"
#include <map>
BEGIN_SEC_NAMESPACE
class traders
{
public:
	traders() {}
	~traders() {}
	
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
	//std::map<std::string, a*> _accounts;
};
END_SEC_NAMESPACE
