/*
*	broker - broker data access module
*/
#include "dao.h"
#include <map>
#include <vector>
#include <string>
#include <mutex>

BEGIN_SERVICE_NAMESPACE
//broker class
class broker {
public:
	broker(const broker_t &brkr) : _broker(brkr), _dao(0) {}
	~broker() {}

	/*
	*	load broker information from database
	*@param db: database object
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise<0
	*/
	int init(std::string *error = 0);

	/*
	*	select a server from broker
	*@param type: in, type of server
	*@param server: in/out, server selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise<0
	*/
	int select(server::type type, server &server, std::string *error = 0);

	/*
	*	destroy brokers
	*/
	int destroy();

public:
	/*
	*	get broker informations
	*/
	const broker_t &brkr() { return _broker; }
	const std::vector<dept>& depts() { return _depts; }
	const std::vector<server>& quotes() { return _quotes; }
	const std::vector<server>& trades() { return _trades; }


private:
	broker_t _broker; //broker property

	std::vector<dept> _depts; //broker's departments
	std::vector<server> _quotes; //quote servers
	std::vector<server> _trades; //trade servers

	brokerdao *_dao; //broker dao
};

//brokers class
class brokers {
public:
	typedef std::exception error;
	//brokers service configure directory in the working directory
	static char* DIR;
public:
	brokers() : _dao(0){}
	~brokers() {}

	/*
	*	initialize brokers from database
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise<0
	*/
	int init(std::string *error = 0);

	/*
	*	add new broker
	*@param brkr: in, new broker
	*@param error: out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const broker_t &brkr, std::string *error = 0);

	/*
	*	select a server
	*@param code: in, broker code
	*@param type: in, server type
	*@param server: in/out, server selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(const std::string &code, server::type type, server &server, std::string *error = 0);

	/*
	*	destroy brokers
	*/
	int destroy();
public:
	/*
	*	get broker number in vector
	*/
	int num() { return _brokers.size(); }

private:
	std::map<std::string, broker*> _brokers; //brokers, <id, broker*>
	std::mutex _mutex; //mutex for brokers

	brokersdao *_dao; //brokers dao
};
END_SERVICE_NAMESPACE
