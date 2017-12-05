/*
*	io - input & output module
*/
#pragma once
#include "cube.h"
#include <list>

BEGIN_CUBE_NAMESPACE
//result for get completion queued status
typedef class iocp_res {
public:
	iocp_res() : error(0), transfered(0), completionkey(0), overlapped(0) {}
	~iocp_res() {}

	int error; // error code for error,0 means no error
	ulong transfered; // bytes transfered
	ulong completionkey; //compeltion key
	void *overlapped; //overlapped data
} iocp_res_t;

//io completion port class
class iocp {
public:
	iocp();
	virtual ~iocp();
	
	/*
	*	bind a handle to the completion port
	*@param handle: in, handle to bind
	*@return:
	*	void
	*/
	void bind(void *handle);

	/*
	*	unbind a handle from the completion port
	*@param handle: in, handle to unbind
	*@return:
	*	void
	*/
	void unbind(void *handle);

	/*
	*	pull queued status from completion port
	*@param waitsec: in, wait seconds for result completed
	*@return:
	*	true if completion result pulled, false when error and error code will return by @error
	*/
	iocp_res pull(int waitsec = -1);

private:
	//handle of io complete port
	void *_iocp;
};
END_CUBE_NAMESPACE
