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
timer::timer() : _stop(false), _nextid(0){

}

timer::~timer() {

}

void timer::start() {
	//set stop flag
	_stop.store(false);

	//start monitor
	_monitor = std::thread(monitor, this);
}

int timer::setup(int delay, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);
	std::shared_ptr<timertask> newtask(new timertask(_nextid, delay, t));
	std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [newtask](std::shared_ptr<timertask> currtask) {return newtask->expire > currtask->expire; });
	_tasks.insert(iter, newtask);
	_cond.notify_one();
	return _nextid++;
}

int timer::setup(int delay, int interval, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);
	std::shared_ptr<timertask> newtask(new timertask(_nextid, delay, interval, t));
	std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [newtask](std::shared_ptr<timertask> currtask) {return newtask->expire > currtask->expire; });
	_tasks.insert(iter, newtask);
	_cond.notify_one();
	return 0;
}

void timer::cancel(int id) {
	std::unique_lock<std::mutex> lck(_mutex);
	_tasks.remove_if([id](std::shared_ptr<timertask> currtask) {return currtask->id == id; });
	_cond.notify_one();
}

void timer::stop() {
	//set stop flag
	_stop.store(true);

	//wait for monitor to stop
	_cond.notify_all();
	_monitor.join();

	//clear tasks
	_tasks.clear();
}

void timer::expire() {
	while (!_stop.load()) {
		std::unique_lock<std::mutex> lck(_mutex);
		if (_tasks.size() == 0) {
			_cond.wait(lck);
		} else {
			std::shared_ptr<timertask> latest = _tasks.back();
			std::chrono::milliseconds ms = std::chrono::duration_cast<milliseconds>(latest->expire - clock::now());
			std::cv_status status = _cond.wait_for(lck, ms);
			if (status == std::cv_status::timeout) {
				//run expired task
				latest->run();
				//remove from task list
				_tasks.pop_back();
				//reset if cycle timer task
				if (latest->cycle) {
					latest->reset();
					std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [latest](std::shared_ptr<timertask> currtask) {return latest->expire > currtask->expire; });
					_tasks.insert(iter, latest);
				}			
			}
		}
	}
}

void timer::monitor(timer *tmr) {
	tmr->expire();
}

END_CUBE_NAMESPACE
