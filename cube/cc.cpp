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

timer::mitem::mitem(int id, int delay, task *task) : _id(id), _delay(delay), _task(task), _cycle(false), _interval(-1) {
	_expire = clock::now() + _delay;
}

timer::mitem::mitem(int id, int delay, int interval, task *task) : _id(id), _delay(delay), _interval(interval), _task(task), _cycle(true) {
	_expire = clock::now() + _delay;
}

timer::mitem::~mitem() {

}

int timer::mitem::id() {
	return _id;
}

bool timer::mitem::cycled() {
	return _cycle;
}

timer::task* timer::mitem::gettask() {
	return _task;
}

void timer::mitem::reset() {
	_expire = _expire + _interval;
}

const timer::timepoint& timer::mitem::expire() {
	return _expire;
}

bool timer::mitem::expired(std::chrono::time_point<clock> now/* = clock::now()*/) {
	return !(_expire > now);
}

timer::milliseconds timer::mitem::latency(std::chrono::time_point<clock> now/* = clock::now()*/) {
	return std::chrono::duration_cast<milliseconds>(_expire - now);
}

timer::eitem::eitem(int id, task *task) : _id(id), _task(task) {
	_status.store((int)status::pending);
	_dummy = new char[1024];
}

timer::eitem::~eitem() {
	delete _dummy;
}

void timer::eitem::run() {
	_status.store((int)status::running);
	_task->run();
	_status.store((int)status::finished);
}

void timer::eitem::join() {
	while (_status.load() != (int)status::finished)
		std::this_thread::yield();
}

bool timer::eitem::pending() {
	return _status.load() == (int)status::pending;
}

void timer::eitem::waiting() {
	_status.store((int)status::waiting);
}

int timer::eitem::id() {
	return _id;
}

timer::executor::executor() {
}

timer::executor::~executor() {
}

int timer::executor::start(int maxthreads/* = 1*/) {
	_maxthreads = maxthreads;
	_stop.store(false);
	std::lock_guard<std::mutex> lck(_mutex);
	for (int i = 0; i<maxthreads; i++)
		_threads.push_back(std::shared_ptr<std::thread>(new std::thread(executor_thread_func, this)));
	return 0;
}

void timer::executor::execute(int id, task *task) {
	std::lock_guard<std::mutex> lck(_mutex);
	_items.push_back(std::shared_ptr<eitem>(new eitem(id, task)));
}

void timer::executor::cancel(int id) {
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

void timer::executor::stop() {
	_stop.store(true);
	std::lock_guard<std::mutex> lck(_mutex);
	std::for_each(_threads.begin(), _threads.end(), [](std::shared_ptr<std::thread> thd) {thd->join(); });
	_threads.clear();
}

void timer::executor::balance() {

}

void timer::executor::execute() {
	int yield = 0;
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

void timer::executor::executor_thread_func(executor *e) {
	e->execute();
}


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
