# -*- coding: utf-8 -*-
"""
    Modul monitor

    Dieses Modul enthält Funktionen, die das System überwachen.

"""
import psutil
import threading

import threading
from collections import deque
import time
import psutil



# http://stackoverflow.com/questions/21866951/get-upload-download-kbps-speed
def calc_ul_dl(rate, dt=3, interface='WiFi'):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    tot = (counter.bytes_sent, counter.bytes_recv)

    while True:
        last_tot = tot
        time.sleep(dt)
        counter = psutil.net_io_counters(pernic=True)[interface]
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [(now - last) / (t1 - t0) / 1000.0
                  for now, last in zip(tot, last_tot)]
        rate.append((ul, dl))
        t0 = time.time()


# http://stackoverflow.com/questions/21866951/get-upload-download-kbps-speed
def print_rate(rate):
    try:
        print 'UL: {0:.0f} kB/s / DL: {1:.0f} kB/s'.format(*rate[-1])
    except IndexError:
        'UL: - kB/s/ DL: - kB/s'


def monitor_network(debug=False):
    # http: // stackoverflow.com / questions / 21866951 / get - upload - download - kbps - speed
    transfer_rate = deque(maxlen=1)
    t = threading.Thread(target=calc_ul_dl, args=(transfer_rate,))

    t.daemon = True
    t.start()

    while True:
        if debug:
            print_rate(transfer_rate)
        time.sleep(2)


def initialise_monitor(debug=False):

    network_thread = threading.Thread(target=monitor_network, args={debug})
    network_thread.start()
