import os
import re


def statistics():

    c = cpu()

    ret = {"cpu_%s" % k: v for k, v in c.items()}

    return ret


def cpu():

    base = "/sys/devices/system/cpu/"

    fields = ['cpuinfo_cur_freq']

    ret = {}

    ret['count'] = 0
    ret['count_active'] = 0

    for d in os.listdir(base):
        if re.match(r"cpu[0-9]+", d) is None:
            continue

        ckey = int(d[3:])

        ret[ckey] = {}

        ret['count_active'] += 1
        ret['count'] += 1

        for field in fields:

            try:
                with open(os.path.join(base, d, "cpufreq", field)) as f:
                    ret[ckey][field] = float(f.read().strip())
            except FileNotFoundError:
                del ret[ckey]
                ret['count_active'] -= 1
                break

    return ret

if __name__ == "__main__":
    print(statistics())