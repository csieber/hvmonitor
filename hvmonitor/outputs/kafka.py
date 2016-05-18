import kafka
from kafka import KafkaProducer
import json
import logging

log = logging.getLogger(__name__)


class KafkaHandler(object):

    def __init__(self, address, topic):

        log.info("Connecting to kafka at %s.." % address)

        try:
            self._kafka = KafkaProducer(bootstrap_servers=address)
        except kafka.common.KafkaUnavailableError:
            log.error("Failed to connect to kafka at %s!" % address)
            raise

        self._topic = topic

    def out(self, study_id, measurement):

        measurement['study_id'] = study_id

        message = json.dumps(measurement)

        self._kafka.send(self._topic, message.encode('ASCII'))
