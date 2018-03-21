#include "cube\cc\thread.h"
#include <algorithm>
BEGIN_CUBE_CC_NS
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

END_CUBE_CC_NS
