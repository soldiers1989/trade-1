#pragma once
#include "cube.h"
#include <string>
BEGIN_CUBE_NAMESPACE

//piped stream class
class pipedstream {
public:
	pipedstream() : _stream(0) {}
	pipedstream(pipedstream *pstream) : _stream(pstream) {}
	virtual ~pipedstream() {
		if (_stream != 0) {
			delete _stream;
			_stream = 0;
		}
	}

	/*
	*	put data into stream
	*@param data: in, data to put
	*@param sz: in, data size
	*@return:
	*	data size put into stream
	*/
	int put(const char *data, int sz);

	/*
	*	get data from stream
	*@param data: in/out, output buffer
	*@param sz: in, output buffer size
	*@return:
	*	data size get from stream
	*/
	int get(char *data, int sz);

	/*
	*	test if end of put, means no more data could be putting into stream
	*@return:
	*	bool
	*/
	bool endp();

	/*
	*	test if end of get, means no more data could be getting from stream
	*@return:
	*	bool
	*/
	bool endg();

	/*
	*	get stream data size
	*@return:
	*	data size in bytes
	*/
	int size();

	/*
	*	get stream data
	*@return:
	*	stream data
	*/
	const char *data();

protected:
	/*
	*	put data into stream
	*@param data: in, data to put
	*@param sz: in, data size
	*@return:
	*	data size put into stream
	*/
	virtual int _put(const char *data, int sz) = 0;

	/*
	*	get data from stream
	*@param data: in/out, output buffer
	*@param sz: in, output buffer size
	*@return:
	*	data size get from stream
	*/
	virtual int _get(char *data, int sz) = 0;

	/*
	*	test if end of put, means no more data could be putting into stream
	*@return:
	*	bool
	*/
	virtual bool _endp() = 0;

	/*
	*	test if end of get, means no more data could be getting from stream
	*@return:
	*	bool
	*/
	virtual bool _endg() = 0;

	/*
	*	get stream data size
	*@return:
	*	data size in bytes
	*/
	virtual int _size() = 0;

	/*
	*	get stream data
	*@return:
	*	stream data
	*/
	virtual const char *_data() = 0;

private:
	//source stream
	pipedstream *_stream;
};

//string stream class
class stringstream : public pipedstream{
public:
	stringstream() : pipedstream(){}
	stringstream(pipedstream *pstream) : pipedstream(pstream) {}
	virtual ~stringstream() {}

private:
	//string stream
};

//stream class
class stream {
public:
	stream() : _full(false) {}
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
	*	get / set stream full flag
	*/
	bool full() { return _full; }
	void full(bool flag) { _full = flag; }

	/*
	*	get / set stream end flag
	*/
	bool ends() { return _ends; }
	void ends(bool flag) { _ends = flag; }

private:
	//stream full flag
	bool _full;
	//stream ends flag
	bool _ends;
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
class filestream {

};
END_CUBE_NAMESPACE