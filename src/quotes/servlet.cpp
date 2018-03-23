#include "quotes\config.h"
#include "cube\str\json.h"
#include "cube\str\cast.h"
#include "cube\str\stype.h"
#include "quotes\quoter.h"
#include "quotes\servlet.h"
BEGIN_QUOTES_NAMESPACE
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
*	/quote/connect?ip=$ip&port=$port
*/
int connect::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string ip = req.params().get("ip");
	std::string port = req.params().get("port");

	//check parameters
	if (ip.empty() || port.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	quote::table result;
	std::string errmsg("");
	//login account
	if (quoter::instance()->connect(ip, (ushort)::atoi(port.c_str()), result, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}
	
	//response json
	std::string data = cube::str::json(result);
	
	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}


/*
*request:
*	/trade/query/count?market=$market
*/
int query_security_count::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//get request parameters
	std::string market = req.params().get("market");

	//check parameters
	if (market.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	int count = -1;
	std::string errmsg("");
	//query account
	if (quoter::instance()->query_security_count(::atoi(market.c_str()), count, &errmsg) != 0) {
		std::string content = protocol::fail(errmsg);
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//response json
	std::string data = "{\"count\":"+cube::str::string(count)+"}";

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
	return 0;
}

/*
*request:
*	/quote/disconnect
*/
int disconnect::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}

	//disconnect
	if (quoter::instance()->disconnect() != 0) {
		std::string content = protocol::fail("disconnect error");
		resp.set_content(content.c_str(), content.length(), "application/json;charset=gbk");
		return 0;
	}
	
	std::string content = protocol::succ("success");
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
END_QUOTES_NAMESPACE
