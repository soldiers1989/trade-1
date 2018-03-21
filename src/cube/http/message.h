#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
class message {
public:
	/*
	*	check if entity has completed
	*@return:
	*	true for entity done, flase not done
	*/
	virtual bool has_entity_done() const = 0;

	/*
	*	set message start line data
	*@param data: in, message start line
	*@return:
	*	0 for sucesss, otherwise <0
	*/
	virtual int set_start_line(const std::string &data) = 0;

	/*
	*	add message header line data
	*@param data: in message header line
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int add_header_line(const std::string &data) = 0;

	/*
	*	end header data input, so entity can be prepared
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int end_header_line() = 0;

	/*
	*	add message entity data
	*@param data: in, entiy data
	*@param sz: in, data size
	*@return:
	*	data size add, <0 for error
	*/
	virtual int add_entity_data(const char *data, int sz) = 0;

	/*
	*	end entity data input, so entity can be processed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int end_entity_data() = 0;
};
END_CUBE_HTTP_NS
