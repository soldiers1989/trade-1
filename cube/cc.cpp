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

void timer::start(int nthread) {
	//set stop flag
	_stop.store(false);

	//start monitor
	for(int i=0; i<nthread; i++)
		_monitors.push_back(std::shared_ptr<std::thread>(new std::thread(monitor, this)));
}

int timer::setup(int delay, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);
	std::shared_ptr<timertask> newtask(new timertask(_nextid, delay, t));
	std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [newtask](std::shared_ptr<timertask> currtask) {return newtask->expire < currtask->expire; });
	_tasks.insert(iter, newtask);
	_cond.notify_all();
	return _nextid++;
}

int timer::setup(int delay, int interval, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);
	std::shared_ptr<timertask> newtask(new timertask(_nextid, delay, interval, t));
	std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [newtask](std::shared_ptr<timertask> currtask) {return newtask->expire < currtask->expire; });
	_tasks.insert(iter, newtask);
	_cond.notify_all();
	return _nextid++;
}

void timer::cancel(int id) {
	std::unique_lock<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [id](std::shared_ptr<timertask> task) {return id == task->id; });
	if (iter != _tasks.end()) {
		if (!(*iter)->waited) {
			_tasks.erase(iter);
		}
		else {
			(*iter)->cancel();
			_cond.notify_all();
		}
	}
}

void timer::stop() {
	//set stop flag
	_stop.store(true);

	//wait for monitor to stop
	_cond.notify_all();
	std::for_each(_monitors.begin(), _monitors.end(), [](std::shared_ptr<std::thread> thd) {thd->join(); });
	_monitors.clear();

	//clear tasks
	_tasks.clear();
}

void timer::expire() {
	while (!_stop.load()) {
		std::unique_lock<std::mutex> lck(_mutex);
		std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [](std::shared_ptr<timertask> task) {return !task->waited; });
		if (iter == _tasks.end()) {
			_cond.wait(lck);
		} else {
			//get the latest and not waited task
			std::shared_ptr<timertask> latest = *iter;
			latest->wait();

			//wait for the task to expired
			std::chrono::time_point<clock> now = clock::now();
			std::cv_status status = _cond.wait_for(lck, latest->latency(now));

			//execute the task if it is not canceled
			if (status == std::cv_status::timeout && !latest->canceled) {
				now = clock::now();
				//run expired task
				latest->run();
				//remove from task list
				_tasks.remove_if([latest](std::shared_ptr<timertask> task) {return task->id == latest->id; });
				//reset if cycle timer task
				if (latest->cycle) {
					latest->reset(now);
					std::list<std::shared_ptr<timertask>>::iterator iter = std::find_if(_tasks.begin(), _tasks.end(), [latest](std::shared_ptr<timertask> task) {return latest->expire < task->expire; });
					_tasks.insert(iter, latest);
				}			
			}
			else {
				//remove the task if it is canceled
				if (latest->canceled) {
					_tasks.remove_if([latest](std::shared_ptr<timertask> task) {return task->id == latest->id; });
				}
				else {
					latest->wait(false);
				}
			}
		}
	}
}

void timer::monitor(timer *tmr) {
	tmr->expire();
}

END_CUBE_NAMESPACE
