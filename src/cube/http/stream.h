#pragma once
#include <fstream>
#include <sstream>
#include "cube\type.h"

BEGIN_CUBE_HTTP_NS
//stream interface
class stream {
public:
	/*
	*	open stream
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int open() = 0;

	/*
	*	read data from stream
	*@param data: in/out, output buffer
	*@param sz: in, output buffer size
	*@return:
	*	data size read from stream
	*/
	virtual size_t read(char *data, size_t sz) = 0;

	/*
	*	write data into stream
	*@param data: in, data to write
	*@param sz: in, data size
	*@return:
	*	data size write into stream
	*/
	virtual size_t write(const char *data, size_t sz) = 0;

	/*
	*	set the next read position in stream
	*@param pos: in, read position in stream
	*@return:
	*	current read position
	*/
	virtual size_t seekr(size_t pos) = 0;

	/*
	*	set the next write position in stream
	*@param pos: in, write position in stream
	*@return:
	*	current write position
	*/
	virtual size_t seekw(size_t pos) = 0;

	/*
	*	tell the current read postion of stream
	*@return:
	*	current read postion of stream
	*/
	virtual size_t tellr() const = 0;

	/*
	*	tell the current write postion of stream
	*@return:
	*	current write postion of stream
	*/
	virtual size_t tellw() const = 0;

	/*
	*	test if current read position is at stream end
	*@return:
	*	bool
	*/
	virtual bool endr() const = 0;

	/*
	*	test if test if current write position is at stream end
	*@return:
	*	bool
	*/
	virtual bool endw() const = 0;

	/*
	*	test if stream is full
	*@return:
	*	bool
	*/
	virtual bool full() const = 0;

	/*
	*	test if stream is empty
	*@return:
	*	bool
	*/
	virtual bool empty() const = 0;

	/*
	*	get stream data size
	*@return:
	*	data size in bytes
	*/
	virtual size_t size() const = 0;

	/*
	*	flush stream data to output
	*@return:
	*	void
	*/
	virtual void flush() = 0;

	/*
	*	close stream
	*@return:
	*	void
	*/
	virtual void close() = 0;

	/*
	*	get stream data
	*@return:
	*	stream data
	*/
	virtual std::string data() = 0;
};

//data stream
class data_stream : public stream {
public:
	data_stream(size_t msz = MAXSZ) : _rpos(0), _wpos(0), _msz(msz), _data(""){}
	data_stream(const std::string &data, size_t msz = MAXSZ) : _rpos(0), _msz(msz), _data(data) {
		_wpos = data.length();
	}
	virtual ~data_stream() {}
	
	int open();

	size_t read(char *data, size_t sz);

	size_t write(const char *data, size_t sz);

	size_t seekr(size_t pos);

	size_t seekw(size_t pos);

	size_t tellr() const;

	size_t tellw() const;

	bool endr() const;

	bool endw() const;

	bool full() const;

	bool empty() const;

	size_t size() const;

	void flush();

	void close();

	std::string data();

private:
	//current read pos
	size_t _rpos;
	//current write pos
	size_t _wpos;
	//max stream data size
	size_t _msz;

	//stream data
	std::string _data;
};

//file stream
class file_stream : public stream {
public:
	file_stream(const std::string &path, int mode = std::ios_base::in | std::ios_base::out) : _rpos(0), _wpos(0), _csz(0), _msz(MAXSZ), _path(""), _file(path, mode) {
	}

	file_stream(const std::string &path, size_t msz, int mode = std::ios_base::in | std::ios_base::out) : _rpos(0), _wpos(0), _csz(0), _msz(msz), _path(""), _file(path, mode) {
	}

	virtual ~file_stream() {}

	int open();

	size_t read(char *data, size_t sz);

	size_t write(const char *data, size_t sz);

	size_t seekr(size_t pos);

	size_t seekw(size_t pos);

	size_t tellr() const;

	size_t tellw() const;

	bool endr() const;

	bool endw() const;

	bool full() const;

	bool empty() const;

	size_t size() const;

	void flush();

	void close();

	std::string data();

private:
	size_t _size();

private:
	//current read pos
	size_t _rpos;
	//current write pos
	size_t _wpos;
	//current file size
	size_t _csz;
	//max file size limit
	size_t _msz;

	//file path
	std::string _path;
	//file stream
	std::fstream _file;
};
END_CUBE_HTTP_NS
