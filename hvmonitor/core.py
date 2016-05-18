import psutil
import time
from datetime import datetime
import pytz
import logging
from hvmonitor.exceptions import NoHVInstanceFound
from hvmonitor.outputs.stdout import PrintHandler
import hvmonitor.proc as proc
import hvmonitor.sys as sys

log = logging.getLogger(__name__)


def hv_pid():

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(['name', 'pid', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        else:
            if any(["flowvisor" in c for c in pinfo['cmdline']]) and any(["java" in c for c in pinfo['cmdline']]):
                print("Found FlowVisor instance! (PID: %d)" % pinfo['pid'])
                return "fv", pinfo['pid']
            elif any(["OpenVirteX.jar" in c for c in pinfo['cmdline']]):
                print("Found OVX instance! (PID: %d)" % pinfo['pid'])
                return "ovx", pinfo['pid']
            elif "ovs-vswitchd" in pinfo['name']:
                print("Found OVS instance! (PID: %d)" % pinfo['pid'])
                return "ovs", pinfo['pid']

    raise NoHVInstanceFound()


class Monitor(object):

    def __init__(self, pid, hv_type, study_id, outputs=[PrintHandler()]):

        self._outputs = outputs
        self._pid = pid
        self._hv_type = hv_type
        self._study_id = study_id
        self._pproc = proc.Process(pid)

    def run(self, frequency=1):

        reference_time = datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.utc)

        while True:

            stats = {}

            start = time.perf_counter()
            stats.update({"proc_%s" % k: v for k, v in self._pproc.statistics().items()})
            log.debug("Total proc time: %fms" % ((time.perf_counter() - start)*1000))

            start = time.perf_counter()
            stats.update({"sys_%s" % k: v for k, v in sys.statistics().items()})
            log.debug("Total sys time: %fms" % ((time.perf_counter() - start)*1000))

            stats['timestamp'] = int((datetime.now(pytz.utc) - reference_time).total_seconds()*1000)
            stats['hv'] = self._hv_type

            for o in self._outputs:
                o.out(self._study_id.get(), stats)

            start = time.perf_counter()

            time.sleep(1/frequency)

            log.debug("Sleep duration: %fms" % ((time.perf_counter() - start)*1000))
