#include "cc.h"
#include <time.h>
#include <future>
#include <algorithm>
BEGIN_CUBE_NAMESPACE
////////////////////////////////looper class//////////////////////////////
looper::looper() : _task(0), _stop(false), _status(status::stopped), _thread(nullptr) {

}

looper::~looper() {

}

void looper::start(task *task) {
	//set task
	_task = task;

	//start loop thread
	_stop = false;
	_status = status::starting;
	_thread = std::shared_ptr<std::thread>(new std::thread(loop_thread_func, this));
}


void looper::stop() {
	//set stop flag
	_stop = true;

	//wait until thread started
	while (_status == status::starting)
		std::this_thread::yield();

	//wait for thread to exit
	if(_thread->joinable())
		_thread->join();
}

void looper::loop() {
	_status = status::runing;

	while (!_stop) {
		_task->run();
	}
	_status = status::stopped;
}

void looper::loop_thread_func(looper *looper) {
	looper->loop();
}

////////////////////////////////loopers class//////////////////////////////
loopers::loopers() {
}

loopers::~loopers() {
}

void loopers::start(task *task, int nloopers) {
	for (int i = 0; i < nloopers; i++) {
		std::shared_ptr<looper> lpr = std::shared_ptr<looper>(new looper());
		lpr->start(task);
		_loopers.push_back(lpr);
	}
}

void loopers::stop() {
	std::for_each(_loopers.begin(), _loopers.end(), [](std::shared_ptr<looper> &looper) {looper->stop(); });
}

////////////////////////////////thread class//////////////////////////////
thread::thread() : _task(0), _thread(nullptr) {
}

thread::~thread() {
}

void thread::start(task *task) {
	//set task
	_task = task;

	//start thread
	_thread = std::shared_ptr<std::thread>(new std::thread(thread_func, this));
}

void thread::detach() {
	_thread->detach();
}

void thread::join() {
	_thread->join();
}

std::thread::id thread::getid() {
	return _thread->get_id();
}

void thread::run() {
	_task->run();
}

void thread::thread_func(thread *thd) {
	thd->run();
}

////////////////////////////////threads class//////////////////////////////
threads::threads() {

}

threads::~threads() {

}

void threads::start(task *task, int nthread) {
	//start threads to run the task
	for (int i = 0; i < nthread; i++) {
		std::shared_ptr<thread> thd = std::shared_ptr<thread>(new thread());
		thd->start(task);
		_threads.push_back(thd);
	}
}

void threads::detach() {
	std::for_each(_threads.begin(), _threads.end(), [](std::shared_ptr<thread> &thd) {thd->detach(); });
}

void threads::join() {
	std::for_each(_threads.begin(), _threads.end(), [](std::shared_ptr<thread> &thd) {thd->join(); });
}

std::list<std::thread::id> threads::getids() {
	std::list<std::thread::id> ids;
	std::for_each(_threads.begin(), _threads.end(), [&ids](std::shared_ptr<thread> &thd) { ids.push_back(thd->getid()); });
	return ids;
}

///////////////////////////////////////reactor class/////////////////////////////////////////

reactor::item::item(int id, task *task) : _id(id), _task(task), _ctime(clock::now()), _pending(true), _refcnt(0) {

}

reactor::item::~item() {

}

bool reactor::item::operator ==(task *task) {
	return _task == task;
}

bool reactor::item::operator ==(int id) {
	return _id == id;
}

int reactor::item::id() {
	return _id;
}

void reactor::item::run() {
	_task->run();
	subref();
}

void reactor::item::join() {
	while (_refcnt.load() != 0)
		std::this_thread::yield();
}

void reactor::item::addref() {
	_refcnt.fetch_add(1);
}
void reactor::item::subref() {
	_refcnt.fetch_sub(1);
}

bool reactor::item::pending() {
	return _pending;
}

void reactor::item::pending(bool flag) {
	_pending = flag;
}

const reactor::timepoint& reactor::item::ctime() {
	return _ctime;
}

reactor::items::items() {

}

reactor::items::~items() {
	std::for_each(_items.begin(), _items.end(), [](item *item) {item->join(); delete item; });
	_items.clear();
}

int reactor::items::add(task *task) {
	static int gID = 0;
	std::lock_guard<std::mutex> lck(_mutex);
	_items.push_back(new item(gID, task));
	return gID++;
}

void reactor::items::cancel(int id) {
	std::lock_guard<std::mutex> lck(_mutex);
	std::list<item*>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](item *item) {return *item == id; });
	while (iter != _items.end()) {
		//delete current match task
		(*iter)->join();
		delete *iter;

		//erase the task from item list
		_items.erase(iter);

		//find next task
		iter = std::find_if(_items.begin(), _items.end(), [id](item *item) {return *item == id; });
	}
}

void reactor::items::cancel(task *task) {
	std::lock_guard<std::mutex> lck(_mutex);
	std::list<item*>::iterator iter = std::find_if(_items.begin(), _items.end(), [task](item *item) {return *item == task; });
	while (iter != _items.end()) {
		//delete current match task
		(*iter)->join();
		delete *iter;
		
		//erase the task from item list
		_items.erase(iter);

		//find next task
		iter = std::find_if(_items.begin(), _items.end(), [task](item *item) {return *item == task; });
	}
}

bool reactor::items::run() {
	item *itm = 0;
	{
		std::lock_guard<std::mutex> lck(_mutex);
		std::list<item*>::iterator iter = std::find_if(_items.begin(), _items.end(), [](item *item) {return item->pending(); });
		if (iter != _items.end()) {
			itm = *iter;
			itm->pending(false);
			itm->addref();
		}
	}

	if (itm != 0) {
		int id = itm->id();
		//run item
		itm->run();

		//remove finished item
		std::lock_guard<std::mutex> lck(_mutex);
		std::list<item*>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](item *item) {return *item == id; });
		if (iter != _items.end()) {
			delete *iter;
			_items.erase(iter);
		}

		//true means run an item
		return true;
	}

	return false;
}

bool reactor::items::busy(int waitms) {
	std::lock_guard<std::mutex> lck(_mutex);
	std::list<item*>::iterator iter = std::find_if(_items.begin(), _items.end(), [](item *item) {return item->pending(); });
	if (iter != _items.end()) {
		if (clock::now() - (*iter)->ctime() > milliseconds(waitms)) {
			return true;
		}
	}

	return false;
}

reactor::executor::executor() : _items(0), _idle_flag(true), _last_idle_time(clock::now()) {

}

reactor::executor::~executor() {

}

void reactor::executor::start(items *items) {
	_items = items;
	_looper.start(this);
}

void reactor::executor::stop() {
	_looper.stop();
}

void reactor::executor::run() {
	bool res = _items->run();
	if (res) {
		if (_idle_flag) {
			_idle_flag = false;
		}
	} else {
		std::this_thread::sleep_for(milliseconds(50));
		if (!_idle_flag) {
			_idle_flag = true;
			_last_idle_time = clock::now();
		}
	}
}

bool reactor::executor::idle(int idlems) {
	if (_idle_flag && clock::now() - _last_idle_time > milliseconds(idlems)) {
		return true;
	}
	return false;
}

reactor::executors::executors() {

}

reactor::executors::~executors() {

}

void reactor::executors::start(int max_executors, items *items) {
	//set parameters
	_max_executors = max_executors;
	_items = items;

	//start 1 executor
	std::lock_guard<std::mutex> lck(_mutex);
	executor *extr = new executor();
	extr->start(_items);
	_executors.push_back(std::shared_ptr<executor>(extr));
}

void reactor::executors::stop() {
	std::lock_guard<std::mutex> lck(_mutex);
	std::for_each(_executors.begin(), _executors.end(), [](std::shared_ptr<executor> &extr) {extr->stop(); });
	_executors.clear();
}

void reactor::executors::balance() {
	const static int max_idle_ms = 5000;
	const static int max_wait_ms = 1000;

	std::lock_guard<std::mutex> lck(_mutex);
	bool decreased = false;
	int current_executors = (int)_executors.size();
	if (current_executors > 1) {
		std::list<std::shared_ptr<executor>>::iterator iter = std::find_if(_executors.begin(), _executors.end(), [](std::shared_ptr<executor> &extr) {return extr->idle(max_idle_ms); });
		if (iter != _executors.end()) {
			//decrease 1 executor
			(*iter)->stop();
			_executors.erase(iter);
			decreased = true;
		}
	}

	if (!decreased && current_executors < _max_executors) {
		if (_items->busy(max_wait_ms)) {
			//increase 1 executor
			executor *extr = new executor();
			extr->start(_items);
			_executors.push_back(std::shared_ptr<executor>(extr));
		}
	}
}

reactor::reactor() {

}

reactor::~reactor() {

}

void reactor::start(int max_executors) {
	_executors.start(max_executors, &_items);
	_monitor.start(this);
}

int reactor::react(task *task) {
	return _items.add(task);
}

void reactor::cancel(int id) {
	return _items.cancel(id);
}

void reactor::cancel(task *task) {
	_items.cancel(task);
}

void reactor::stop() {
	//stop monitor
	_monitor.stop();

	//stop executors
	_executors.stop();
}

void reactor::balance() {
	_executors.balance();
}


void reactor::run() {
	balance();
	std::this_thread::sleep_for(milliseconds(1000));
}


///////////////////////global reactor object///////////////////
static reactor _g_reactor;

reactor::default::default() {
	_g_reactor.start(10);
}

reactor::default::~default() {
	_g_reactor.stop();
}

void reactor::default::react(task *task) {
	static reactor::default _g_reactor_default;
	_g_reactor.react(task);
}

void reactor::default::cancel(task *task) {
	_g_reactor.cancel(task);
}

///////////////////////////////////////timer class/////////////////////////////////////////

timer::item::item(int id, int delay, cube::task *task) : _id(id), _delay(delay), _task(task), _cycle(false), _interval(-1) {
	_expire = clock::now() + _delay;
}

timer::item::item(int id, int delay, int interval, cube::task *task) : _id(id), _delay(delay), _interval(interval), _task(task) {
	_expire = clock::now() + _delay;
	_cycle = interval > 0 ? true : false;
}

timer::item::~item() {

}

int timer::item::id() {
	return _id;
}

bool timer::item::cycled() {
	return _cycle;
}

task* timer::item::task() {
	return _task;
}

void timer::item::reset() {
	_expire = _expire + _interval;
}

const timer::timepoint& timer::item::expire() {
	return _expire;
}

bool timer::item::expired(std::chrono::time_point<clock> now/* = clock::now()*/) {
	return !(_expire > now);
}

timer::milliseconds timer::item::latency(std::chrono::time_point<clock> now/* = clock::now()*/) {
	return std::chrono::duration_cast<milliseconds>(_expire - now);
}

timer::timer() : _nextid(0) {
}

timer::~timer() {
}

void timer::start(int max_executors) {
	//start reactor
	_reactor.start(max_executors);

	//start monitor
	_monitor.start(this);
}

int timer::setup(int delayms, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<item> newitem(new item(_nextid, delayms, t));
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<item> &item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

int timer::setup(int delayms, int intervalms, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<item> newitem(new item(_nextid, delayms, intervalms, t));
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<item> &item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

void timer::cancel(int id) {
	//cancel task in moniter
	std::unique_lock<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<item> &item) {return id == item->id(); });
	if (iter != _items.end()) {
		//cancel task in executor
		_reactor.cancel((*iter)->task());
		
		//remove from timer items
		_items.erase(iter);
		_cond.notify_all();
	}

}

void timer::stop() {
	//stop monitor
	_cond.notify_all();
	_monitor.stop();

	//stop reactor
	_reactor.stop();

	//clear items
	_items.clear();
}

void timer::expire() {
	
	std::unique_lock<std::mutex> lck(_mutex);
	if (_items.empty()) {
		_cond.wait_for(lck, std::chrono::milliseconds(100));
	} else {
		milliseconds waitms = _items.front()->latency();
		std::cv_status status = _cond.wait_for(lck, waitms);
		if (status == std::cv_status::timeout) {
			if (!_items.empty() && _items.front()->expired()) {
				std::shared_ptr<item> expireditem = _items.front();
				//generate executor item
				_reactor.react(expireditem->task());

				//remove expired item from items list
				_items.remove_if([expireditem](std::shared_ptr<item> &item) {return item->id() == expireditem->id(); });
				//setup the expired item if it is cycled
				if (expireditem->cycled()) {
					expireditem->reset();
					std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [expireditem](std::shared_ptr<item> &item) {return expireditem->expire() < item->expire(); });
					_items.insert(iter, expireditem);
				}
			}
		}
	}
}

void timer::run() {
	expire();
}

///////////////////////global timer object///////////////////
static timer _g_timer;

timer::default::default() {
	_g_timer.start(10);
}

timer::default::~default() {
	_g_timer.stop();
}

int timer::default::setup(int delay, task *t) {
	return setup(delay, -1, t);
}

int timer::default::setup(int delay, int interval, task *t) {
	static timer::default _g_timer_default;
	return _g_timer.setup(delay, interval, t);
}

void timer::default::cancel(int id) {
	_g_timer.cancel(id);
}

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

crontab::crontab() : _nextid(0){
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
	std::list<std::shared_ptr<item>>::iterator iter= std::find_if(_items.begin(), _items.end(), ([id](std::shared_ptr<item> &item) {return item->id() == id; }));
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

END_CUBE_NAMESPACE
