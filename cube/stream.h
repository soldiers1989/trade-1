#pragma once
#include "cube.h"
#include <string>
BEGIN_CUBE_NAMESPACE
//stream class
class stream {
public:
	stream() : _completed(false) {}
	virtual ~stream() {}

	/*
	*	read data from stream
	*@param data: in/out, output data for write
	*@param sz: in, output buffer size
	*@return:
	*	data size read
	*/
	virtual int read(char *data, int sz) = 0;

	/*
	*	write data to stream
	*@param data: in, input data for read
	*@param sz: in, data size
	*@return:
	*	data size write
	*/
	virtual int write(const char* data, int sz) = 0;

	/*
	*	flag for indicating completed status of stream
	*/
	void complete(bool flag) { _completed = flag; }
	bool completed() { return _completed; }

private:
	//completed flag for stream
	bool _completed;

};

//string stream class
class sstream : public stream {
public:
	sstream() : _str("") {}
	virtual ~sstream() {}

	/*
	*	get string data of stream
	*/
	std::string &str() { return _str; }
	const std::string &c_str() const { return _str; }

protected:
	//data has taken
	std::string _str;
};

//sized string stream class
class sizedstream : public sstream{
public:
	sizedstream() : _size(INT_MAX) {}
	sizedstream(int size) : _size(size) {}
	virtual ~sizedstream() {}

	/*
	*	read data from stream
	*/
	int read(char *data, int sz);

	/*
	*	write data to stream
	*/
	int write(const char *data, int sz);

	/*
	*	set stream size
	*/
	void size(int sz) { _size = sz; }

private:
	//stream size
	int _size;
};

//delimited string stream class
class delimitedstream : public sstream {
public:
	delimitedstream(const std::string delimiter) : _delimiter(delimiter), _currpos(0) {}
	virtual ~delimitedstream() {}

	int read(char *data, int sz);
	int write(const char *data, int sz);

private:
	//delimiter for stream
	std::string _delimiter;

	//current pos to delimiter
	int _currpos;
};

//file streamer
class filestreamer {

};
END_CUBE_NAMESPACE