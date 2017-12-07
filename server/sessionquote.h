#pragma once
#include "stdsvr.h"
#include "cube\net.h"
BEGIN_SERVER_NAMESPACE
class sessionquote : public cube::session {
public:
	sessionquote();
	~sessionquote();

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual int on_close();
};
END_SERVER_NAMESPACE
