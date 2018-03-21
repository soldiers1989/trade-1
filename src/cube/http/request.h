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
	request() {}
	virtual ~request() {}

	std::string pack() const;
	int parse(const std::string &str);

public:
	const http::query &query() const { return _query; }
	const http::headers &headers() const { return _headers; }

private:
	//http request query
	http::query _query;
	//http request headers
	http::headers _headers;
};
END_CUBE_HTTP_NS
