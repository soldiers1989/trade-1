#include "cube\cc\reactor.h"
#include <algorithm>
BEGIN_CUBE_CC_NS
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
END_CUBE_CC_NS
