/*
*	tsc - thread safe containers
*/
#pragma once
#include "cube.h"
#include <list>
#include <mutex>

BEGIN_CUBE_NAMESPACE
template<class T>
class list {
public:
	list() {}
	~list() {}

	void push_back(const T& val) {
		std::lock_guard<std::mutex> lock(_mutex);
		_list.push_back(val);
	}

	void push_front(const T& val) {
		std::lock_guard<std::mutex> lock(_mutex);
		_list.push_front(val);
	}

	void pop_back() {
		std::lock_guard<std::mutex> lock(_mutex);
		_list.pop_back();
	}

	void pop_front() {
		std::lock_guard<std::mutex> lock(_mutex);
		_list.pop_front();
	}

private:
	//mutex for list
	std::mutex _mutex;
	//stl list
	std::list<T> _list;
};
END_CUBE_NAMESPACE
