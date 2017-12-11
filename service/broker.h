#include "stdsvr.h"
#include "cube\cube.h"
#include <vector>
#include <string>

BEGIN_SERVICE_NAMESPACE
//department of broker
typedef class dept {
public:
	dept(const std::string &name, const std::string &code) : name(name), code(code) {}
	dept() {}

	std::string name; //department name
	std::string code; //department code

public:
	/*
	*	variable for parsing configure file
	*/
	static char* SEPROW;
	static char* SEPCOL;
	static int SKIPROWS;
	static int SKIPCOLS;
} dept_t;

//server class
typedef class server {
public:
	server(const std::string &name, const std::string &host, ushort port) : name(name), host(host), port(port) {}
	~server() {}

	std::string name; //server name
	std::string host; //host address, ip or domain name
	ushort port; //service port

public:
	/*
	*	variable for parsing configure file
	*/
	static char* SEPROW;
	static char* SEPCOL;
	static int SKIPROWS;
	static int SKIPCOLS;

} server_t;

//broker class
class broker {
public:
	broker(const std::string &name) : _name(name) {}
	~broker() {}

	/*
	*	load broker information
	*@param dir: in, configure directory path of broker
	*@return:
	*	0 for success, otherwise<0
	*/
	int load(const std::string &dir);

	/*
	*	get broker informations
	*/
	const std::string& name() { return _name; }
	const dept& depts(int no) { return _depts[no]; }
	const server& quotes(int no) { return _quotes[no]; }
	const server& trades(int no) { return _trades[no]; }
	const std::vector<dept>& depts() { return _depts; }
	const std::vector<server>& quotes() { return _quotes; }
	const std::vector<server>& trades() { return _trades; }

public:
	/*
	*	file names for broker's configure file
	*/
	static char* FILE_NAME_DEPTS;
	static char* FILE_NAME_QUOTES;
	static char* FILE_NAME_TRADES;
private:
	/*
	*	load departments/quote servers/trade servers from configure file
	*@param dir: configure directory of broker
	*@return:
	*	0 for success, otherwise <0
	*/
	int load_depts(const std::string &dir);
	int load_quotes(const std::string &dir);
	int load_trades(const std::string &dir);

private:
	std::string _name; //broker name
	std::vector<dept> _depts; //broker's departments
	std::vector<server> _quotes; //quote servers
	std::vector<server> _trades; //trade servers
};

//brokers class
class brokers {
public:
	//brokers service configure directory in the working directory
	static char* DIR;

public:
	brokers() {}
	~brokers() {}

	/*
	*	load brokers information
	*@param workdir: in, working directory
	*@return:
	*	0 for success, otherwise<0
	*/
	int load(const std::string &workdir);

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
END_SERVICE_NAMESPACE
