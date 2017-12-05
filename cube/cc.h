/*
*	cc - concurrence module
*/
#pragma once
#include <mutex>
#include <thread>
#include <vector>
#include "cube.h"

BEGIN_CUBE_NAMESPACE
//runnable class for thread/threads
class runnable {
public:
	runnable() {}
	virtual ~runnable() {}

	/*
	*	thread function to do something
	*/
	virtual void run() = 0;
};

//thread 
class thread {
public:
	/*
	*	create a new thread object by a runnable object
	*@param runnable: in, runnable object, it can be delay passed at @start method
	*/
	thread();
	thread(runnable *runnable);
	virtual ~thread();

	/*
	*	start thread
	*@param error: out, error message when start thread failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(std::string *error = 0);

	/*
	*	start thread
	*@param runnable: in, runnable object
	*@param error: out, error message when start thread failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(runnable *runnable, std::string *error = 0);

	/*
	*	detach thread from create thread
	*@return:
	*	void
	*/
	void detach();

	/*
	*	wait for thread exit
	*@return:
	*	void
	*/
	void join();

	/*
	*	get thread id
	*@return:
	*	thread id
	*/
	std::thread::id getid();

private:
	/*
	*	thread function
	*/
	static unsigned __stdcall thread_func(void *arg);

private:
	//thread object
	std::thread _thread;

	//runnable object
	runnable *_runnable;
};

//thread pool
class threads {
public:
	/*
	*	create a new threads object by a runnable object
	*@param runnable: in, runnable object, it can be delay passed at @start method
	*/
	threads();
	threads(runnable *runnable);
	virtual ~threads();

	/*
	*	start thread pool
	*@param nthread: in, thread number want to create
	*@param error: out, error message when start threads failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(int nthread, std::string *error = 0);

	/*
	*	start thread pool
	*@param runnable: in, runnable object, replace object passed by constructor if not null
	*@param nthread: in, thread number want to create
	*@param error: out, error message when start threads failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int start(runnable *runnable, int nthread, std::string *error = 0);

	/*
	*	detach threads from create thread
	*@return:
	*	void
	*/
	void detach();

	/*
	*	wait for threads exit
	*@return:
	*	void
	*/
	void join();

	/*
	*	get thread id
	*@return:
	*	thread id
	*/
	std::vector<std::thread::id> getids();

private:
	//thread objects
	std::vector<thread*> _threads;

	//runnable object
	runnable *_runnable;
};
END_CUBE_NAMESPACE
