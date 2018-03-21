#include "cube\cc\crontab.h"
#include <future>
#include <algorithm>
BEGIN_CUBE_CC_NS
//////////////////////////////////crontab class///////////////////////////////////
crontab::ltime::ltime() {

}

crontab::ltime::ltime(int sec, int min, int hour, int day, int month, int week) : sec(sec), min(min), hour(hour), day(day), month(month), week(week) {

}

crontab::ltime::~ltime() {

}

crontab::ltime crontab::ltime::now() {
	time_t t = ::time(0);
	struct tm* now = ::localtime(&t);

	return crontab::ltime(now->tm_sec, now->tm_min, now->tm_hour, now->tm_mday, now->tm_mon + 1, now->tm_wday == 0 ? 7 : now->tm_wday);
}

bool crontab::ltime::operator!=(const ltime &t) {
	bool res = false;

	res = res || (min != t.min);
	res = res || (hour != t.hour);
	res = res || (day != t.day);
	res = res || (month != t.month);
	res = res || (week != t.week);

	return res;
}

crontab::ctime::ctime(int min, int hour, int day, int month, int week) : _min(min), _hour(hour), _day(day), _month(month), _week(week) {

}

crontab::ctime::~ctime() {

}

bool crontab::ctime::operator==(const ltime &t) {
	bool res = true;

	res = res && (_min < 0 || _min == t.min);
	res = res && (_hour < 0 || _hour == t.hour);
	res = res && (_day < 0 || _day == t.day);
	res = res && (_month < 0 || _month == t.month);
	res = res && (_week < 0 || _week == t.week);

	return res;
}

crontab::item::item(int id, task *task, int min, int hour, int day, int month, int week) : _id(id), _task(task), _time(min, hour, day, month, week), _refcnt(0), _last_expire_time(ltime::now()) {

}

crontab::item::~item() {

}

int crontab::item::id() {
	return _id;
}

void crontab::item::run() {
	_task->run();
	subref();
}

void crontab::item::join() {
	while (_refcnt.load() != 0) {
		std::this_thread::sleep_for(std::chrono::milliseconds(50));
	}
}

void crontab::item::addref() {
	_refcnt.fetch_add(1);
}

void crontab::item::subref() {
	_refcnt.fetch_sub(1);
}

bool crontab::item::expired(const ltime &now) {
	return _time == now && _last_expire_time != now;
}

void crontab::item::last_expire_time(const ltime &tm) {
	_last_expire_time = tm;
}

crontab::crontab() : _nextid(0) {
}

crontab::~crontab() {
}

void crontab::start() {
	_monitor.start(this);
}

int crontab::setup(task *t, int min, int hour, int day, int month, int week) {
	std::lock_guard<std::mutex> lck(_mutex);
	_items.push_back(std::shared_ptr<item>(new item(_nextid, t, min, hour, day, month, week)));
	return _nextid++;
}

void crontab::cancel(int id) {
	std::lock_guard<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), ([id](std::shared_ptr<item> &item) {return item->id() == id; }));
	if (iter != _items.end()) {
		(*iter)->join();
		_items.erase(iter);
	}
}

void crontab::stop() {
	//stop monitor
	_monitor.stop();

	//wait all running items to stop
	std::for_each(_items.begin(), _items.end(), [](std::shared_ptr<item> &item) { item->join();	});
	_items.clear();
}

void crontab::execute(std::shared_ptr<item> &item) {
	item->run();
}

void crontab::expire() {
	{
		std::lock_guard<std::mutex> lck(_mutex);
		ltime now = ltime::now();
		std::for_each(_items.begin(), _items.end(), [now](std::shared_ptr<item> &item) {
			if (item->expired(now)) {
				//add new thread reference
				item->addref();

				//start new thread to execute task
				std::async(execute, item);

				//set last expired time point
				item->last_expire_time(now);
			}
		});
	}

	std::this_thread::sleep_for(std::chrono::seconds(1));
}

void crontab::run() {
	expire();
}

///////////////////////global crontab object///////////////////
static crontab _g_crontab;

crontab::default::default() {
	_g_crontab.start();
}

crontab::default::~default() {
	_g_crontab.stop();
}

int crontab::default::setup(task *t, int min, int hour, int day, int month, int week) {
	static crontab::default _g_crontab_default;
	return _g_crontab.setup(t, min, hour, day, month, week);
}

void crontab::default::cancel(int id) {
	_g_crontab.cancel(id);
}
END_CUBE_CC_NS
