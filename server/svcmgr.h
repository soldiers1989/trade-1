#pragma once
#include "stdsvr.h"
#include "cube\svr.h"
BEGIN_SVR_NAMESPACE
BEGIN_MGR_NAMESPACE
//manager login
class login : public cube::http::servlet {
public:
	void handle(const cube::http::request &req, cube::http::response &resp);
};

//manager logout
class logout : public cube::http::servlet {
public:
	void handle(const cube::http::request &req, cube::http::response &resp);
};

//add account
class add_account : public cube::http::servlet {
public:
	void handle(const cube::http::request &req, cube::http::response &resp);
};

//get account
class get_account : public cube::http::servlet {
public:
	void handle(const cube::http::request &req, cube::http::response &resp);
};

//del account
class del_account : public cube::http::servlet {
public:
	void handle(const cube::http::request &req, cube::http::response &resp);
};

//modify account
class mod_account : public cube::http::servlet {
public:
	void handle(const cube::http::request &req, cube::http::response &resp);
};

//manage service class
class service {
public:
	/*mount manage servlet*/
	class servlet{
	public:
		servlet(const std::string &method, const std::string &path, cube::http::servlet *servlet) {
			service::mount(method, path, servlet);
		}
		~servlet() {}
	};

public:
	/*
	*	start manage service
	*@return:
	*	0 for success, otherwise <0
	*/
	static int start();

	/*
	*	stop manage service
	*@return:
	*	void
	*/
	static void stop();

	/*
	*	mount new servlet to service
	*@param method: in, http method
	*@param path: in, service path
	*@param servlet: in, servlet for path
	*@return:
	*	void
	*/
	static void mount(const std::string &method, const std::string &path, cube::http::servlet *servlet);

private:
	//http server
	static cube::http::server server;
	//servlets registered for http server
	static cube::http::applet applet;
};
END_MGR_NAMESPACE
END_SVR_NAMESPACE
