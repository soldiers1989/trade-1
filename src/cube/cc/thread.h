#pragma once
#include "cube\cc\task.h"
#include <list>
#include <mutex>
#include <thread>
BEGIN_CUBE_CC_NS
//thread to run task
class thread {
public:
	/*
	*	create a new thread object by a looper object
	*@param looper: in, looper object, it can be delay passed at @start method
	*/
	thread();
	virtual ~thread();

	/*
	*	start thread
	*@param task: in, task object to run
	*@return:
	*	void
	*/
	void start(task *task);


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
	//run task
	void run();

	//thread function to run task
	static void thread_func(thread *thd);

private:
	//task object to run
	task *_task;

	//thread object
	std::shared_ptr<std::thread> _thread;
};

//threads to run task
class threads {
public:
	threads();
	virtual ~threads();

	/*
	*	start threads to run a task
	*@param task: in, task object to run
	*@param nthread: in, thread number want to create
	*@return:
	*	void
	*/
	void start(task *task, int nthread = 1);

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
	std::list<std::thread::id> getids();

private:
	//threads to run the task
	std::list<std::shared_ptr<thread>> _threads;
};
END_CUBE_CC_NS
