import copy


class PrettyPrintHandler(object):

    def __init__(self):

        self._last_values = None

    def out(self, _, f):

        msg = """\
HV: {hv}, Total: {proc_stat_time_total:.2f} (+ {proc_stat_time_total_diff:.5f}), \
Total Children: {proc_stat_time_total_children:.2f} (+ {proc_stat_time_total_children_diff:.5f}), \
Threads: {proc_tasks_active} / {proc_tasks_total}, CPUs: {sys_cpu_count_active} / {sys_cpu_count} \
""".format(**f)

        print(msg)