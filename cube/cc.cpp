#include "cc.h"
#include <algorithm>

BEGIN_CUBE_NAMESPACE
thread::thread() : _runnable(0) {

}

thread::thread(runnable *runnable) : _runnable(runnable) {

}

thread::~thread() {

}

int thread::start(std::string *error/* = 0*/) {
	if (_runnable == 0) {
		safe_assign<std::string>(error, "runnable object is null.");
		return -1;
	}

	//start thread
	try {
		_thread = std::thread(thread_func, this);
	} catch (const std::exception& e) {
		safe_assign<std::string>(error, e.what());
		return -1;
	}

	return 0;
}

int thread::start(runnable *runnable, std::string *error/* = 0*/) {
	_runnable = runnable;
	return start(error);
}

void thread::detach() {
	_thread.detach();
}

void thread::join() {
	_thread.join();
}

std::thread::id thread::getid() {
	return _thread.get_id();
}

unsigned __stdcall thread::thread_func(void *arg) {
	thread *pr = (thread*)arg;
	pr->_runnable->run();
	return 0;
}

threads::threads() : _runnable(0) {

}

threads::threads(runnable *runnable) : _runnable(runnable) {

}

threads::~threads() {

}

int threads::start(int nthread, std::string *error/* = 0*/) {
	for (int i = 0; i < nthread; i++) {
		thread *pthread = new thread(_runnable);
		if (pthread->start(error) != 0)
			return -1;
		_threads.push_back(pthread);
	}

	return 0;
}


int threads::start(runnable *runnable, int nthread, std::string *error/* = 0*/) {
	_runnable = runnable;
	return start(nthread, error);
}

void threads::detach() {
	for (size_t i = 0; i < _threads.size(); i++)
		_threads[i]->detach();
}

void threads::join() {
	for (size_t i = 0; i < _threads.size(); i++) {
		_threads[i]->join();
		delete _threads[i];
	}
	_threads.clear();
}

std::vector<std::thread::id> threads::getids() {
	std::vector<std::thread::id> ids;
	for (size_t i = 0; i < _threads.size(); i++)
		ids.push_back(_threads[i]->getid());
	return ids;
}

///////////////////////////////////////timer class/////////////////////////////////////////
timer::timer() : _nextid(0) {
}


timer::~timer() {
}

void timer::start(int maxethreads) {
	//set stop flag
	_stop.store(false);


	//start monitor
	_monitor = std::shared_ptr<std::thread>(new std::thread(monitor_thread_func, this));

	//start executor
	_executor.start(maxethreads);
}

int timer::setup(int delay, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<mitem> newitem(new mitem(_nextid, delay, t));
	std::list<std::shared_ptr<mitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<mitem> item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

int timer::setup(int delay, int interval, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<mitem> newitem(new mitem(_nextid, delay, interval, t));
	std::list<std::shared_ptr<mitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<mitem> item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

void timer::cancel(int id) {
	//cancel task in moniter
	std::unique_lock<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<mitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<mitem> item) {return id == item->id(); });
	if (iter != _items.end()) {
		_items.erase(iter);
		_cond.notify_all();
	}

	//cancel task in executor
	_executor.cancel(id);
}

void timer::stop() {
	//set stop flag
	_stop.store(true);

	//stop monitor
	_cond.notify_all();
	_monitor->join();

	//stop executor
	_executor.stop();

	//clear items
	_items.clear();
}

void timer::expire() {
	while (!_stop.load()) {
		std::unique_lock<std::mutex> lck(_mutex);
		if (_items.empty()) {
			_cond.wait_for(lck, std::chrono::milliseconds(100));
		} else {
			milliseconds waitms = _items.front()->latency();
			std::cv_status status = _cond.wait_for(lck, waitms);
			if (status == std::cv_status::timeout) {
				if (!_items.empty() && _items.front()->expired()) {
					std::shared_ptr<mitem> expireditem = _items.front();
					//generate executor item
					_executor.execute(expireditem->id(), expireditem->gettask());

					//remove expired item from items list
					_items.remove_if([expireditem](std::shared_ptr<mitem> item) {return item->id() == expireditem->id(); });
					//setup the expired item if it is cycled
					if (expireditem->cycled()) {
						expireditem->reset();
						std::list<std::shared_ptr<mitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [expireditem](std::shared_ptr<mitem> item) {return expireditem->expire() < item->expire(); });
						_items.insert(iter, expireditem);
					}
				}
			}
		}
	}
}

void timer::monitor_thread_func(timer *tmr) {
	tmr->expire();
}
END_CUBE_NAMESPACE
