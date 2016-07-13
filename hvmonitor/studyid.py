import etcd
import threading
import logging

log = logging.getLogger(__name__)


class StaticID(object):

    def __init__(self, study_id):
        self._study_id = study_id

    def get(self):
        return self._study_id


class EtcdID(object):

    def __init__(self, etcd_ip):

        import etcd

        self._etcd = etcd.Client(host=etcd_ip, port=2379, read_timeout=0)
        self._study_id = "ETCDERROR"

        # Start an etcd watch thread
        self._watch_th = threading.Thread(target=EtcdID.watch, args=(self,))
        self._watch_th.start()

    def watch(self):

        while True:
            self._study_id = self._etcd.watch("/hvbench/globals/study_id").value
            log.info("Changing study id to '%s'" % self._study_id)

    def get(self):
        return self._study_id
