#pragma once
#include "cube\cc\reactor.h"
BEGIN_CUBE_CC_NS
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
		cc::task *_task; //item's task

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

END_CUBE_CC_NS
