#pragma once
#include "admin.h"
#include "cube\net.h"
BEGIN_SERVICE_NAMESPACE

class servlet_login : public cube::http::servlet {
public:
	int handle_get(const cube::http::request &req, cube::http::response &resp);
	int handle_post(const cube::http::request &req, cube::http::response &resp);
};

class service_manager {
public:
	virtual ~service_manager() {}

	/*
	*	get service manager instance
	*@return:
	*	service manager instance
	*/
	static service_manager *instance();

	/*
	*	start manage service on specified port
	*@param port: in, local http service port
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(ushort port);

	/*
	*	stop manage service
	*@return:
	*	void
	*/
	void stop();

private:
	//only allow singleton instance
	service_manager() {}

private:
	//service manger instance
	static service_manager *_instance;

	//http server
	cube::http::server _server;
	//servlets registered for http server
	cube::http::servlets _servlets;
};
END_SERVICE_NAMESPACE
