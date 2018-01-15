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
	sstream() : _data(""), _rpos(0), _wpos(0) {}
	virtual ~sstream() {}

	/*
	*	read data from stream
	*/
	int read(char *data, int sz);

	/*
	*	get/set string data of stream
	*/
	std::string &data() { return _data; }
	void data(const std::string &data) { _data = data; _rpos = 0; _wpos = _data.length(); }

	const std::string &cdata() const { return _data; }

protected:
	//data has taken
	std::string _data;

	//current read pos
	int _rpos;
	//current write pos
	int _wpos;
};

//sized string stream class
class sizedstream : public sstream{
public:
	sizedstream() : _size(INT_MAX) {}
	sizedstream(int size) : _size(size) {}
	virtual ~sizedstream() {}

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