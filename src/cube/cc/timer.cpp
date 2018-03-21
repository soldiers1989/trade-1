#include "cube\cc\timer.h"
#include <algorithm>
BEGIN_CUBE_CC_NS
///////////////////////////////////////timer class/////////////////////////////////////////

timer::item::item(int id, int delay,cc::task *task) : _id(id), _delay(delay), _task(task), _cycle(false), _interval(-1) {
	_expire = clock::now() + _delay;
}

timer::item::item(int id, int delay, int interval,cc::task *task) : _id(id), _delay(delay), _interval(interval), _task(task) {
	_expire = clock::now() + _delay;
	_cycle = interval > 0 ? true : false;
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

int timer::setup(int delayms, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<item> newitem(new item(_nextid, delayms, t));
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<item> &item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

int timer::setup(int delayms, int intervalms, task *t) {
	std::unique_lock<std::mutex> lck(_mutex);

	std::shared_ptr<item> newitem(new item(_nextid, delayms, intervalms, t));
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [newitem](std::shared_ptr<item> &item) {return newitem->expire() < item->expire(); });
	_items.insert(iter, newitem);
	_cond.notify_all();

	return _nextid++;
}

void timer::cancel(int id) {
	//cancel task in moniter
	std::unique_lock<std::mutex> lck(_mutex);
	std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [id](std::shared_ptr<item> &item) {return id == item->id(); });
	if (iter != _items.end()) {
		//cancel task in executor
		_reactor.cancel((*iter)->task());

		//remove from timer items
		_items.erase(iter);
		_cond.notify_all();
	}

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
				_reactor.react(expireditem->task());

				//remove expired item from items list
				_items.remove_if([expireditem](std::shared_ptr<item> &item) {return item->id() == expireditem->id(); });
				//setup the expired item if it is cycled
				if (expireditem->cycled()) {
					expireditem->reset();
					std::list<std::shared_ptr<item>>::iterator iter = std::find_if(_items.begin(), _items.end(), [expireditem](std::shared_ptr<item> &item) {return expireditem->expire() < item->expire(); });
					_items.insert(iter, expireditem);
				}
			}
		}
	}
}

void timer::run() {
	expire();
}

///////////////////////global timer object///////////////////
static timer _g_timer;

timer::default::default() {
	_g_timer.start(10);
}

timer::default::~default() {
	_g_timer.stop();
}

int timer::default::setup(int delay, task *t) {
	return setup(delay, -1, t);
}

int timer::default::setup(int delay, int interval, task *t) {
	static timer::default _g_timer_default;
	return _g_timer.setup(delay, interval, t);
}

void timer::default::cancel(int id) {
	_g_timer.cancel(id);
}

END_CUBE_CC_NS
