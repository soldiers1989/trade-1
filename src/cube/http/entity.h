#pragma once
#include <vector>
#include <memory>
#include <iostream>
#include "cube\http\header.h"
#include "cube\http\stream.h"
BEGIN_CUBE_HTTP_NS
//http entity class
class entity {
public:
	entity() : _length(0), _type(""), _language(""), _encoding(""), _range(""), _expires("") {}
	virtual ~entity() { }

	std::string pack() const;
	int parse(const std::string &str);

	/*
	*	set content type & charset
	*/
	void set_type(const char *type, const char *charset = 0);

	/*
	*	get entity data
	*/
	std::string get_data() const;

	/*
	*	set entity data
	*/
	void set_data(const char *data, int sz);

	/*
	*	get meta information from entity
	*/
	void get_meta(headers &headers);

	/*
	*	set entity meta information by http message headers
	*@param headers: in, http message headers
	*@return:
	*	0 for success, otherwise <0
	*/
	int set_meta(const headers &headers);

	/*
	*	add entity data of body
	*@param data: in, entity data
	*@param sz: in, entity data size
	*@return:
	*	data size add, <0 for error
	*/
	int add_data(const char *data, int sz);

	/*
	*	end entity data input
	*@return:
	*	0 for success, otherwise <0
	*/
	int end_data();

	/*
	*	check if entity has completed
	*@return:
	*	true for entity done, flase not done
	*/
	bool has_done() const;

private:
	//content length
	int _length;
	//content type
	std::string _type;
	//content language
	std::string _language;
	//content encoding
	std::string _encoding;
	//content ranage
	std::string _range;
	//content expires
	std::string _expires;

	//entity data stream
	data_stream _stream;
};
END_CUBE_HTTP_NS
