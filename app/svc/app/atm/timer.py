"""
    timer for scheduler and execute tasks
"""
import threading, time, datetime


class Status:
    TODO = '待执行'
    DOING = '执行中'
    DONE = '已执行'

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.status = Status.TODO
        self.result = None
        self.stopped = None


class Runnable(threading.Thread):
    def __init__(self):
        # status of thread
        self.status = Status()

        # init thread
        threading.Thread.__init__(self)

    def getstatus(self):
        """
            get runnable task status
        :return:
        """
        return {
            'stime':self.status.start_time,
            'etime':self.status.end_time,
            'result':self.status.result,
            'status':self.status.status,
            'alive':self.is_alive()
        }

    def do(self):
        """
            sub class must be realize this method to do something
        :return:
        """
        pass

    def run(self):
        """
            thread run method
        :return:
        """
        self.status.stopped = False

        self.status.status = Status.DOING
        self.status.start_time = time.time()
        try:
            # do something
            res = self.do()
            # update result
            self.status.result = str(res)
        except Exception as e:
            self.status.result = str(e)
        self.status.end_time = time.time()
        self.status.status = Status.DONE

        self.status.stopped = True


class Task:
    """
        timer task
    """
    def __init__(self, id, name, threadcls, exclusive=False, maxkeep=10):
        """
            init task
        :param id:
        :param threadcls:
        :param exclusive:
        :param maxkeep:
        """
        # id/name for task
        self._id = id
        self._name = name

        # thread class for task
        self._threadcls = threadcls

        # exclusive flag for task
        self._exclusive =exclusive

        # max tasks keep in queue
        self._maxkeep = maxkeep

        # stop flag for task
        self._stopped = False

        # execute times
        self._times = 0

        # task execute histories
        self._tasks = []

    @property
    def id(self):
        return self._id

    def schedule(self, tm):
        """
            schedule task
        :param tm: float, current timestamp
        :return:
        """
        pass

    def config(self):
        """
            timer configure
        :return:
        """
        pass

    def execute(self):
        """
            execute task
        :return:
        """
        # check if there is running object
        if self._exclusive:
            for t in self._tasks:
                if t.is_alive():
                    return

        # create & start task runnable object
        t = self._threadcls()
        t.start()

        # add to task queue end
        self._tasks.append(t)

        # add execute times
        self._times += 1

        # remove header task
        if len(self._tasks) > self._maxkeep:
            for i in range(0, len(self._tasks)):
                if self._tasks[i].status.stopped is not None and self._tasks[i].status.stopped:
                    self._tasks.pop(i)
                    break

    def joinall(self):
        """
            join all task
        :return:
        """
        for t in self._tasks:
            if t.is_alive():
                t.join(0)

    def info(self):
        """
            get task information
        :return:
        """
        return {
            'id': self._id,
            'name': self._name,
            'class': self._threadcls.__name__,
            'config': self.config(),
            'times': self._times,
            'maxkeep': self._maxkeep,
            'exclusive': self._exclusive,
            'stopped': self._stopped,
        }

    def status(self):
        """
            get task runable object status
        :return:
        """
        results = []

        for t in self._tasks:
            results.append(t.getstatus())

        return results

    def enable(self):
        """
            enable task
        :return:
        """
        self._stopped = False

    def disable(self):
        """
            disable task
        :return:
        """
        self._stopped = True

    @property
    def stopped(self):
        return self._stopped

    def tolist(self, obj):
        """
            if obj is tupple/list
        :param obj:
        :return:
        """
        if obj is None:
            return []

        if isinstance(obj, list) or isinstance(obj, tuple):
            return list(obj)

        return [obj]


class CrondTask(Task):
    """
        crontab task
    """
    def __init__(self, id, name, threadcls, min=None, hour=None, day=None, month=None, week=None, exclusive=False, maxkeep=10):
        """
            init a crontab task
        :param id: str, task identifier
        :param threadcls: class, thread subclass
        :param min: int/int array: 0~59
        :param hour:int/int array : 0~23
        :param day: int/int array: 1~31
        :param month: int/int array: 1~12
        :param week: int/int array: 1~7
        :param exclusive: bool
        :param maxkeep: int
        """
        # time scheduler of task
        self._min = self.tolist(min)
        self._hour = self.tolist(hour)
        self._day = self.tolist(day)
        self._month = self.tolist(month)
        self._week = self.tolist(week)

        # last time execute
        self._last_execute_time = datetime.datetime.now()

        # init super class
        Task.__init__(self, id, name, threadcls, exclusive, maxkeep)

    def expired(self, tm):
        """

        :param tm:
        :return:
        """
        # get date time by @tm
        dt = datetime.datetime.fromtimestamp(tm)

        # check last execute time
        lt = self._last_execute_time
        if dt.month==lt.month and dt.day==lt.day and dt.hour==lt.hour and dt.minute==lt.minute:
            return False

        # check if expired
        if (len(self._month)==0 or dt.month in self._month)\
            and (len(self._day)==0 or dt.day in self._day)\
            and (len(self._week)==0 or dt.weekday()+1 in self._week)\
            and (len(self._hour)==0 or dt.hour in self._hour)\
            and (len(self._min)==0 or dt.minute in self._min):
            return True

        return False

    def schedule(self, tm):
        """
            schedule task
        :param tm:
        :return:
        """
        if not self.stopped and self.expired(tm):
            # execute task
            self.execute()
            # update last execute timestamp
            self._last_execute_time = datetime.datetime.fromtimestamp(tm)

    def config(self):
        """
            crontab configure
        :return:
        """
        return 'min%s/hour%s/day%s/month%s/week%s' % (str(self._min), str(self._hour), str(self._day), str(self._month), str(self._week))


class TimerTask(Task):
    """
        timer task
    """
    def __init__(self, id, name, threadcls, interval, exclusive=False, maxkeep=10):
        """
            init a timer task
        :param id: str, task identifier
        :param threadcls:
        :param interval:
        :param exclusive:
        :param maxkeep:
        """
        # timer interval in seconds
        self._interval = interval

        # last execute timestamp
        self._last_execute_time = time.time()

        # init super class
        Task.__init__(self, id, name, threadcls, exclusive, maxkeep)

    def expired(self, tm):
        """
            check if task has expired
        :param tm: float, current timestamp
        :return:
        """
        if tm - self._last_execute_time > self._interval:
            return True
        return False

    def schedule(self, tm):
        """
            schedule task
        :param tm:
        :return:
        """
        if not self.stopped and self.expired(tm):
            # execute task
            self.execute()
            # update last execute timestamp
            self._last_execute_time = tm

    def config(self):
        """
            timer task configure
        :return:
        """
        return 'interval: %f S' % self._interval


class Timer(threading.Thread):
    """
        timer scheduler and executor
    """
    def __init__(self):
        """
            init timer
        """
        self._lock = threading.RLock()
        self._tasks = []
        self._stopped = False

        threading.Thread.__init__(self)

    def setup(self, id, name, threadcls, min=None, hour=None, day=None, month=None, week=None, interval=None, exclusive=False, maxkeep=10):
        """
            setup a timer task
        :param threadcls:
        :param min:
        :param hour:
        :param day:
        :param month:
        :param week:
        :param interval:
        :param exclusive:
        :param maxkeep:
        :return:
        """
        self._lock.acquire()

        if interval is not None:
            task = TimerTask(id, name, threadcls, interval, exclusive, maxkeep)
        else:
            task = CrondTask(id, name, threadcls, min, hour, day, month, week, exclusive, maxkeep)

        self._tasks.append(task)

        self._lock.release()

    def enable(self, id):
        """
            enable a task
        :param id:
        :return:
        """
        self._lock.acquire()

        for t in self._tasks:
            if t.id == id:
                t.enable()
        self._lock.release()

    def disable(self, id):
        """
            disable a task
        :param id:
        :return:
        """
        self._lock.acquire()

        for t in self._tasks:
            if t.id == id:
                t.disable()
        self._lock.release()

    def execute(self, id):
        """
            execute a task
        :param id:
        :return:
        """
        self._lock.acquire()
        for t in self._tasks:
            if t.id == id:
                t.execute()
        self._lock.release()

    def status(self, id=None):
        """
            get status of timer
        :param id:
        :return:
        """
        # get timer status
        if id is None:
            results = []
            for t in self._tasks:
                results.append(t.info())
            return results

        # get specified task status
        for t in self._tasks:
            if t.id == id:
                return t.status()

        return []

    def stop(self):
        """
            stop timer
        :return:
        """
        self._lock.acquire()
        self._stopped = True
        self._lock.release()

    def run(self):
        """
            timer thread for schedule tasks
        :return:
        """
        while not self._stopped:
            # schedule tasks
            self._schedule()

            # sleep for a while
            time.sleep(0.5)

    def _schedule(self):
        self._lock.acquire()

        # schedule all tasks
        for task in self._tasks:
            # schedule task
            task.schedule(time.time())
            # join task
            task.joinall()

        self._lock.release()


#default timer object
default = Timer()
