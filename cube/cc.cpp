#include "cc.h"
#include "log.h"
#include <algorithm>
BEGIN_CUBE_NAMESPACE
////////////////////////////////looper class//////////////////////////////
looper::looper() : _task(0), _stop(false), _thread(nullptr) {

}

looper::~looper() {

}

void looper::start(task *task) {
	//set task
	_task = task;

	//start loop thread
	_stop = false;
	_thread = std::shared_ptr<std::thread>(new std::thread(loop_thread_func, this));
}


void looper::stop() {
	//set stop flag
	_stop = true;

	//wait for thread to exit
	_thread->join();
}

void looper::loop() {
	while (!_stop) {
		_task->run();
	}
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
	std::for_each(_loopers.begin(), _loopers.end(), [](std::shared_ptr<looper> looper) {looper->stop(); });
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
	std::for_each(_threads.begin(), _threads.end(), [](std::shared_ptr<thread> thd) {thd->detach(); });
}

void threads::join() {
	std::for_each(_threads.begin(), _threads.end(), [](std::shared_ptr<thread> thd) {thd->join(); });
}

std::list<std::thread::id> threads::getids() {
	std::list<std::thread::id> ids;
	std::for_each(_threads.begin(), _threads.end(), [&ids](std::shared_ptr<thread> thd) { ids.push_back(thd->getid()); });
	return ids;
}

///////////////////////////////////////reactor class/////////////////////////////////////////

reactor::item::item(int id, task *task) : _id(id), _task(task), _ctime(clock::now()) {

}

reactor::item::~item() {

}

int reactor::item::id() {
	return _id;
}

void reactor::item::run() {
	_status.store((int)status::running);
	_task->run();
	_status.store((int)status::finished);
}

void reactor::item::join() {
	while (_status.load() != (int)status::finished)
		std::this_thread::yield();
}

void reactor::item::waiting() {
	_status.store((int)status::waiting);
}

bool reactor::item::pending() {
	return _status.load() == (int)status::pending;
}

bool reactor::item::finished() {
	return _status.load() == (int)status::finished;
}

const reactor::timepoint& reactor::item::ctime() {
	return _ctime;
}

reactor::items::items() {

}

reactor::items::~items() {

}

void reactor::items::add(int id, task *task) {
	std::lock_guard<std::mutex> lck(_mutex);
	_items.push_back(std::shared_ptr<item>(new item(id, task)));
}

void reactor::items::del(int id) {
	std::lock_guard<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<item> item) {return item->id() == id; });
	while (iter != _items.end()) {
		if (!(*iter)->pending()) {
			(*iter)->join();
		}
		_items.erase(iter);

		iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<item> item) {return item->id() == id; });
	}
}

void reactor::items::del(std::shared_ptr<item> &itm) {
	std::lock_guard<std::mutex> lck(_mutex);
	_items.remove(itm);
}

bool reactor::items::run_next(std::shared_ptr<item> &itm) {
	itm = nullptr;
	{
		std::lock_guard<std::mutex> lck(_mutex);
		std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [](std::shared_ptr<item> item) {return item->pending(); });
		if (iter != _items.end()) {
			itm = *iter;
			itm->waiting();
		}
	}

	if (itm != nullptr) {
		itm->run();
		return true;
	}

	return false;
}

bool reactor::items::busy(int waitms) {
	std::lock_guard<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [](std::shared_ptr<item> item) {return item->pending(); });
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
	std::shared_ptr<item> itm = nullptr;
	bool res = _items->run_next(itm);
	if (res) {
		_items->del(itm);
		if (_idle_flag) {
			_idle_flag = false;
		}
	} else {
		std::this_thread::sleep_for(milliseconds(10));
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
	std::for_each(_executors.begin(), _executors.end(), [](std::shared_ptr<executor> extr) {extr->stop(); });
	_executors.clear();
}

void reactor::executors::balance() {
	log::info("balance......");
	const static int max_idle_ms = 5000;
	const static int max_wait_ms = 1000;

	std::lock_guard<std::mutex> lck(_mutex);
	bool decreased = false;
	int current_executors = (int)_executors.size();
	if (current_executors > 1) {
		std::list<std::shared_ptr<executor>>::iterator iter = std::find_if(_executors.begin(), _executors.end(), [](std::shared_ptr<executor> extr) {return extr->idle(max_idle_ms); });
		if (iter != _executors.end()) {
			//decrease 1 executor
			(*iter)->stop();
			_executors.erase(iter);
			decreased = true;
			log::info("decrease 1 thread.");
		}
	}

	if (!decreased && current_executors < _max_executors) {
		if (_items->busy(max_wait_ms)) {
			//increase 1 executor
			executor *extr = new executor();
			extr->start(_items);
			_executors.push_back(std::shared_ptr<executor>(extr));
			log::info("increase 1 thread.");
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

void reactor::react(int id, task *task) {
	_items.add(id, task);
}

void reactor::cancel(int id) {
	_items.del(id);
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

///////////////////////////////////////timer class/////////////////////////////////////////

timer::item::item(int id, int delay, cube::task *task) : _id(id), _delay(delay), _task(task), _cycle(false), _interval(-1) {
	_expire = clock::now() + _delay;
}

timer::item::item(int id, int delay, int interval, cube::task *task) : _id(id), _delay(delay), _interval(interval), _task(task), _cycle(true) {
	_expire = clock::now() + _delay;
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

int timer::setup(int delay, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<item> newitem(new item(_nextid, delay, t));
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<item> item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

int timer::setup(int delay, int interval, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<item> newitem(new item(_nextid, delay, interval, t));
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<item> item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

void timer::cancel(int id) {
	//cancel task in moniter
	std::unique_lock<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<item> item) {return id == item->id(); });
	if (iter != _items.end()) {
		_items.erase(iter);
		_cond.notify_all();
	}

	//cancel task in executor
	_reactor.cancel(id);
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
				_reactor.react(expireditem->id(), expireditem->task());

				//remove expired item from items list
				_items.remove_if([expireditem](std::shared_ptr<item> item) {return item->id() == expireditem->id(); });
				//setup the expired item if it is cycled
				if (expireditem->cycled()) {
					expireditem->reset();
					std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [expireditem](std::shared_ptr<item> item) {return expireditem->expire() < item->expire(); });
					_items.insert(iter, expireditem);
				}
			}
		}
	}
}

void timer::run() {
	expire();
}
END_CUBE_NAMESPACE
