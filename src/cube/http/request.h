#pragma once
#include <mutex>
#include <memory>
#include "cube\http\query.h"
#include "cube\http\header.h"
#include "cube\http\entity.h"
#include "cube\http\message.h"
BEGIN_CUBE_HTTP_NS
//http request class
class request {
public:
	request() : _peerip("") {}
	virtual ~request() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	const std::string &method() const { return _query.method(); }
	const std::string &path() const { return _query.path(); }
	const http::params &params() const { return _query.params(); }
	void peerip(const std::string &ip){ _peerip = ip; }
	const std::string &peerip() const { return _peerip; }

public:
	const http::query &query() const { return _query; }
	const http::headers &headers() const { return _headers; }

private:
	//http request query
	http::query _query;
	//http request headers
	http::headers _headers;

	//remote peer ip
	std::string _peerip;

};
END_CUBE_HTTP_NS
