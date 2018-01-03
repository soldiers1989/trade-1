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
	typedef enum class status {starting = 0, runing = 1, stopped = 2} status;
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
class reactor : private task {
	//clock using for timer
	using clock = std::chrono::system_clock;
	//million seconds
	using milliseconds = std::chrono::milliseconds;
	//time point in million seconds
	using timepoint = std::chrono::time_point<clock>;

	//reactor item
	class item {
	public:
		item(int id, task *task);
		~item();
		
		bool operator ==(task *task);
		bool operator ==(int id);
		
		int id();

		void run();
		void join();

		void addref();
		void subref();
		bool pending();
		void pending(bool flag);
		const timepoint& ctime();

	private:
		int _id;
		task *_task;
		timepoint _ctime;

		volatile bool _pending;
		std::atomic_int _refcnt; //item reference count
	};

	//reactor items
	class items {
	public:
		items();
		~items();
		
		bool run();
		int add(task *task);
		void cancel(int id);
		void cancel(task *task);

		bool busy(int waitms);
	private:
		//mutex for items
		std::mutex _mutex;
		//current items in reactor
		std::list<item*> _items;
	};

	//executor of reactor
	class executor : task{
	public:
		executor();
		~executor();

		void start(items *items);

		void stop();

		void run();

		bool idle(int idlems);

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

	//executors for rector
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

	/*
	*	start reactor by specified max executors
	*@param max_executors: in, max executors
	*@return:
	*	void
	*/
	void start(int max_executors = 1);

	/*
	*	process task
	*@param task: in, react task
	*@return:
	*	void
	*/
	int react(task *task);

	/*
	*	cancel task by task id
	*param task: in, task
	*@return:
	*	void
	*/
	void cancel(int id);
	void cancel(task *task);

	/*
	*	stop reactor
	*@return:
	*	void
	*/
	void stop();

private:
	/*
	*	run by looper monitor
	*/
	void run();

	/*
	*	balance executors of reactor
	*/
	void balance();

private:
	//reactor items
	items _items;
	//monitor of reactor
	looper _monitor;
	//reactor executors
	executors _executors;

public:
	class default{
	public:
		/*
		*	process task
		*@param task: in, react task
		*@return:
		*	void
		*/
		static void react(task *task);

		/*
		*	cancel task by task id
		*param task: in, task
		*@return:
		*	void
		*/
		static void cancel(task *task);

	public:
		default();
		~default();
	};
};

//timer class
class timer : private task {
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
	*@param delayms: in, delay milliseconds for expire
	*@param intervalms: in, cycle interval in milliseonds
	*@param task: in, timer task
	*@return:
	*	timer task id
	*/
	int setup(int delayms, task *t);
	int setup(int delayms, int intervalms, task *t);

	/*
	*	cancel timer task by timer task id
	*@param id: in, timer task id
	*@return:
	*	void
	*/
	void cancel(int id);

	/*
	*	stop timer
	*/
	void stop();

private:
	//expire timer items
	void expire();

	/*
	*	run by looper monitor
	*/
	void run();
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

public:
	class default{
	public:
		/*
		*	setup timer task
		*@param delay: in, delay milliseconds for expire
		*@param interval: in, cycle interval in milliseonds
		*@param task: in, timer task
		*@return:
		*	timer task id
		*/
		static int setup(int delay, task *t);
		static int setup(int delay, int interval, task *t);

		/*
		*	cancel timer task by timer task id
		*@param id: in, timer task id
		*@return:
		*	void
		*/
		static void cancel(int id);

	public:
		default();
		~default();
	};
};

//crontab class
class crontab : private task {
	//local time
	class ltime {
	public:
		ltime();
		~ltime();

		//get current crontab time
		static ltime now();

		bool operator !=(const ltime &t);

	private:
		ltime(int sec, int min, int hour, int day, int month, int week);

	public:
		int sec;
		int min;
		int hour;
		int day;
		int month;
		int week;
	};

	//crontab time
	class ctime {
	public:
		ctime(int min, int hour, int day, int month, int week);
		~ctime();

		//compare with another crontab time
		bool operator ==(const ltime &t);

	private:
		int _min;
		int _hour;
		int _day;
		int _month;
		int _week;
	};

	//crontab task item
	class item {
	public:
		item(int id, task *task, int min, int hour, int day, int month, int week);
		~item();

		int id();
		void run();
		void join();
		void addref();
		void subref();
		bool expired(const ltime &now);
		void last_expire_time(const ltime &tm);

	private:
		int _id;
		task *_task;
		ctime _time;
		ltime _last_expire_time;
		std::atomic_int _refcnt;
	};

public:
	crontab();
	virtual ~crontab();

	static crontab * global();

	/*
	*	start crontab
	*@return:
	*	void
	*/
	void start();

	/*
	*	setup a crontab task
	*@param t: in, crontab task
	*@param min: in, minitue, [0~59]
	*@param hour: in, hour, [0~23]
	*@param day: in, day, [1~31]
	*@param month: in, month, [1~12]
	*@param week: in, week, [1~7]
	*@return:
	*	crontab task id
	*/
	int setup(task *t, int min, int hour, int day, int month, int week);

	/*
	*	cancel a crontab task by task id
	*@param id: in, crontab task id
	*@return:
	*	void
	*/
	void cancel(int id);

	/*
	*	stop crontab task
	*@return:
	*	void
	*/
	void stop();

private:
	/*
	*	execute expired task
	*/
	static void execute(std::shared_ptr<item> &item);

	/*
	*	expire task every seconds
	*/
	void expire();


	/*
	*	run for monitor
	*/
	void run();

private:
	//next crontab task id
	int _nextid;

	//monitor
	looper _monitor;

	//mutex for item list
	std::mutex _mutex;
	//timer item list of monitor
	std::list<std::shared_ptr<item>> _items;

public:
	class default{
	public:
		/*
		*	setup a crontab task
		*@param t: in, crontab task
		*@param min: in, minitue, [0~59]
		*@param hour: in, hour, [0~23]
		*@param day: in, day, [1~31]
		*@param month: in, month, [1~12]
		*@param week: in, week, [1~7]
		*@return:
		*	crontab task id
		*/
		static int setup(task *t, int min, int hour, int day, int month, int week);

		/*
		*	cancel a crontab task by task id
		*@param id: in, crontab task id
		*@return:
		*	void
		*/
		static void cancel(int id);

	public:
		default();
		~default();
	};
};
END_CUBE_NAMESPACE
