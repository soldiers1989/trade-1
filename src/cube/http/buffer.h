#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
//data buffer
class buffer {
public:
	/*
	*	get data from buffer
	*@param data: in/out, output buffer for data
	*@param sz: in/out, output buffer size
	*@return:
	*	size get
	*/
	virtual int get(char *data, int sz) = 0;

	/*
	*	put data to buffer
	*@param data: in, data to put
	*@param sz: in, data size
	*@return:
	*	size put
	*/
	virtual int put(const char *data, int sz) = 0;

	/*
	*	check buffer full status
	*@return:
	*	true for full
	*/
	virtual bool full() const = 0;

	/*
	*	clear buffer
	*/
	virtual void clear() = 0;

	/*
	*	buffer data size
	*/
	virtual int size() const = 0;

	/*
	*	buffer data
	*/
	virtual const char *data() const = 0;
};

//carriage return/line buffer
class line_buffer : public buffer{
public:
	line_buffer() : _data("") {}
	virtual ~line_buffer() {}

	int get(char *data, int sz);

	int put(const char *data, int sz);

	bool full() const;
	
	int size() const;

	void clear();

	const char *data() const;
	std::string line() const;
private:
	//carriage line data, not include 
	std::string _data;
};
END_CUBE_HTTP_NS
