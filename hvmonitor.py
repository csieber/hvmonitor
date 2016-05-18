import argparse
from hvmonitor.core import Monitor, hv_pid
import logging

log = logging.getLogger(__name__)


if __name__ == "__main__":

    description = "Resource monitor for SDN hypervisors."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument( "-v", "--verbose", help="Enable debug log.", dest='verbose', action='store_true')
    parser.add_argument( "-f", "--frequency", type=int, default=1, help="Monitoring frequency in Hz. (Default: 1)")
    parser.add_argument( "-k", "--kafka", action='store_true', help="Activate kafka output.")
    parser.add_argument("-ka", "--kafka-address", type=str, default="127.0.0.1", help="IP of kafka.")
    parser.add_argument("-kt", "--kafka-topic", type=str, default="hvmonitor", help="Kafka topic to publish to.")
    parser.add_argument("-fp", "--fileprint", action='store_true', help="Print data to a file.")
    parser.add_argument("-p", "--print", action='store_true',  help="Activate print output.")
    parser.add_argument("-pp", "--pretty-print", action='store_true',  help="Activate pretty print output.")
    parser.add_argument("-s", "--study", type=str, default="default", help="Study identifier of the measurements.")
    parser.add_argument("-e", "--etcd-study", action="store_true", help="Use etcd to get the current study identifier.")
    parser.add_argument("-ea", "--etcd-address", type=str, default="127.0.0.1", help="IP of etcd.")
    parser.add_argument('pid', type=int, default=0, nargs="?", help='The PID to monitor (disables HV autodetect).')

    args = parser.parse_args()

    logconf = {'format': '[%(asctime)s.%(msecs)-3d: %(name)-16s - %(levelname)-5s] %(message)s',
               'datefmt': "%H:%M:%S"}

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, **logconf)
    else:
        logging.basicConfig(level=logging.INFO, **logconf)

    if args.pid:
        pid = args.pid
        hv_type = "(not detected)"
    else:
        hv_type, pid = hv_pid()

    outputs = []

    if args.print:

        log.info("Using print output.")

        from hvmonitor.outputs.stdout import PrintHandler
        outputs.append(PrintHandler())

    if args.kafka:

        log.info("Using kafka output.")

        from hvmonitor.outputs.kafka import KafkaHandler
        outputs.append(KafkaHandler("%s:9092" % args.kafka_address,
                                    args.kafka_topic))

    if args.fileprint:

        log.info("Using file output.")

        from hvmonitor.outputs.file import fileHandler
        outputs.append(fileHandler())

    if not outputs and not args.pretty_print:

        log.warn("No output is set. Activating pretty print output.")

        args.pretty_print = True

    if args.pretty_print:

        log.info("Using pretty print output.")

        from hvmonitor.outputs.prettyprint import PrettyPrintHandler
        outputs.append(PrettyPrintHandler())

    if args.etcd_study:

        log.info("Using etcd to determine the current study id.")

        from hvmonitor.studyid import EtcdID
        study_id = EtcdID(args.etcd_address)

    else:

        log.info("Using a fixed study ID.")

        from hvmonitor.studyid import StaticID
        study_id = StaticID(args.study)

    m = Monitor(pid, hv_type, study_id, outputs=outputs)

    m.run(args.frequency)
