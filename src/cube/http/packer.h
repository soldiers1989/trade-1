#pragma once
#include "cube\ns.h"
#include "cube\http\request.h"
#include "cube\http\response.h"
BEGIN_CUBE_HTTP_NS
class packer {
public:
	virtual int pack() = 0;

	/*
	*	take data from stream
	*@param data: in/out, data take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	virtual int take(char *data, int sz) = 0;
};

//http response stream
class response_stream_packer : public packer {
public:
	response_stream_packer() {}
	virtual ~response_stream_packer() {}

	int pack();

	/*
	*	take data from response buffer
	*@param data: in/out, data to take to
	*@param sz: in, data size
	*@return:
	*	size taked
	*/
	int take(char *data, int sz);

public:
	http::response &response() { return _response; }

private:
	//response object
	http::response _response;
};
END_CUBE_HTTP_NS
