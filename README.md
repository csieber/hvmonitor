# hvmonitor - Resource usage monitor for SDN hypervisors

A resource monitor for network hypervisors designed to work with in combination with the [hvbench](https://github.com/csieber/hvbench) framework.

## Features

  - Auto-detection of FlowVisor, OVX and OpenvSwitches processes
  - Records CPU, RAM and network resource usage with high precision (using /proc filesystem)
  - Specify PID to monitor manually
  - Modules to report ressource usage to the console or remotely locations via kafka
  - Easy extensible with additional output modules

## Dependencies

  - psutil
    - will be replaced soon by a custom and lightweight implementation
  - kafka-python (optional)
  - etcd (optional)

## Install

To install for deployment:

```
python3 setup.py install
```

To install for development:

```
python3 setup.py develop
```

## Quickstart

Run hvmonitor to start the application:

```bash
python3 hvmonitor.py
```

If the hypervisor is not detected automatically, you can specify it manually using the PID:

```bash
python3 hvmonitor.py 34123
```

In order to use kafka for central logging, use the **-k** and **-ka** switches:

```bash
python3 hvmonitor.py -k --kafka-address 192.168.34.1
```

## Usage

```
usage: hvmonitor.py [-h] [-v] [-f FREQUENCY] [-k] [-ka KAFKA_ADDRESS]
                    [-kt KAFKA_TOPIC] [-fp] [-p] [-s STUDY]

Resource monitor for SDN hypervisors.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable debug log.
  -f FREQUENCY, --frequency FREQUENCY
                        Monitoring frequency in Hz. (Default: 1)
  -k, --kafka           Activate kafka output.
  -ka KAFKA_ADDRESS, --kafka-address KAFKA_ADDRESS
                        IP of kafka.
  -kt KAFKA_TOPIC, --kafka-topic KAFKA_TOPIC
                        Kafka topic to publish to.
  -fp, --fileprint      Print data to a file.
  -p, --print           Activate print output.
  -s STUDY, --study STUDY
                        Study identifier of the measurements.
```
