/*
*	cc - concurrence module
*/
#pragma once
#include <list>
#include <mutex>
#include <thread>
#include <atomic>
#include <chrono>
#include <vector>
#include <functional>
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

//timer class
class timer {
public:
	//task definiation
	using task = std::function<void(...)>;
	//clock using for timer
	using clock = std::chrono::system_clock;
	//million seconds
	using milliseconds = std::chrono::milliseconds;
	//time point in million seconds
	using timepoint = std::chrono::time_point<clock, milliseconds>;

	//timer item
	class item {
	public:
		item(int id, int delayms, task t) : id(id), delay(delayms), task(t), interval(-1), expire(std::chrono::time_point_cast<milliseconds>(std::chrono::system_clock::now()) + delay) {}
		item(int id, int delayms, int intervalms, task t) : id(id), delay(delayms), task(t), interval(intervalms), expire(std::chrono::time_point_cast<milliseconds>(std::chrono::system_clock::now()) + delay) {}
		~item() {}

		void update() {
		}



		int id; //item id
		task task; //item's task
		timepoint expire; //expire time point

		milliseconds delay; //delay in milliseconds
		milliseconds interval; //interval in milliseconds
	};

public:
	timer();
	~timer();

	void init(int executors = 1);

	int set(int delay, task t);

	int set(int delay, int interval, task t);

	void cancel(int id);

	void destroy();

private:
	void wait_expire();
	void run_expired();

	static void monitor(timer *tmr);
	static void execute(timer *tmr);

private:
	//next task item id
	int _nextid;
	
	//mutex for waiting expire items
	std::mutex _wmutex;
	//timer item list waiting for expire
	std::list<item> _witems;
	//condition variable for waiting expire
	std::condition_variable _wcond;

	//mutex for expired items
	std::mutex _emutex;
	//timer item expired waiting for execute
	std::list<item> _eitems;
	//condition variable for waiting execute
	std::condition_variable _econd;

	//stop flag for timer
	std::atomic<bool> _stop;

	//timer task wait monitor
	std::thread _monitor;

	//timer task expired executors
	std::vector<std::thread> _executors;

};
END_CUBE_NAMESPACE
