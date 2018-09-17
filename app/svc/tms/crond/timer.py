"""
    timer for scheduler and execute tasks
"""
import threading, time, datetime, logging


class ConditionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class TimerError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class Runnable:
    def execute(self, seq):
        pass


class _Status:
    # status
    TODO, DOING, DONE = 'todo', 'doing', 'done'

    def __init__(self):
        self.status = _Status.TODO # executor status

        self.estime = None # execute start time
        self.eetime = None # execute end time
        self.estatus = None # execute status
        self.eresult = None # execute result

        self.retime = None # runnable end time
        self.rstatus = None # runnable status
        self.rresult = None # runnable result


class _Executor(threading.Thread):
    """
        timer task executor
    """
    # sequence number
    SEQ = 0

    def __init__(self, runnable):
        """
            init executor
        :param runnable:
        """
        self._seq = _Executor.nextseq()
        self._runnable = runnable
        self._status = _Status()

        super().__init__()

    @staticmethod
    def nextseq():
        _Executor.SEQ += 1
        return _Executor.SEQ

    @property
    def seq(self):
        return self._seq

    def run(self):
        """
            thread run method
        :return:
        """
        self._status.status = _Status.DOING

        self._status.estime = time.time()
        try:
            # do something
            self._status.estatus, self._status.eresult = self._runnable.execute(self._seq)
        except Exception as e:
            self._status.estatus, self._status.eresult = False, str(e)
        self._status.eetime = time.time()

        self._status.status = _Status.DONE

    def done(self):
        """
            check if executor has done
        :return:
        """
        if self._status.status == _Status.DONE:
            return True
        return False

    def notify(self, rstatus, rresult):
        """
            notify runnable execute results
        :param rstatus:
        :param rresult:
        :return:
        """
        self._status.retime = time.time()
        self._status.rstatus = rstatus
        self._status.rresult = rresult

    def status(self):
        """
            get runnable task status
        :return:
        """
        return {
            'seq': self._seq,
            'status': self._status.status,

            'estime':self._status.estime,
            'eetime':self._status.eetime,
            'estatus': self._status.estatus,
            'eresult': self._status.eresult,

            'retime': self._status.retime,
            'rstatus': self._status.rstatus,
            'rresult': self._status.rresult,

            'alive':self.is_alive()
        }


class _Unit:
    """
        time condition unit
    """
    def __init__(self, unitstr, minval, maxval):
        """

        :param values:
        """
        self._values = []
        if unitstr is not None:
            values = unitstr.split(',')
            for value in values:
                if value.isdigit():
                    value = int(value)
                    if value<minval or value>maxval:
                        raise ConditionError('time condition unit value %s error' % unitstr)

                    self._values.append(value)

    @staticmethod
    def parse(unitstr, minval, maxval):
        """
            parse unit object
        :param unitstr:
        :param minval:
        :param maxval:
        :return:
        """
        units = unitstr.split('/')
        if len(units) == 1:
            return _UnitEqual(units[0], minval, maxval)
        elif len(units) == 2:
            return _UnitEvery(units[1], minval, maxval)
        else:
            raise ConditionError('time condition unit value %s error' % unitstr)

    def match(self, value):
        """

        :param value:
        :return:
        """
        pass


class _UnitEqual(_Unit):
    """
        time condition unit
    """
    def match(self, value):
        """

        :param value:
        :return:
        """
        if len(self._values) == 0 or value in self._values:
            return True
        return False

    def __str__(self):
        if len(self._values) == 0:
            return '*'

        svalues = []
        for v in self._values:
            svalues.append(str(v))

        return ','.join(svalues)


class _UnitEvery(_Unit):
    """
        time condition unit
    """
    def match(self, value):
        """

        :param value:
        :return:
        """
        if len(self._values) == 0:
            return True

        for val in self._values:
            if val != 0 and value % val == 0:
                return True

        return False

    def __str__(self):
        if len(self._values) == 0:
            return '*/*'

        svalues = []
        for v in self._values:
            svalues.append(str(v))

        return '*/'+','.join(svalues)


class _Cond:
    """
        time task expire condition
    """
    # minutes, hours, days, months, weeks
    UNITS = 5

    def __init__(self, condstr):
        """

        :param conditions:
        """
        units = condstr.split()
        if len(units) != _Cond.UNITS:
            raise ConditionError('time conditions must be equals with %s' % str(_Cond.UNITS))

        self._minutes = _Unit.parse(units[0], 0, 59)
        self._hours = _Unit.parse(units[1], 0, 23)
        self._days = _Unit.parse(units[2], 1, 31)
        self._months = _Unit.parse(units[3], 1, 12)
        self._weeks = _Unit.parse(units[4], 1, 7)

    def __str__(self):
        return '%s %s %s %s %s' % (str(self._minutes), str(self._hours), str(self._days), str(self._months), str(self._weeks))

    def config(self):
        """
            condition configure
        :return:
        """
        return {
            'min': str(self._minutes),
            'hour': str(self._hours),
            'day': str(self._days),
            'mon': str(self._months),
            'week': str(self._weeks)
        }

    def match(self, dt):
        """
            check timestamp if match the condition
        :param dt: datetime
        :return:
        """
        if self._minutes.match(dt.minute) and self._hours.match(dt.hour) and self._days.match(dt.day) and self._months.match(dt.month) and self._weeks.match(dt.isoweekday()):
            return True

        return False


class _Tick:
    def __init__(self):
        self._last = datetime.datetime.now()

    def match(self, dt):
        if dt.isoweekday()==self._last.isoweekday() and dt.month==self._last.month  and dt.day==self._last.day and dt.hour==self._last.hour and dt.minute==self._last.minute:
            return True

        return False

    def reset(self, dt):
        self._last = dt


class _Task:
    """
        timer base task
    """
    """
         timer task
     """

    def __init__(self, id, name, runnable, exclusive, maxkeep):
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

        # runnable object for timer task
        self._runnable = runnable

        # exclusive flag for task, set true for limit 1 same task
        self._exclusive = exclusive

        # max tasks keep in queue
        self._maxkeep = maxkeep

        # stop flag for task
        self._stopped = False

        # execute count & latest execute time
        self._count = 0
        self._latest = None

        # task execute histories
        self._executors = []

    @property
    def id(self):
        return self._id

    @property
    def stopped(self):
        return self._stopped

    def execute(self):
        """
            execute task
        :return:
        """
        # check if there is running object
        if self._exclusive:
            for t in self._executors:
                if t.is_alive():
                    return

        # create new executor to run the runnable object
        executor = _Executor(self._runnable)
        executor.start()

        # add to task queue end
        self._executors.append(executor)

        # add execute times
        self._count += 1
        self._latest = int(time.time())

        # remove header task
        if len(self._executors) > self._maxkeep:
            for i in range(0, len(self._executors)):
                if self._executors[i].done():
                    self._executors.pop(i)
                    break

    def notify(self, seq, status, result):
        """
            notify runnable status
        :param seq:
        :return:
        """
        for executor in self._executors:
            if seq == executor.seq:
                executor.notify(status, result)
                break

    def join(self):
        """
            join all task
        :return:
        """
        for t in self._executors:
            if t.is_alive():
                t.join(0)

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

    def status(self):
        """
            get task status
        :return:
        """
        return {
            'id': self._id,
            'name': self._name,
            'count': self._count,
            'latest': self._latest,
            'maxkeep': self._maxkeep,
            'exclusive': self._exclusive,
            'stopped': self._stopped,
        }

    def detail(self):
        """
            get task runable object status
        :return:
        """
        results = []

        for executor in self._executors:
            results.append(executor.status())

        return results


class _CrondTask(_Task):
    """
        crontab task
    """
    def __init__(self, id, name, condstr, runnable, exclusive=False, maxkeep=10):
        """
            init timer task
        :param id:
        :param name:
        :param condstr:
        :param runnable:
        :param exclusive:
        :param maxkeep:
        """
        # timer task
        super().__init__(id, name, runnable, exclusive, maxkeep)

        # time condition
        self._cond = _Cond(condstr)

        # last expired time point
        self._tick = _Tick()

    def schedule(self, tm):
        """
            schedule task
        :param tm:
        :return:
        """
        if not self.stopped and self._expired(tm):
            # execute task
            self.execute()
            # reset tick time
            self._reset(tm)

    def status(self):
        """
            get task status
        :return:
        """
        results = super().status()
        results['conifg'] = str(self._cond)
        return results

    def _expired(self, tm):
        """

        :param tm:
        :return:
        """
        # get date time by @tm
        dt = datetime.datetime.fromtimestamp(tm)

        # check if has expired already
        if self._tick.match(dt):
            return False

        # check if match time condition
        if self._cond.match(dt):
            return True

        return False

    def _reset(self, tm):
        """
            reset last tick
        :param tm:
        :return:
        """
        self._tick.reset(datetime.datetime.fromtimestamp(tm))


class _TimerTask(_Task):
    """
        timer task
    """
    def __init__(self, id, name, interval, runnable, exclusive=False, maxkeep=10):
        """

        :param id:
        :param name:
        :param runnable:
        :param interval:
        :param exclusive:
        :param maxkeep:
        """
        # timer interval in seconds
        self._interval = int(interval)

        # last execute timestamp
        self._last_execute_time = time.time()

        # init super class
        super().__init__(id, name, runnable, exclusive, maxkeep)

    def schedule(self, tm):
        """
            schedule task
        :param tm:
        :return:
        """
        if not self.stopped and self._expired(tm):
            # execute task
            self.execute()
            # update last execute timestamp
            self._last_execute_time = tm

    def status(self):
        results = super().status()
        results['conifg'] = str(self._interval)
        return results

    def _expired(self, tm):
        """
            check if task has expired
        :param tm: float, current timestamp
        :return:
        """
        if tm - self._last_execute_time > self._interval:
            return True
        return False


class _Timer(threading.Thread):
    """
        timer scheduler and executor, including timer task and crontab task
    """
    def __init__(self):
        """
            init timer
        """
        self._lock = threading.RLock()
        self._tasks = {}
        self._stopped = False

        threading.Thread.__init__(self)

    def add(self, id, name, condstr, runnable, exclusive=False, maxkeep=10):
        """

        :param id:
        :param name:
        :param condstr:
        :param runnable:
        :param exclusive:
        :param maxkeep:
        :return:
        """
        if not isinstance(condstr, int) and not isinstance(condstr, str):
            raise ConditionError('timer setup condition not valid')

        with self._lock:
            if self._tasks.get(id) is not None:
                raise TimerError('timer task with id: %s has exist' % str(id))

            if isinstance(condstr, int) or condstr.isdigit():
                task = _TimerTask(id, name, condstr, runnable, exclusive, maxkeep)
            else:
                task = _CrondTask(id, name, condstr, runnable, exclusive, maxkeep)

            self._tasks[id] = task

    def delete(self, id):
        """
            delete a timer task
        :param id:
        :return:
        """
        with self._lock:
            if self._tasks.get(id) is None:
                raise TimerError('time task with id: %s not exist' % (str(id)))

            self._tasks.pop(id)

    def clear(self):
        """
            clear all tasks
        :return:
        """
        with self._lock:
            self._tasks.clear()

    def exist(self, id):
        """
            check if task with @id has exist
        :param id:
        :return:
        """
        with self._lock:
            if self._tasks.get(id) is not None:
                return True
            return False

    def enable(self, id):
        """
            enable a task
        :param id:
        :return:
        """
        with self._lock:
            t = self._tasks.get(id)
            if t is None:
                raise TimerError('time task with id: %s not exist' % (str(id)))
            t.enable()

    def disable(self, id):
        """
            disable a task
        :param id:
        :return:
        """
        with self._lock:
            t = self._tasks.get(id)
            if t is None:
                raise TimerError('time task with id: %s not exist' % (str(id)))
            t.disable()

    def execute(self, id):
        """
            execute a task
        :param id:
        :return:
        """
        with self._lock:
            t = self._tasks.get(id)
            if t is None:
                raise TimerError('time task with id: %s not exist' % (str(id)))
            t.execute()

    def notify(self, id, seq, status, result):
        """
            notify runnable execute result
        :param id:
        :param seq:
        :return:
        """
        with self._lock:
            t = self._tasks.get(id)
            if t is None:
                raise TimerError('time task with id: %s not exist' % (str(id)))
            t.notify(seq, status, result)

    def status(self, id=None):
        """
            get status of timer
        :param id:
        :return:
        """
        results = []
        with self._lock:
            # get timer status
            if id is None:
                for t in self._tasks.values():
                    results.append(t.status())
            else:
                # get specified task status
                t = self._tasks.get(id)
                if t is None:
                    raise TimerError('time task with id: %s not exist' % (str(id)))
                results.append(t.status())

        return results

    def detail(self, id):
        """
            get detail of task by @id
        :param id:
        :return:
        """
        with self._lock:
            t = self._tasks.get(id)
            if t is None:
                raise TimerError('time task with id: %s not exist' % (str(id)))

            return t.detail()

    def stop(self):
        """
            stop timer
        :return:
        """
        with self._lock:
            self._stopped = True

    def run(self):
        """
            timer thread for schedule tasks
        :return:
        """
        while not self._stopped:
            try:
                # schedule tasks
                self._schedule()

                # sleep for a while
                time.sleep(0.5)
            except Exception as e:
                logging.error(str(e))

    def _schedule(self):
        with self._lock:
            # schedule all tasks
            for task in self._tasks.values():
                # schedule task
                task.schedule(time.time())
                # join task
                task.join()

# default timer object
default = _Timer()


# demo task
class _TimerDemoTask(Runnable):
    def execute(self, seq):
        print('timer demo task %s' % str(seq))


class _CrondDemoTask(Runnable):
    def execute(self, seq):
        print('crond demo task %s' % str(seq))


if __name__ == '__main__':
    default.start()

    default.add('abc', 'timerdemo', 1, _TimerDemoTask())
    default.add('efg', 'cronddemo', '*/2 * * * *', _CrondDemoTask())

    while True:
        time.sleep(60)
        print(default.status())
