#pragma once
#include "cube\cc\task.h"
#include "cube\cc\looper.h"
#include <list>
#include <mutex>
#include <atomic>
BEGIN_CUBE_CC_NS
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
END_CUBE_CC_NS
