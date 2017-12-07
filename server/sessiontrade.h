#pragma once
#include "stdsvr.h"
#include "cube\net.h"
BEGIN_SERVER_NAMESPACE
class sessiontrade : public cube::session {
public:
	sessiontrade();
	~sessiontrade();

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual int on_close();
};
END_SERVER_NAMESPACE
