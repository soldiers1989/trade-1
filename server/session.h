#pragma once
#include "stdsvr.h"
#include "cube\net.h"
BEGIN_SERVICE_NAMESPACE
class ssquote : public cube::net::session {
public:
	ssquote() {}
	~ssquote() {}

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual void on_close();
};

class sstrade : public cube::net::session {
public:
	sstrade() {}
	~sstrade() {}

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual void on_close();
};

class ssmanage : public cube::net::session {
public:
	ssmanage() {}
	~ssmanage() {}

	virtual int on_open(void *arg);

	virtual int on_send(int transfered);

	virtual int on_recv(char *data, int transfered);

	virtual void on_close();
};

END_SERVICE_NAMESPACE
