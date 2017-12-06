/*
*	io - input & output module
*/
#pragma once
#include "cube.h"
#include <list>
#include <Windows.h>

BEGIN_CUBE_NAMESPACE
//result for get completion queued status
class iores {
public:
	iores() : error(0), transfered(0), completionkey(0), overlapped(0) {}
	~iores() {}

	int error; // error code for error,0 means no error
	ulong transfered; // bytes transfered
	ulong completionkey; //compeltion key
	void *overlapped; //overlapped data
};

//io completion port class
class iocp {
	//iocp exceptions
	typedef std::exception ewarn;
	typedef std::exception efatal;

public:
	iocp();
	virtual ~iocp();
	
	/*
	*	open an iocp
	*/
	void open();

	/*
	*	bind a handle to the completion port
	*@param handle: in, handle to bind
	*@return:
	*	void
	*/
	void bind(HANDLE handle, ULONG_PTR key);

	/*
	*	pull queued status from completion port
	*@param waitmsec: in, wait time in million seconds for result completed
	*@return:
	*	true if completion result pulled, false when error and error code will return by @error
	*/
	iores pull(int waitmsec = -1);

	/*
	*	close iocp handle
	*/
	void close();

private:
	//handle of io complete port
	HANDLE _iocp;
};
END_CUBE_NAMESPACE
