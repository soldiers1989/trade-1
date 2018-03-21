#pragma once
#include "cube\cc\task.h"
#include <list>
#include <mutex>
#include <thread>
BEGIN_CUBE_CC_NS
//looper for task
class looper {
	typedef enum class status { starting = 0, runing = 1, stopped = 2 } status;
public:
	looper();
	virtual ~looper();

	/*
	*	start loop a task
	*@param task: in, loop task
	*@return:
	*	void
	*/
	void start(task *task);

	/*
	*	stop loop task
	*@return:
	*	void
	*/
	void stop();

private:
	//loop for task
	void loop();
	//thread function of looper
	static void loop_thread_func(looper *looper);

private:
	//loop task
	task *_task;

	//stop flag for loop task
	volatile bool _stop;
	//loopper status
	volatile status _status;
	//thread to execute loop task
	std::shared_ptr<std::thread> _thread;
};

//loopers to run task
class loopers {
public:
	loopers();
	virtual ~loopers();

	/*
	*	start loopers to run a task
	*@param task: in, loop task
	*@return:
	*	void
	*/
	void start(task *task, int nloopers);

	/*
	*	stop loopers
	*@return:
	*	void
	*/
	void stop();

private:
	//loopers
	std::list<std::shared_ptr<looper>> _loopers;
};

END_CUBE_CC_NS
