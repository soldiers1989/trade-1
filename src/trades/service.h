#pragma once
#include "cube\http\applet.h"
#include "cube\svc\http_server.h"
//manage service class
class service {
public:
	/*mount manage servlet*/
	class mount_servlet {
	public:
		mount_servlet(const std::string &method, const std::string &path, cube::http::servlet *servlet) {
			service::mount(method, path, servlet);
		}
		~mount_servlet() {}
	};

public:
	/*
	*	start manage service
	*@return:
	*	0 for success, otherwise <0
	*/
	static int start();

	/*
	*	wait for exist
	*/
	static void wait();

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
	//servlets registered for http server
	static cube::http::applet applet;

	//http server
	static cube::svc::http_server server;
};