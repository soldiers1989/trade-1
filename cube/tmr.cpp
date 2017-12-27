#include "tmr.h"
BEGIN_CUBE_NAMESPACE
timer::timer() : _nextid(0){
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
	//cancel task in executor
	_executor.cancel(id);

	//cancel task in moniter
	std::unique_lock<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<mitem>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<mitem> item) {return id == item->id(); });
	if (iter != _items.end()) {
		_items.erase(iter);
		_cond.notify_all();
	}
}

void timer::stop() {
	//set stop flag
	_stop.store(true);

	//stop monitor
	_cond.notify_all();
	_monitor->join();

	//clear items
	_items.clear();

	//stop executor
	_executor.stop();
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
