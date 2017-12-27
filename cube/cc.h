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
	//timer task
	class task {
	public:
		virtual void run() {}
	};

private:
	//clock using for timer
	using clock = std::chrono::system_clock;
	//million seconds
	using milliseconds = std::chrono::milliseconds;
	//time point in million seconds
	using timepoint = std::chrono::time_point<clock>;

	//timer monitor item
	class mitem {
	public:
		mitem(int id, int delay, task *task);
		mitem(int id, int delay, int interval, task *task);
		~mitem();

		int id();
		bool cycled();
		task* gettask();
		
		void reset();
		const timepoint& expire();
		bool expired(std::chrono::time_point<clock> now = clock::now());
		milliseconds latency(std::chrono::time_point<clock> now = clock::now());

	private:
		int _id; //item id
		bool _cycle; //cycle task flag
		task *_task; //item's task

		timepoint _expire; //next expire time point

		milliseconds _delay; //delay in milliseconds
		milliseconds _interval; //interval in milliseconds
	};

	//timer executor item
	class eitem {
		typedef enum class status { pending = 0, waiting = 1, running = 2, finished = 3 }status;

	public:
		eitem(int id, task *task);
		~eitem();

		int id();

		void run();
		void join();

		bool pending();
		void waiting();

	private:
		int _id;
		task *_task;
		char *_dummy;
		std::atomic<int> _status; //item status
	};

	//timer task executor
	class executor {
	public:
		executor();
		~executor();

		int start(int maxthreads = 1);
		void execute(int id, task *task);
		void cancel(int id);
		void stop();

	private:
		//balance exector threads
		void balance();
		//execute timer tasks
		void execute();
		//executor thread function
		static void executor_thread_func(executor *e);

	private:
		//max threads of executor limit
		int _maxthreads;
		//stop flag for executor
		std::atomic<bool> _stop;
		//task execute threads
		std::list<std::shared_ptr<std::thread>> _threads;

		//mutex for item list
		std::mutex _mutex;
		//timer item to be executing
		std::list<std::shared_ptr<eitem>> _items;
		//condition variable of executor
		std::condition_variable _cond;
	};

public:
	timer();
	~timer();

	/*
	*	start timer with max executor threads
	*@param maxethreads: in, max executor threads
	*@return:
	*	void
	*/
	void start(int maxethreads = 1);

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
	*	stop monitor
	*/
	void stop();

private:
	//expire timer items
	void expire();

	//monitor thread function
	static void monitor_thread_func(timer *m);

private:
	//next task item id
	int _nextid;

	//relate timer
	executor _executor;

	//stop flag for timer
	std::atomic<bool> _stop;
	//task expire monitor
	std::shared_ptr<std::thread> _monitor;

	//mutex for item list
	std::mutex _mutex;
	//timer item list of monitor
	std::list<std::shared_ptr<mitem>> _items;
	//condition variable of monitor
	std::condition_variable _cond;
};
END_CUBE_NAMESPACE
