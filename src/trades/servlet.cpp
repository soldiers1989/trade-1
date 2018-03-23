#include "trades\config.h"
#include "cube\str\json.h"
#include "cube\str\stype.h"
#include "trades\account.h"
#include "trades\servlet.h"
BEGIN_TRADES_NAMESPACE
std::string protocol::succ(const std::string &msg, const std::string &data) {
	std::string res("{\"status\":0,");
	res.append("\"msg\":\""+msg+"\",");
	res.append("\"data\":");


	if (data.empty())
		res.append("{}");
	else
		res.append(data);

	res.append("}");

	return res;
}

std::string protocol::fail(const std::string &msg, const std::string &data) {
	std::string res("{\"status\":-1,");
	res.append("\"msg\":\"" + msg + "\",");
	res.append("\"data\":");

	if (data.empty())
		res.append("{}");
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
*	/trade/login?account=$account&pwd=$pwd&ip=$ip&port=$port&dept=dept&version=$version
*/
int login::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string pwd = req.params().get("pwd");
	std::string ip = req.params().get("ip");
	std::string port = req.params().get("port");
	std::string dept = req.params().get("dept");
	std::string version = req.params().get("version");

	std::string data = "{\"account\":\"" + account + "\"}";
	//check parameters
	if (account.empty() || pwd.empty() || ip.empty() || port.empty() || dept.empty() || version.empty()) {
		std::string content = protocol::fail("invalid parameter.", data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	std::string errmsg("");
	//login account
	if (accounts::instance()->login(account, pwd, ip, (ushort)::atoi(port.c_str()), ::atoi(dept.c_str()), version, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg, data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}


/*
*request:
*	/trade/quote?account=$account&code=$code
*/
int quote::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string code = req.params().get("code");

	std::string data = "{\"account\":\"" + account + "\"}";

	//check parameters
	if (account.empty() || code.empty()) {
		std::string content = protocol::fail("invalid parameter.", data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//query account
	if (accounts::instance()->quote(account, code, result, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg, data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//response json
	data = cube::str::json(result);

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}

/*
*request:
*	/trade/query/current?account=$account&category=$category	
*/
int querycurrent::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string category = req.params().get("category");

	std::string data = "{\"account\":\"" + account + "\"}";

	//check parameters
	if (account.empty() || category.empty()) {
		std::string content = protocol::fail("invalid parameter.", data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//query account
	if (accounts::instance()->query(account, ::atoi(category.c_str()), result, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg, data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}
	
	//response json
	data = cube::str::json(result);

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}

/*
*request:
*	/trade/query/history?account=$account&category=$category&sdate=$sdate&edate=$edate
*/
int queryhistory::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string category = req.params().get("category");
	std::string sdate = req.params().get("sdate");
	std::string edate = req.params().get("edate");

	std::string data = "{\"account\":\"" + account + "\"}";

	//check parameters
	if (account.empty() || category.empty() || sdate.empty() || edate.empty()) {
		std::string content = protocol::fail("invalid parameter.", data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//query account
	if (accounts::instance()->query(account, ::atoi(category.c_str()), sdate, edate, result, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg, data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//response json
	data = cube::str::json(result);

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}

/*
*request:
*	/trade/order?account=$account&otype=$otype&ptype=$ptype&gddm=$gddm&zqdm=$zqdm&price=$price&count=$count
*/
int order::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
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

	std::string data = "{\"account\":\"" + account + "\"}";

	//check parameters
	if (account.empty() || otype.empty() || ptype.empty() || gddm.empty() || zqdm.empty() || price.empty() || count.empty()) {
		std::string content = protocol::fail("invalid parameter.", data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//send order
	if (accounts::instance()->order(account, ::atoi(otype.c_str()), ::atoi(ptype.c_str()), gddm, zqdm, (float)::atof(price.c_str()), ::atoi(count.c_str()), result, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg, data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//response json
	data = cube::str::json(result);

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}

/*
*request:
*	/trade/cancel?account=$account&seid=$seid&orderno=$orderno
*/
int cancel::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	std::string seid = req.params().get("seid");
	std::string orderno = req.params().get("orderno");
	
	std::string data = "{\"account\":\"" + account + "\"}";

	//check parameters
	if (account.empty() || seid.empty() || orderno.empty()) {
		std::string content = protocol::fail("invalid parameter.", data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	trade::table result;
	std::string errmsg("");
	//send order
	if (accounts::instance()->cancel(account, seid, orderno, result, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg, data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//response json
	data = cube::str::json(result);

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}

/*
*request:
*	/trade/logout?account=$account
*/
int logout::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string account = req.params().get("account");
	
	std::string data = "{\"account\":\"" + account + "\"}";

	//check parameters
	if (account.empty()) {
		std::string content = protocol::fail("invalid parameter.", data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	std::string errmsg("");
	//logout account
	if (accounts::instance()->logout(account, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg, data);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}


	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}

int echo::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	std::string content = protocol::succ("success");
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}
END_TRADES_NAMESPACE
