#pragma once
#include "cube.h"
#include <list>
#include <mutex>
#include <atomic>
#include <chrono>
#include <thread>
#include <algorithm>
BEGIN_CUBE_NAMESPACE
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
		mitem(int id, int delay, task *task): _id(id), _delay(delay), _task(task), _cycle(false), _interval(-1) {
			_expire = clock::now() + _delay;
		}

		mitem(int id, int delay, int interval, task *task) : _id(id), _delay(delay), _interval(interval), _task(task), _cycle(true) {
			_expire = clock::now() + _delay;
		}

		~mitem() {

		}
		
		inline int id() {
			return _id;
		}

		inline bool cycled() {
			return _cycle;
		}
		
		inline task* gettask() {
			return _task;
		}

		inline void reset() {
			_expire = _expire + _interval;
		}

		inline const timepoint& expire() {
			return _expire;
		}

		bool expired(std::chrono::time_point<clock> now = clock::now()) {
			return !(_expire > now);
		}

		inline milliseconds latency(std::chrono::time_point<clock> now = clock::now()) {
			return std::chrono::duration_cast<milliseconds>(_expire - now);
		}

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
		eitem(int id, task *task) : _id(id), _task(task) {
			_status.store((int)status::pending);
		}
		~eitem() {}

		void run() {
			_status.store((int)status::running);
			_task->run();
			_status.store((int)status::finished);
		}

		void join() {
			while(_status.load() != (int)status::finished)
				std::this_thread::yield();
		}

		bool pending() {
			return _status.load() == (int)status::pending;
		}

		void waiting() {
			_status.store((int)status::waiting);
		}

		inline int id() {
			return _id;
		}

	private:
		int _id;
		task *_task;

		std::atomic<int> _status; //item status
	};

	//timer task executor
	class executor {
	public:
		executor() {}
		~executor() {}

		int start(int maxthreads = 1) {
			_stop.store(false);
			for (int i = 0; i<maxthreads; i++)
				_threads.push_back(std::shared_ptr<std::thread>(new std::thread(executor_thread_func, this)));
			return 0;
		}

		void execute(int id, task *task) {
			std::lock_guard<std::mutex> lck(_mutex);
			_items.push_back(std::shared_ptr<eitem>(new eitem(id, task)));
		}

		void cancel(int id) {
			std::lock_guard<std::mutex> lck(_mutex);
			std::list<std::shared_ptr<eitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<eitem> item) {return id == item->id(); });
			if (iter != _items.end()) {
				if ((*iter)->pending()) {
					_items.erase(iter);
				} else {
					(*iter)->join();
				}
			}
		}

		void balance() {

		}

		void stop() {
			_stop.store(true);
			std::for_each(_threads.begin(), _threads.end(), [](std::shared_ptr<std::thread> thd) {thd->join(); });
			_threads.clear();
		}

	private:
		//execute timer tasks
		void execute() {
			while (!_stop.load()) {
				std::shared_ptr<eitem> nextitem = nullptr;
				{
					std::lock_guard<std::mutex> lck(_mutex);
					std::list<std::shared_ptr<eitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [](std::shared_ptr<eitem> item) {return item->pending(); });
					if (iter != _items.end()) {
						nextitem = *iter;
						nextitem->waiting();
					}
				}

				if (nextitem != nullptr) {
					nextitem->run();
					{
						int id = nextitem->id();
						std::lock_guard<std::mutex> lck(_mutex);
						std::list<std::shared_ptr<eitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<eitem> item) {return id == item->id(); });
						if (iter != _items.end()) {
							_items.erase(iter);
						}
					}
				} else {
					std::this_thread::yield();
				}
			}
		}

		//executor thread function
		static void executor_thread_func(executor *e) {
			e->execute();
		}

	private:
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
