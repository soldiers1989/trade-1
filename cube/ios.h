/*
*	ios - input output stream module
*/
#pragma once
#include "cube.h"
#include <string>
BEGIN_CUBE_NAMESPACE
//stream class
class stream {
public:
	stream() : _stream(0) {}
	stream(stream *stream) : _stream(stream) {}
	virtual ~stream() {
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
	const std::string &cdata();

	/*
	*	assign stream data
	*/
	void assign(const std::string &data);

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
	virtual const std::string &_cdata() = 0;

	/*
	*	assign stream data
	*/
	virtual void _assign(const std::string &data) = 0;

private:
	//source stream
	stream *_stream;
};

//string stream class
class stringstream : public stream {
public:
	stringstream() : _rpos(0) {}
	stringstream(stream *stream) : stream(stream), _rpos(0) {}
	virtual ~stringstream() {}

	int _put(const char *data, int sz);

	int _get(char *data, int sz);

	bool _endp() { return false; }

	bool _endg() { return _rpos == _data.length(); }

	int _size() { return _data.length(); }

	void _assign(const std::string &data) { _data = data; }

	const std::string &_cdata() { return _data; }

private:
	//string stream data
	std::string _data;

	//current read pos
	int _rpos;
};

//sized string stream class
class sizedstream : public stream {
public:
	sizedstream(int size) : _dsize(size), _rpos(0) {}
	virtual ~sizedstream() {}

	int _put(const char *data, int sz);

	int _get(char *data, int sz);

	bool _endp() { return _dsize == _data.length(); }

	bool _endg() { return _rpos == _data.length(); }

	int _size() { return _data.length(); }

	void _assign(const std::string &data) { _data = data; _dsize = _data.length(); }

	const std::string &_cdata() { return _data; }

private:
	//string stream data
	std::string _data;
	//stream data size
	int _dsize;

	//current read pos
	int _rpos;
};

//delimited string stream class
class delimitedstream : public stream {
public:
	delimitedstream(const std::string &delimiter) : _rpos(0), _full(false), _delimiter(delimiter), _dpos(0) {}
	virtual ~delimitedstream() {}

	int _put(const char *data, int sz);

	int _get(char *data, int sz);

	bool _endp() { return _full; }

	bool _endg() { return _rpos == _data.length(); }

	int _size() { return _data.length(); }

	void _assign(const std::string &data) { _data = data; _full = true; }

	const std::string &_cdata() { return _data; }

private:
	//stream data
	std::string _data;
	//current read pos
	int _rpos;
	//full flag for stream
	bool _full;

	//delimiter for stream
	std::string _delimiter;
	//delimiter pos to compare
	int _dpos;
};

//file stream class
class filestream : public stream{

};
END_CUBE_NAMESPACE
