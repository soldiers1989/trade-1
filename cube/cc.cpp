#include "cc.h"

BEGIN_CUBE_NAMESPACE
thread::thread() : _runnable(0), _stop(false), _stopped(true)
{

}

thread::thread(runnable *runnable) : _runnable(runnable), _stop(false), _stopped(true)
{

}

thread::~thread()
{

}

int thread::start(std::string *error/* = 0*/)
{
	if (_runnable == 0)
	{
		safe_assign<std::string>(error, "runnable object is null.");
		return -1;
	}

	//start thread
	try
	{
		if (!_stopped)
			return 0;
		_stop = false;
		_thread = std::thread(thread_func, this);
		_stopped = false;
	}
	catch (const std::exception& e)
	{
		safe_assign<std::string>(error, e.what());
		return -1;
	}

	return 0;
}

int thread::start(runnable *runnable, std::string *error/* = 0*/)
{
	_runnable = runnable;
	return start(error);
}

void thread::detach()
{
	_thread.detach();
}

void thread::stop()
{
	//thread is not running
	if (_stopped)
		return;

	//stop running thread
	_stop = true;
	_thread.join();
	_stopped = true;
}

std::thread::id thread::getid()
{
	return _thread.get_id();
}

unsigned __stdcall thread::thread_func(void *arg)
{
	thread *pr = (thread*)arg;
	while (!pr->_stop)
		pr->_runnable->loop();
	return 0;
}

threads::threads() : _runnable(0)
{

}

threads::threads(runnable *runnable) : _runnable(runnable)
{

}

threads::~threads()
{

}

int threads::start(int nthread, std::string *error/* = 0*/)
{
	for (int i = 0; i < nthread; i++)
	{
		thread *pthread = new thread(_runnable);
		if (pthread->start(error) != 0)
		{
			//stop the started threads
			stop();
			return -1;
		}
		_threads.push_back(pthread);
	}

	return 0;
}


int threads::start(runnable *runnable, int nthread, std::string *error/* = 0*/)
{
	_runnable = runnable;
	return start(nthread, error);
}

void threads::detach()
{
	for (size_t i = 0; i < _threads.size(); i++)
		_threads[i]->detach();
}

void threads::stop()
{
	for (size_t i = 0; i < _threads.size(); i++)
	{
		_threads[i]->stop();
		delete _threads[i];
	}
	_threads.clear();
}

std::vector<std::thread::id> threads::getids()
{
	std::vector<std::thread::id> ids;
	for (size_t i = 0; i < _threads.size(); i++)
		ids.push_back(_threads[i]->getid());
	return ids;
}
END_CUBE_NAMESPACE
