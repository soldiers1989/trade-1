"""
    test task for timer
"""
import datetime
from app.atm import timer
from app.util import rand

class TimerTestTask(timer.Runnable):
    def do(self):
        tm = str(datetime.datetime.now())
        print("[%s]timer task" % tm)
        return tm


class CrondTestTask(timer.Runnable):
    def do(self):
        tm = str(datetime.datetime.now())
        print("[%s]crontab task" % tm)
        return tm


#timer.default.setup(rand.uuid(), '定时任务测试1', TimerTestTask, interval=2)

#timer.default.setup(rand.uuid(), '定时任务测试2', CrondTestTask)
