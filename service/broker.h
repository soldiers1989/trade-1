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

//broker class
class broker {
public:
	broker(int id, const std::string &code, const std::string &name, const std::string &version, bool disable, uint ctime) : _id(id), _code(code), _name(name), _version(version), _disable(disable), _ctime(ctime), _dao(0) {}
	broker(const std::string &name) : _name(name), _dao(0) {}
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
	int _id; //broker id
	std::string _code; //broker code
	std::string _name; //broker name
	std::string _version; //client version
	bool _disable; //disable flag
	uint _ctime; //create time

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
	*	select a server
	*@param id: in, broker id
	*@param type: in, server type
	*@param server: in/out, server selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(int id, server::type type, server &server, std::string *error = 0);

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
	std::map<int, broker*> _brokers; //brokers, <id, broker*>
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
	*	 select brokers from database
	*@param brokers: in/out, brokers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(std::map<int, broker*> &brokers, std::string *error = 0);
};

END_SERVICE_NAMESPACE
