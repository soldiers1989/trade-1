#include "stdsvr.h"
#include "db.h"
#include <map>
#include <vector>
#include <string>
#include <mutex>

BEGIN_SERVICE_NAMESPACE
class brokerdao;
class brokersdao;

//department of broker
class dept {
public:
	dept(int id, const std::string &name, const std::string &code, bool disable, uint ctime) : id(id), code(code), name(name), disable(disable), ctime(ctime) {}
	dept(const std::string &name, const std::string &code) : name(name), code(code) {}
	dept() {}

	int id; //department id
	std::string code; //department code
	std::string name; //department name
	bool disable; //disable flag
	uint ctime; //create time

public:
	/*
	*	variable for parsing configure file
	*/
	static char* SEPROW;
	static char* SEPCOL;
	static int SKIPROWS;
	static int SKIPCOLS;
};

//server class
class server {
public:
	//server type
	typedef enum class type{trade=0, quote=1} type;

public:
	server(int id, const std::string &name, const std::string &host, ushort port, int stype, bool disable, uint ctime) : id(id), name(name), host(host), port(port), stype((type)stype), disable(disable), ctime(ctime) {}
	server(const std::string &name, const std::string &host, ushort port) : name(name), host(host), port(port) {}
	~server() {}

	int id; //server id
	std::string name; //server name
	std::string host; //host address, ip or domain name
	ushort port; //service port
	type stype; //server type;
	bool disable; //disable flag
	uint ctime; //create time

public:
	/*
	*	variable for parsing configure file
	*/
	static char* SEPROW;
	static char* SEPCOL;
	static int SKIPROWS;
	static int SKIPCOLS;

};

//broker property class
class broker_t {
public:
	broker_t() {}
	broker_t(const broker_t &brkr) : id(brkr.id), code(brkr.code), name(brkr.name), version(brkr.version), disable(brkr.disable), ctime(brkr.ctime) {}
	broker_t(const std::string &code, const std::string &name, const std::string &version, bool disable) : id(-1), code(code), name(name), version(version), disable(disable), ctime(0) {}
	broker_t(int id, const std::string &code, const std::string &name, const std::string &version, bool disable, uint ctime) : id(id), code(code), name(name), version(version), disable(disable), ctime(ctime) {}
	~broker_t() {}

	int id; //broker id
	std::string code; //broker code
	std::string name; //broker name
	std::string version; //client version
	bool disable; //disable flag
	uint ctime; //create time
};

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
	*	load broker information from configure dir
	*@param dir: in, configure dir path of broker
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise<0
	*/
	int init(const std::string &dir, std::string *error = 0);

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
	*	initialize brokers from configure dir
	*@param workdir: in, working directory
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise<0
	*/
	int init(const std::string &workdir, std::string *error = 0);

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

//broker dao class
class brokerdao : public dao {
public:
	brokerdao() {}
	~brokerdao() {}

	/*
	*	 select departments by specfied broker
	*@param id: in, broker id
	*@param depts: in/out, departments selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(int id, std::vector<dept> &depts, std::string *error = 0);

	/*
	*	 select departments by specfied broker
	*@param id: in, broker id
	*@param stype: in, server type
	*@param servers: in/out, servers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(int id, server::type stype, std::vector<server> &servers, std::string *error = 0);
};

//brokers dao class
class brokersdao : public dao {
public:
	brokersdao() {}
	~brokersdao() {}

	/*
	*	insert new broker
	*@param brkr: new broker
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int insert(const broker_t &brkr, std::string *error = 0);

	/*
	*	 select all brokers
	*@param brokers: in/out, brokers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(std::vector<broker_t> &brokers, std::string *error = 0);

	/*
	*	select specified broker by code
	*@param code: in, broker code
	*@param brkr: in/out, broker selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(const std::string &code, broker_t &brkr, std::string *error = 0);
};

END_SERVICE_NAMESPACE
