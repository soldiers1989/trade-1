#include "broker.h"
#include "cube\fd.h"
#include "cube\str.h"

BEGIN_TRADE_NAMESPACE

char *dept::SEPROW = "\n";
char *dept::SEPCOL = ",";
int dept::SKIPROWS = 0;
int dept::SKIPCOLS = 0;

char *server::SEPROW = "\n";
char *server::SEPCOL = ",";
int server::SKIPROWS = 0;
int server::SKIPCOLS = 0;

char *broker::FILE_NAME_DEPTS = "depts";
char *broker::FILE_NAME_QUOTES = "quotes";
char *broker::FILE_NAME_TRADES = "trades";

int broker::load(const std::string &dir) {
	//load departements
	int err = load_depts(dir);
	if (err != 0)
		return -1;

	//load quote servers
	err = load_quotes(dir);
	if (err != 0)
		return -1;

	//load trade servers
	err = load_trades(dir);
	if (err != 0)
		return -1;

	return 0;
}

int broker::load_depts(const std::string &dir) {
	//configure file path
	std::string path = cube::path::make(dir, FILE_NAME_DEPTS);
	if (!cube::fd::isfile(path))
		return -1;

	//parse department config file
	std::string content;
	int err = cube::file::read(path, content);
	static std::vector<std::vector<std::string>>  table = cube::str::split(content, dept::SEPROW, dept::SEPCOL);
	for (size_t row = dept::SKIPROWS; row < table.size(); row++) {
		size_t pos = dept::SKIPCOLS;
		if (table[row].size() < pos + 2)
			continue; //invalid row
		_depts.push_back(dept(table[row][pos], table[row][pos + 1]));
	}

	return 0;
}

int broker::load_quotes(const std::string &dir) {
	//configure file path
	std::string path = cube::path::make(dir, FILE_NAME_QUOTES);
	if (!cube::fd::isfile(path))
		return -1;

	//parse config file
	std::string content;
	int err = cube::file::read(path, content);
	static std::vector<std::vector<std::string>>  table = cube::str::split(content, server::SEPROW, server::SEPCOL);
	for (size_t row = server::SKIPROWS; row < table.size(); row++) {
		size_t pos = server::SKIPCOLS;
		if (table[row].size() < pos + 3)
			continue; //invalid row

		std::string name = table[row][pos];
		std::string host = table[row][pos + 1];
		std::string port = table[row][pos + 2];
		if(cube::str::isnum(port.c_str()))
			_quotes.push_back(server(name, host, (ushort)::atoi(port.c_str())));
	}

	return 0;
}

int broker::load_trades(const std::string &dir) {
	//configure file path
	std::string path = cube::path::make(dir, FILE_NAME_TRADES);
	if (!cube::fd::isfile(path))
		return -1;

	//parse config file
	std::string content;
	int err = cube::file::read(path, content);
	static std::vector<std::vector<std::string>>  table = cube::str::split(content, server::SEPROW, server::SEPCOL);
	for (size_t row = server::SKIPROWS; row < table.size(); row++) {
		size_t pos = server::SKIPCOLS;
		if (table[row].size() < pos + 3)
			continue; //invalid row

		std::string name = table[row][pos];
		std::string host = table[row][pos + 1];
		std::string port = table[row][pos + 2];
		if (cube::str::isnum(port.c_str()))
			_trades.push_back(server(name, host, (ushort)::atoi(port.c_str())));
	}

	return 0;
}

int brokers::load(const std::string &dir) {
	//get sub directories from configure path, suppose file name is broker name
	std::vector<std::string> names = cube::fd::dirs(dir);

	//load each broker
	for (size_t i = 0; i < names.size(); i++) {
		broker broker(names[i]);
		int err = broker.load(cube::path::make(dir, names[i]));
		if (err != 0) {
			_brokers.push_back(broker);
		}
	}
	return 0;
}

END_TRADE_NAMESPACE
