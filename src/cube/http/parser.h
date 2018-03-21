#pragma once
#include "cube\http\buffer.h"
#include "cube\http\request.h"
BEGIN_CUBE_HTTP_NS
//message parser interface
class message_parser {
public:

	/*
	*	check if message body has parse completed
	*@return:
	*	bool
	*/
	virtual bool has_body_done() const = 0;

	/*
	*	notify parser with head line string
	*@param data: in, line string without "\r\n"
	*@return:
	*	0 for success, <0 for error
	*/
	virtual int add_head_line(const std::string &data) = 0;

	/*
	*	notify parser with end input of head data
	*@return:
	*	0 for success, <0 for error
	*/
	virtual int end_head_data() = 0;

	/*
	*	notify parser with body data
	*@param data: in, body data
	*@param sz: in, data size
	*@return:
	*	data size feed, <0 for error
	*/
	virtual int add_body_data(const char *data, int sz) = 0;

	/*
	*	notify parser with end input of body data
	*@return:
	*	0 for success, <0 for error
	*/
	virtual int end_body_data() = 0;
};

//stream parser interface
class stream_parser {
public:
	/*
	*	feed data to request buffer
	*@param data: in, data to feed
	*@param sz: in, data size
	*@return:
	*	size feeded, <0 when error
	*/
	virtual int feed(const char *data, int sz) = 0;

	/*
	*	check if request transfering has done
	*@return:
	*	true - request has done, false - not done
	*/
	virtual bool done() const = 0;
};

//request message parser
class request_message_parser : public message_parser {
public:
	request_message_parser() :  _start_line(true) { }
	virtual ~request_message_parser() {}

	bool has_body_done() const;
	int add_head_line(const std::string &data);
	int end_head_data();
	int add_body_data(const char *data, int sz);
	int end_body_data();

public:
	http::request &request() { return _request; }
	const http::request &request() const { return _request; }

private:
	//start line flag
	bool _start_line;

	//request object
	http::request _request;
};

//request stream parser
class request_stream_parser : public stream_parser {
public:
	request_stream_parser() : _head_feed_completed(false) {}
	virtual ~request_stream_parser() {}

	int feed(const char *data, int sz);

	bool done() const;
public:
	http::request &request() { return _message_parser.request(); }
	const http::request &request() const { return _message_parser.request(); }

private:
	//line buffer
	line_buffer _line_buffer;

	//head feed completed flag
	bool _head_feed_completed;
	//body feed completed flag
	bool _body_feed_completed;

	//request message parser
	request_message_parser _message_parser;
};
END_CUBE_HTTP_NS
