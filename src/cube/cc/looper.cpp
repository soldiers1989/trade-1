#include "cube\cc\looper.h"
#include <algorithm>
BEGIN_CUBE_CC_NS
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
	if (_thread->joinable())
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

END_CUBE_CC_NS
