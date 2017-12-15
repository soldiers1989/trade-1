#include "dbinit.h"
#include "cube\fd.h"
#include "cube\str.h"
BEGIN_SERVICE_NAMESPACE
int dbinit::init(const std::string &sqlfile, const std::string &name, db* db, std::string *error) {
	//create database first
	std::string sql = cube::str::format("create database if not exists %s default character set utf8 collate utf8_general_ci;", name.c_str());
	int err = db->execute(sql, error);
	if (err != 0) {
		return -1;
	}

	//use new database
	err = db->use(name, error);
	if (err != 0) {
		return -1;
	}

	//create tables
	std::string content;
	err = cube::file::read(sqlfile, content);
	if (err != 0) {
		cube::safe_assign<std::string>(error, cube::str::format("dbinit: read sql file %s failed.", sqlfile.c_str()));
		return -1;
	}
	std::vector<std::string> sqls = cube::str::split(content, ';');
	for (int i = 0; i < sqls.size(); i++) {
		sql = cube::str::strip(sqls[i]);
		if (sql.empty())
			continue;

		err = db->execute(sqls[i], error);
		if (err != 0) {
			return -1;
		}
	}

	return 0;
}
END_SERVICE_NAMESPACE
