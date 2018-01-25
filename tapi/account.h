/*
*	account - security account data access module
*/
#pragma once
#include "dao.h"
#include "broker.h"
#include "trade\tdx.h"
#include <mutex>

BEGIN_SEC_NAMESPACE
//sercurity accounts class
class accounts {
public:
	accounts(brokers *brokers) : _brokers(brokers) {}
	~accounts() {}

	/*
	*	initialize accounts module
	*@param error: out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int init(std::string *error = 0);

	/*
	*	add new account
	*@param acnt: in, new account
	*@param error: out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const account &acnt, std::string *error = 0);

	/*
	*	delete account by account id
	*@param id: in, account id
	*@param error: out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int del(int id, std::string *error = 0);

	/*
	*	destroy account module
	*/
	int destroy();

private:
	//accounts managed
	std::map<std::string, account> _accounts;
	//mutex for accounts
	std::mutex _mutex;

	//brokers supported
	brokers *_brokers;

	//database access
	accountsdao *_dao;
};
END_SEC_NAMESPACE
