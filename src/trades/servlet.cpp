#include "trades\lang.h"
#include "trades\alias.h"
#include "trades\config.h"
#include "cube\str\json.h"
#include "cube\str\stype.h"
#include "cube\str\format.h"
#include "trades\status.h"
#include "trades\account.h"
#include "trades\servlet.h"
BEGIN_TRADES_NAMESPACE
//response content type
std::string protocol::ctype = "application/json";

std::string protocol::resp(int status, const std::string &msg, const std::string &data) {
	std::string res = cube::str::format("{\"status\":%d,", status);
	res.append("\"msg\":\"" + cube::str::json(msg) + "\",");
	res.append("\"data\":");

	if (data.empty())
		res.append("[]");
	else
		res.append(data);

	res.append("}");

	return res;
}

bool authority::allow(const std::string &ip) {
	if (config::allowips.empty() || config::allowips.find(ip) != std::string::npos)
		return true;
	return false;
}

/*
*request:
*	/login?account=$account&pwd=$pwd&ip=$ip&port=$port&dept=dept&version=$version
*/
int login::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string pwd = req.params().get("pwd");

	//login account
	std::string laccount = req.params().get("laccount");
	if (laccount.empty()) {
		laccount = account;
	}

	//trade account
	std::string taccount = req.params().get("taccount");
	if (taccount.empty()) {
		taccount = account;
	}

	//trade password
	std::string tpwd = req.params().get("tpwd");
	if (tpwd.empty()) {
		tpwd = pwd;
	}

	std::string cpwd = req.params().get("cpwd");

	std::string ip = req.params().get("ip");
	std::string port = req.params().get("port");
	std::string dept = req.params().get("dept");
	std::string version = req.params().get("version");

	//check parameters
	if (laccount.empty() || taccount.empty() || tpwd.empty() || ip.empty() || port.empty() || dept.empty() || version.empty()) {
		std::string content = protocol::resp(status::ERROR_INVALID_PARAM, "invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	std::string errmsg("");
	//login account
	if (accounts::instance()->login(laccount, taccount, tpwd, cpwd, ip, (ushort)::atoi(port.c_str()), ::atoi(dept.c_str()), version, &errmsg) != 0) {
		std::string content = protocol::resp(status::ERROR, errmsg);
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	std::string content = protocol::resp(status::SUCCESS, "success");
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}


/*
*request:
*	/query/quote?account=$account&code=$code
*/
int quote::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string code = req.params().get("code");

	//check parameters
	if (account.empty() || code.empty()) {
		std::string content = protocol::resp(status::ERROR_INVALID_PARAM, "invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//query account
	int ret = accounts::instance()->quote(account, code, result, &errmsg);
	if (ret != 0) {
		std::string content = protocol::resp(ret, lang::instance()->conv(errmsg));
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//proccess alias if enabled
	if (alias::instance()->enabled()) {
		//charset will be convert in alias processing
		result = alias::instance()->process(result);
	} else {
		//process charset converting
		if (lang::instance()->needconv()) {
			result = lang::instance()->process(result);
		}
	}

	//response json
	std::string data = cube::str::json(result);

	std::string content = protocol::resp(status::SUCCESS, "success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/query/current?account=$account&category=$category	
*/
int querycurrent::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string category = req.params().get("category");

	//check parameters
	if (account.empty() || category.empty()) {
		std::string content = protocol::resp(status::ERROR_INVALID_PARAM, "invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//query account
	int ret = accounts::instance()->query(account, ::atoi(category.c_str()), result, &errmsg);
	if (ret != 0) {
		std::string content = protocol::resp(ret, lang::instance()->conv(errmsg));
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}
	
	//proccess alias if enabled
	if (alias::instance()->enabled()) {
		//charset will be convert in alias processing
		result = alias::instance()->process(result);
	} else {
		//process charset converting
		if (lang::instance()->needconv()) {
			result = lang::instance()->process(result);
		}
	}

	//response json
	std::string data = cube::str::json(result);

	std::string content = protocol::resp(status::SUCCESS, "success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/query/history?account=$account&category=$category&sdate=$sdate&edate=$edate
*/
int queryhistory::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string category = req.params().get("category");
	std::string sdate = req.params().get("sdate");
	std::string edate = req.params().get("edate");

	//check parameters
	if (account.empty() || category.empty() || sdate.empty() || edate.empty()) {
		std::string content = protocol::resp(status::ERROR_INVALID_PARAM, "invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//query account
	int ret = accounts::instance()->query(account, ::atoi(category.c_str()), sdate, edate, result, &errmsg);
	if (ret != 0) {
		std::string content = protocol::resp(ret, lang::instance()->conv(errmsg));
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//proccess alias if enabled
	if (alias::instance()->enabled()) {
		//charset will be convert in alias processing
		result = alias::instance()->process(result);
	} else {
		//process charset converting
		if (lang::instance()->needconv()) {
			result = lang::instance()->process(result);
		}
	}

	//response json
	std::string data = cube::str::json(result);

	std::string content = protocol::resp(status::SUCCESS, "success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/send/order?account=$account&otype=$otype&ptype=$ptype&gddm=$gddm&zqdm=$zqdm&price=$price&count=$count
*/
int order::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string otype = req.params().get("otype");
	std::string ptype = req.params().get("ptype");
	std::string gddm = req.params().get("gddm");
	std::string zqdm = req.params().get("zqdm");
	std::string price = req.params().get("price");
	std::string count = req.params().get("count");

	//check parameters
	if (account.empty() || otype.empty() || ptype.empty() || gddm.empty() || zqdm.empty() || price.empty() || count.empty()) {
		std::string content = protocol::resp(status::ERROR_INVALID_PARAM, "invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//send order
	int ret = accounts::instance()->order(account, ::atoi(otype.c_str()), ::atoi(ptype.c_str()), gddm, zqdm, (float)::atof(price.c_str()), ::atoi(count.c_str()), result, &errmsg);
	if (ret != 0) {
		std::string content = protocol::resp(ret, lang::instance()->conv(errmsg));
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//proccess alias if enabled
	if (alias::instance()->enabled()) {
		//charset will be convert in alias processing
		result = alias::instance()->process(result);
	} else {
		//process charset converting
		if (lang::instance()->needconv()) {
			result = lang::instance()->process(result);
		}
	}

	//response json
	std::string data = cube::str::json(result);

	std::string content = protocol::resp(status::SUCCESS, "success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/cancel/order?account=$account&seid=$seid&orderno=$orderno
*/
int cancel::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string seid = req.params().get("seid");
	std::string orderno = req.params().get("orderno");
	
	//check parameters
	if (account.empty() || seid.empty() || orderno.empty()) {
		std::string content = protocol::resp(status::ERROR_INVALID_PARAM, "invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//send order
	int ret = accounts::instance()->cancel(account, seid, orderno, result, &errmsg);
	if (ret != 0) {
		std::string content = protocol::resp(ret, lang::instance()->conv(errmsg));
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//proccess alias if enabled
	if (alias::instance()->enabled()) {
		//charset will be convert in alias processing
		result = alias::instance()->process(result);
	} else {
		//process charset converting
		if (lang::instance()->needconv()) {
			result = lang::instance()->process(result);
		}
	}

	//response json
	std::string data = cube::str::json(result);

	std::string content = protocol::resp(status::SUCCESS, "success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/logout?account=$account
*/
int logout::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");

	//check parameters
	if (account.empty()) {
		std::string content = protocol::resp(status::ERROR_INVALID_PARAM, "invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	std::string errmsg("");
	//logout account
	accounts::instance()->logout(account, &errmsg);


	std::string content = protocol::resp(status::SUCCESS, "success");
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

int echo::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::resp(status::ERROR_NOT_AUTHORIZED, "authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	std::string content = protocol::resp(status::SUCCESS, "success");
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}
END_TRADES_NAMESPACE
