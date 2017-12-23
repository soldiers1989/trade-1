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

//runnable task
class task {
public:
	task() {}
	virtual ~task() {}

	virtual void run() = 0;
};

//clock using for timer
using clock = std::chrono::system_clock;
//million seconds
using milliseconds = std::chrono::milliseconds;
//time point in million seconds
using timepoint = std::chrono::time_point<clock, milliseconds>;

//timer task
class timertask : public task {
public:
	timertask(int id, int delayms, task *t) : id(id), delay(delayms), task(t), cycle(false), interval(0), waited(false), canceled(false) {
		expire = std::chrono::time_point_cast<milliseconds>(clock::now() + delay);
	}
	timertask(int id, int delayms, int intervalms, task *t) : id(id), delay(delayms), task(t), cycle(true), interval(intervalms), waited(false), canceled(false) {
		expire = std::chrono::time_point_cast<milliseconds>(clock::now() + delay);
	}
	~timertask() {}

	virtual void run() {
		task->run();
	}

	/*
	*	get expire latency time
	*/
	inline milliseconds latency(std::chrono::time_point<clock> now = clock::now()) {
		return std::chrono::duration_cast<milliseconds>(expire - now);
	}

	/*
	*	reset timer item
	*/
	inline void reset(std::chrono::time_point<clock> now = clock::now()) {
		if (cycle) {
			waited = false;
			expire = std::chrono::time_point_cast<milliseconds>(now + interval);
		}
	}

	/*
	*	set wait flag, so we known it has waited by monitor when canceled
	*/
	inline void wait() {
		waited = true;
	}
	inline void wait(bool flag) {
		waited = flag;
	}

	/*
	*	set cancel timer task flag, so we can cancel the task when monitor wake up
	*/
	inline void cancel() {
		canceled = true;
	}

public:
	int id; //item id
	bool cycle; //cycle task flag
	task *task; //item's task
	timepoint expire; //expire time point

	milliseconds delay; //delay in milliseconds
	milliseconds interval; //interval in milliseconds

	volatile bool waited; //waited flag by monitor
	volatile bool canceled; //cancel flag
};


//timer class
class timer {
public:
	timer();
	~timer();

	/*
	*	start timer with specified thread, default 1 thread
	*@return:
	*	void
	*/
	void start(int nthread = 1);

	/*
	*	setup timer task
	*@param delay: in, delay milliseconds for expire
	*@param task: in, timer task
	*@param interval: in, cycle timer task interval
	*@return:
	*	timer task id
	*/
	int setup(int delay, task *t);
	int setup(int delay, int interval, task *t);

	/*
	*	cancel timer task by timer task id
	*@param id: in, timer task id
	*@return:
	*	void
	*/
	void cancel(int id);

	/*
	*	stop timer
	*@return:
	*	void
	*/
	void stop();

private:
	/*
	*	expire the timer task
	*@return:
	*	void
	*/
	void expire();

	/*
	*	timer task monitor thread function
	*@param tmr: in, timer object to monitor
	*@return:
	*	void
	*/
	static void monitor(timer *tmr);
private:
	//next task item id
	int _nextid;
	
	//stop flag for timer
	std::atomic<bool> _stop;
	//timer task wait monitor
	std::list<std::shared_ptr<std::thread>> _monitors;

	//mutex for waiting expire items
	std::mutex _mutex;
	//timer item list waiting for expire
	std::list<std::shared_ptr<timertask>> _tasks;
	//condition variable for waiting expire
	std::condition_variable _cond;
};
END_CUBE_NAMESPACE
