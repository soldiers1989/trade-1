#pragma once
#include "stdsvr.h"
#include "cube\net.h"
BEGIN_SERVER_NAMESPACE
class sessionapi : public cube::session
{
public:
	sessionapi(SOCKET s, cube::uint ip, cube::uint port);
	virtual ~sessionapi();

	/*
	*	recalled when the connection has build, the @arg is the
	*parameter passed when the accepter started or specified by the
	*connector's connect method.
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_open(void *arg);

	/*
	*	recalled when the the data has send out, with send size @sz_send.
	*@param context: in, context of send opertation
	*@param transfered: in, data has transfered
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_send(cube::io_context *context, cube::uint transfered);

	/*
	*	recalled when the the @data with size @sz_recv has received.
	*@param context: in, context of receive opertation
	*@param transfered: in, data has transfered
	*return:
	*	0--success, other--failed, handler will be destroyed
	*/
	virtual int on_recv(cube::io_context *context, cube::uint transfered);

	/*
	*	recalled when the handler will be destroyed.
	*return:
	*	0--success, other--failed
	*/
	virtual int on_close();

private:
};
END_SERVER_NAMESPACE
