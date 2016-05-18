import os

CLOCK_TICKS = os.sysconf("SC_CLK_TCK")


def find_process(name):

    result = []

    for d in os.listdir("/proc/"):

        if not d.isdigit():
            continue

        try:
            with open("/proc/%s/cmdline" % d) as f:
                cmdline = f.read()
        except FileNotFoundError:
            continue

        if name in cmdline:
            result.append(Process(d))

    return result


class Process(object):

    def __init__(self, pid):
        self._pid = int(pid)
        self._cmdline = None
        self._last = None

        self._tasks_cache = {}

    def pid(self):
        return self._pid

    def statistics(self):

        diff_fields = []

        ret = {}

        stat = self.__getitem__('stat')
        sched = self.__getitem__('sched')

        ret.update({'stat_%s' % k: v for k, v in stat.items()})
        ret.update({'sched_%s' % k: v for k, v in sched.items()})

        diff_fields.extend(["stat_%s" % f for f in stat.keys()])
        diff_fields.extend(["sched_%s" % f for f in sched.keys()])

        ret['tasks'] = {}

        for t in self.tasks():
            try:
                ret['tasks'][t.pid()] = t.statistics()
            except FileNotFoundError:
                pass

        if self._last is not None:
            ret.update({"%s_diff" % f: ret[f] - self._last[f] for f in diff_fields})
        else:
            ret.update({"%s_diff" % f: 0 for f in diff_fields})

        ret['tasks_active'] = sum([1 for task in ret['tasks'].values() if task['stat_time_total_diff'] > 0.01])
        ret['tasks_total'] = len(ret['tasks'])

        #ret['cmd_line'] = self.__getitem__("cmdline")

        self._last = ret.copy()

        return ret

    def __getitem__(self, name):

        if name == "stat":
            values = self.parse_stat("/proc/%d/stat" % self._pid)
        elif name == "sched":
            values = self.parse_sched("/proc/%d/sched" % self._pid)
        elif name == "cmdline":
            if not self._cmdline:
                with open("/proc/%d/cmdline" % self._pid) as f:
                    self._cmdline = f.read()
            values = self._cmdline.replace('\00', ' ')
        else:
            raise NotImplementedError()

        return values

    def __repr__(self):
        return "(%d) %s" % (self._pid, self.__getitem__("cmdline"))

    def tasks(self):

        base = "/proc/%d/task/" % self._pid

        for d in os.listdir(base):
            if d not in self._tasks_cache:
                self._tasks_cache[d] = Task(self, d)

        return self._tasks_cache.values()

    @staticmethod
    def parse_stat(fname):

        with open(fname, 'r') as f:
            contents = f.read().split(" ")

        pos = {"utime": 13,
               "stime": 14,
               "cutime": 15,
               "cstime": 16,
               "num_threads": 19}

        tick_fields = ["utime", "stime", "cutime", "cstime"]

        ret = {k: float(contents[v]) for k, v in pos.items()}

        for t in tick_fields:
            ret[t] /= CLOCK_TICKS

        ret['time_total'] = ret['utime'] + ret['stime']
        ret['time_total_children'] = ret['cutime'] + ret['cstime']

        return ret

    @staticmethod
    def parse_sched(fname):

        with open(fname, 'r') as f:
            contents = f.read().split("\n")

        metrics = {}
        for c in contents[2:-4]:
            split = c.split(":")
            metrics[split[0].strip()] = float(split[1].strip())

        # Only consider those metrics
        mfilter = ["se.sum_exec_runtime"]

        metrics = {k: v for k, v in metrics.items() if k in mfilter}

        return metrics


class Task(object):

    def __init__(self, process, task_pid):
        self._process = process
        self._task_pid = int(task_pid)

        self._last = None

    def pid(self):
        return self._task_pid

    def statistics(self):

        diff_fields = []

        ret = {}

        stat = self.__getitem__('stat')
        sched = self.__getitem__('sched')

        ret.update({'stat_%s' % k: v for k, v in stat.items()})
        ret.update({'sched_%s' % k: v for k, v in sched.items()})

        diff_fields.extend(["stat_%s" % f for f in stat.keys()])
        diff_fields.extend(["sched_%s" % f for f in sched.keys()])

        if self._last is not None:
            ret.update({"%s_diff" % f: ret[f] - self._last[f] for f in diff_fields})
        else:
            ret.update({"%s_diff" % f: 0 for f in diff_fields})

        self._last = ret.copy()

        return ret

    def __getitem__(self, name):

        if name == "stat":
            values = Process.parse_stat("/proc/%d/task/%d/stat" % (self._process.pid(), self._task_pid))
        elif name == "sched":
            values = Process.parse_sched("/proc/%d/task/%d/sched" % (self._process.pid(), self._task_pid))
        else:
            raise NotImplementedError("'%s' is not implemented." % name)

        return values
