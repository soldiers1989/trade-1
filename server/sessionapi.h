#pragma once
#include "stdsvr.h"
#include "cube\net.h"
BEGIN_SERVER_NAMESPACE
class sessionapi : public cube::session
{
public:
	sessionapi();
	virtual ~sessionapi();

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual int on_close();

private:
};
END_SERVER_NAMESPACE
