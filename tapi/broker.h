/*
*	broker - broker data access module
*/
#include "dao.h"
#include <map>
#include <mutex>

BEGIN_SEC_NAMESPACE
//brokers class
class brokers {
public:
	typedef cube::cexception error;

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
	int add(const broker &brkr, std::string *error = 0);

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
	brokersdao *_dao; //brokers dao

	std::map<std::string, broker> _brokers; //brokers, <id, broker*>
	std::mutex _mutex; //mutex for brokers
};
END_SEC_NAMESPACE
