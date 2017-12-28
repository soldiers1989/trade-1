/*
*	cc - concurrence module
*/
#pragma once
#include <map>
#include <list>
#include <mutex>
#include <thread>
#include <atomic>
#include <chrono>
#include "cube.h"

BEGIN_CUBE_NAMESPACE
//runnable task
class task {
public:
	virtual void run() = 0;
};

//looper for task
class looper{
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

//reactor class
class reactor : task {
	//clock using for timer
	using clock = std::chrono::system_clock;
	//million seconds
	using milliseconds = std::chrono::milliseconds;
	//time point in million seconds
	using timepoint = std::chrono::time_point<clock>;

	//reactor item
	class item {
		typedef enum class status { pending = 0, waiting = 1, running = 2, finished = 3 }status;
	public:
		item(int id, task *task);
		~item();

		int id();
		void run();
		void join();

		void waiting();
		bool pending();
		bool finished();

		const timepoint& ctime();
	private:
		int _id;
		task *_task;
		timepoint _ctime;

		std::atomic<int> _status; //item status
	};

	//reactor items
	class items {
	public:
		items();
		~items();

		void add(int id, task *task);
		void del(int id);
		bool run_next(int &id);
		bool busy();
	private:
		//mutex for items
		std::mutex _mutex;
		//current items in reactor
		std::list<std::shared_ptr<item>> _items;
	};

	//executor of reactor
	class executor : task{
	public:
		executor();
		~executor();

		void start(items *items);

		void stop();

		void run();

		bool idle();

	private:
		//looper
		looper _looper;
		//items
		items *_items;
		//idle flag
		volatile bool _idle_flag;
		//idle timepoint
		timepoint _last_idle_time;
	};

	class executors {
	public:
		executors();
		~executors();

		void start(int max_executors, items *items);

		void stop();

		void balance();

	private:
		//items
		items *_items;
		//max executors limit
		int _max_executors;
		//mutex for executors
		std::mutex _mutex;
		//current executors in reactor
		std::list<std::shared_ptr<executor>> _executors;
	};

public:
	reactor();
	virtual ~reactor();

	void start(int max_executors = 1);

	void react(int id, task *task);

	void cancel(int id);

	void stop();

	void balance();

	void run();
private:
	//reactor items
	items _items;
	//reactor executors
	executors _executors;
	//monitor of reactor
	looper _monitor;
};

//timer class
class timer : task {
private:
	//clock using for timer
	using clock = std::chrono::system_clock;
	//million seconds
	using milliseconds = std::chrono::milliseconds;
	//time point in million seconds
	using timepoint = std::chrono::time_point<clock>;

	//timer item
	class item {
	public:
		item(int id, int delay, task *task);
		item(int id, int delay, int interval, task *task);
		~item();

		int id();
		bool cycled();
		task* task();
		
		void reset();
		const timepoint& expire();
		bool expired(std::chrono::time_point<clock> now = clock::now());
		milliseconds latency(std::chrono::time_point<clock> now = clock::now());

	private:
		int _id; //item id
		bool _cycle; //cycle task flag
		cube::task *_task; //item's task

		timepoint _expire; //next expire time point

		milliseconds _delay; //delay in milliseconds
		milliseconds _interval; //interval in milliseconds
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
	void start(int max_executors = 1);

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

	void run();
private:
	//expire timer items
	void expire();

private:
	//next task item id
	int _nextid;

	//relate timer
	reactor _reactor;

	//monitor
	looper _monitor;

	//mutex for item list
	std::mutex _mutex;
	//timer item list of monitor
	std::list<std::shared_ptr<item>> _items;
	//condition variable of monitor
	std::condition_variable _cond;
};
END_CUBE_NAMESPACE
