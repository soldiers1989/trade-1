#pragma once
#include "cube\cc\looper.h"
#include <atomic>
BEGIN_CUBE_CC_NS
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
	class executor : task {
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

END_CUBE_CC_NS
