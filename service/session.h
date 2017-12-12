#pragma once
#include "stdsvr.h"
#include "cube\net.h"
BEGIN_SERVICE_NAMESPACE
class ssquote : public cube::session {
public:
	ssquote() {}
	~ssquote() {}

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual int on_close();
};

class sstrade : public cube::session {
public:
	sstrade() {}
	~sstrade() {}

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual int on_close();
};

class ssmanage : public cube::session {
public:
	ssmanage() {}
	~ssmanage() {}

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual int on_close();
};

END_SERVICE_NAMESPACE
