#include "stdtrd.h"
#include "cube\cube.h"

BEGIN_TRADE_NAMESPACE
//department of broker
typedef class dept {
public:
	dept(const std::string &name, const std::string &code) : name(name), code(code) {}
	dept() {}

	std::string name; //department name
	std::string code; //department code
} dept_t;

//server class
typedef class server {
public:
	server(const std::string &name, const std::string &ip, ushort port) : name(name), ip(ip), port(port) {}
	~server() {}

	std::string name; //server name
	std::string ip; //ip address
	ushort port; //service port
} server_t;

//broker class
class broker {
public:
	broker() {}
	~broker() {}

	/*
	*	load broker information
	*@param dir: in, configure directory path of broker
	*@return:
	*	0 for success, otherwise<0
	*/
	int load(const char *dir);

	/*
	*	get broker informations
	*/
	const std::string& name() { return _name; }
	const std::vector<dept>& depts() { return _depts; }
	const std::vector<server>& quotes() { return _quotes; }
	const std::vector<server>& trades() { return _trades; }

private:
	std::string _name; //broker name
	std::vector<dept> _depts; //broker's departments
	std::vector<server> _quotes; //quote servers
	std::vector<server> _trades; //trade servers
};

//brokers class
class brokers {
public:
	brokers() {}
	~brokers() {}

	/*
	*	load brokers information
	*@param dir: in, configure directory path of brokers
	*@return:
	*	0 for success, otherwise<0
	*/
	int load(const char *dir);

	/*
	*	get broker number in vector
	*/
	int num() { return _brokers.size(); }

	/*
	*	get broker by it's number in broker vector
	*@param no: in, number in vector, from 0
	*@return:
	*	broker
	*/
	const broker& get(int no) { return _brokers[no]; }

private:
	std::vector<broker> _brokers; //brokers
};
END_TRADE_NAMESPACE
