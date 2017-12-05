#pragma once
#include "stdsvr.h"
#include "cube\net.h"
BEGIN_SERVER_NAMESPACE
class sessionapi : public cube::session
{
public:
	sessionapi(SOCKET s, cube::uint ip, cube::uint port);
	virtual ~sessionapi();

	virtual int on_open(void *arg);

	virtual int on_send(cube::io_context *context, cube::uint transfered);

	virtual int on_recv(cube::io_context *context, cube::uint transfered);

	virtual int on_close();

private:
};
END_SERVER_NAMESPACE
