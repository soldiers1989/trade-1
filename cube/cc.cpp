#include "cc.h"

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
timer::timer() : _stop(false){

}

timer::~timer() {

}

void timer::init(int executors/* = 1*/) {
	//set stop flag
	_stop = false;

	//start executors
	for (int i = 0; i < executors; i++) {
		_executors.push_back(std::thread(execute, this));
	}

	//start monitor
	_monitor = std::thread(monitor, this);
}

int timer::set(int delay, task t) {
	std::lock_guard<std::mutex> lck(_wmutex);
	//create new item
	item *newitem = new item(_nextid, delay, t);

	//insert to proper position to wait list by expire timepoint
	std::list<itemptr>::iterator iter = _witems.begin(), iterend = _witems.end();
	while (iter != iterend) {
		if (newitem->expire > (*iter)->expire) {
			break;
		} else {
			iter++;
		}
	}
	_witems.insert(iter, itemptr(newitem));

	//new item coming wake up monitor
	_wcond.notify_all();

	return _nextid++;
}

int timer::set(int delay, int interval, task t) {
	std::lock_guard<std::mutex> lck(_wmutex);
	//create new item
	item *newitem = new item(_nextid, delay, interval, t);

	//insert to proper position to wait list by expire timepoint
	std::list<itemptr>::iterator iter = _witems.begin(), iterend = _witems.end();
	while (iter != iterend) {
		if (newitem->expire > (*iter)->expire) {
			break;
		} else {
			iter++;
		}
	}
	_witems.insert(iter, itemptr(newitem));
	
	//new item coming wake up monitor
	_wcond.notify_all();

	return _nextid++;
}

void timer::cancel(int id) {
	{
		std::lock_guard<std::mutex> lck(_wmutex);
		std::list<itemptr>::iterator iter = _witems.begin(), iterend = _witems.end();
		while (iter != iterend) {
			if ((*iter)->id == id) {
				_witems.erase(iter);
				return;
			} else {
				iter++;
			}
		}
	}

	{
		std::lock_guard<std::mutex> lck(_emutex);
		std::list<itemptr>::iterator iter = _eitems.begin(), iterend = _eitems.end();
		while (iter != iterend) {
			if ((*iter)->id == id) {
				_eitems.erase(iter);
				return;
			} else {
				iter++;
			}
		}
	}
}

void timer::destroy() {
	//set stop flag
	_stop = true;

	//wait for monitor to stop
	_wcond.notify_all();
	_monitor.join();

	//wait for executors to stop
	_econd.notify_all();
	for (size_t i = 0; i < _executors.size(); i++) {
		_executors[i].join();
	}

	//free all item tasks
	_witems.clear();
	_eitems.clear();
}

void timer::wait_expire() {
	while (_stop) {
		itemptr pitem = nullptr;
		{
			std::unique_lock<std::mutex> lck(_wmutex);
			if (_witems.size() == 0) {
				_wcond.wait(lck);
			} else {
				std::cv_status status = _wcond.wait_for(lck, _witems.back()->expire - clock::now());
				if (status == std::cv_status::timeout) {
					pitem = _witems.back();
					_witems.pop_back();
				}
			}
		}

		{
			if (pitem != nullptr) {
				std::unique_lock<std::mutex> lck(_emutex);
				_eitems.push_back(pitem);
				_econd.notify_one();
			}
		}
	}
}

void timer::run_expired() {
	while (_stop) {
		itemptr pitem = nullptr;
		{
			std::unique_lock<std::mutex> lck(_emutex);
			if (_eitems.size() == 0) {
				_econd.wait(lck);
			} else {
				pitem = _eitems.front();
				_eitems.pop_front();
			}
		}
	}
}

void timer::monitor(timer *tmr) {
	tmr->wait_expire();
}

void timer::execute(timer *tmr) {
	tmr->run_expired();
}

END_CUBE_NAMESPACE
