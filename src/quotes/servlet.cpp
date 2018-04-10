#include "quotes\lang.h"
#include "quotes\alias.h"
#include "quotes\config.h"
#include "cube\str\json.h"
#include "cube\str\cast.h"
#include "cube\str\stype.h"
#include "quotes\quoter.h"
#include "quotes\servlet.h"
BEGIN_QUOTES_NAMESPACE
//response content type
std::string protocol::ctype = "application/json";

std::string protocol::succ(const std::string &msg, const std::string &data) {
	std::string res("{\"status\":0,");
	res.append("\"msg\":\""+cube::str::json(msg)+"\",");
	res.append("\"data\":");


	if (data.empty())
		res.append("[]");
	else
		res.append(data);

	res.append("}");

	return res;
}

std::string protocol::fail(const std::string &msg, const std::string &data) {
	std::string res("{\"status\":-1,");
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
*	/connect?ip=$ip&port=$port
*/
int connect::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string ip = req.params().get("ip");
	std::string port = req.params().get("port");

	//check parameters
	if (ip.empty() || port.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	quote::table result;
	std::string errmsg("");
	//login account
	if (quoter::instance()->connect(ip, (ushort)::atoi(port.c_str()), result, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
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
	
	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/quote/count?market=$market
*/
int query_security_count::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string market = req.params().get("market");

	//check parameters
	if (market.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	int count = -1;
	std::string errmsg("");
	//query account
	if (quoter::instance()->query_security_count(::atoi(market.c_str()), count, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//response json
	std::string data = "[[\"count\"],["+cube::str::string(count)+"]]";

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}


/*
*request:
*	/query/security/list?market=$market&start=$start
*/
int query_security_list::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string market = req.params().get("market");
	std::string start = req.params().get("start");
	
	//check parameters
	if (market.empty() || start.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	int count = 0;
	quote::table result;
	std::string errmsg("");
	//query security list
	if (quoter::instance()->query_security_list(::atoi(market.c_str()), ::atoi(start.c_str()), count, result, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
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

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/query/security/kline?line=$line&market=$market&zqdm=$zqdm&start=$start
*/
int query_security_kline::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string line = req.params().get("line");
	std::string market = req.params().get("market");
	std::string zqdm = req.params().get("zqdm");
	std::string start = req.params().get("start");

	//check parameters
	if (line.empty() || market.empty() || zqdm.empty() || start.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	int count = 0;
	quote::table result;
	std::string errmsg("");
	//query security list
	if (quoter::instance()->query_security_kline(::atoi(line.c_str()), ::atoi(market.c_str()), zqdm, ::atoi(start.c_str()), count, result, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
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

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/query/index/kline?line=$line&market=$market&zqdm=$zqdm&start=$start
*/
int query_index_kline::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string line = req.params().get("line");
	std::string market = req.params().get("market");
	std::string zqdm = req.params().get("zqdm");
	std::string start = req.params().get("start");

	//check parameters
	if (line.empty() || market.empty() || zqdm.empty() || start.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	int count = 0;
	quote::table result;
	std::string errmsg("");
	//query security list
	if (quoter::instance()->query_index_kline(::atoi(line.c_str()), ::atoi(market.c_str()), zqdm, ::atoi(start.c_str()), count, result, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
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

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/quote/current?market=$market&zqdm=$zqdm
*/
int query_current_time_data::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string market = req.params().get("market");
	std::string zqdm = req.params().get("zqdm");

	//check parameters
	if (market.empty() || zqdm.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	quote::table result;
	std::string errmsg("");
	//query account
	if (quoter::instance()->query_current_time_data(::atoi(market.c_str()), zqdm, result, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
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

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

int query_current_deal_data::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string market = req.params().get("market");
	std::string zqdm = req.params().get("zqdm");

	//check parameters
	if (market.empty() || zqdm.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	int count = 0;
	quote::table result;
	std::string errmsg("");
	//query account
	if (quoter::instance()->query_current_deal_data(::atoi(market.c_str()), zqdm, 0, count,result, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
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

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

/*
*request:
*	/query/current/deal/data?market=$market&zqdm=$zqdm
*/
int query_current_quote_data::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//get request parameters
	std::string market = req.params().get("market");
	std::string zqdm = req.params().get("zqdm");

	//check parameters
	if (market.empty() || zqdm.empty()) {
		std::string content = protocol::fail("invalid parameter.");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	quote::table result;
	std::string errmsg("");
	//query account
	if (quoter::instance()->query_current_quote_data(::atoi(market.c_str()), zqdm, result, &errmsg) != 0) {
		std::string content = protocol::fail(lang::instance()->conv(errmsg));
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

	std::string content = protocol::succ("success", data);
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
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
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	//disconnect
	if (quoter::instance()->disconnect() != 0) {
		std::string content = protocol::fail("disconnect error");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}
	
	std::string content = protocol::succ("success");
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}

int echo::handle(const cube::http::request &req, cube::http::response &resp) {
	//check authority
	if (!authority::allow(req.peerip())) {
		std::string content = protocol::fail("authority denied");
		resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
		return 0;
	}

	std::string content = protocol::succ("success");
	resp.set_content(content.c_str(), content.length(), protocol::ctype, lang::charset());
	return 0;
}
END_QUOTES_NAMESPACE
