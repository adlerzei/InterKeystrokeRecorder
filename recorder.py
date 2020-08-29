# Copyright (C) 2020  Christian Zei
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from csv_handler import CSVHandler
from threading import Thread
from datetime import datetime, timedelta
from pcapy import findalldevs, open_live

packet_buffer = []


def clear_packet_buffer():
    packet_buffer.clear()


def start():
    dev = get_interface()

    # Open interface for capturing.
    p = open_live(dev, 1500, 0, 100)

    # Set default BPF filter. See tcpdump(3).
    pcap_filter = ''
    p.setfilter(pcap_filter)

    print("Listening on %s: net=%s, mask=%s, linktype=%d" % (dev, p.getnet(), p.getmask(), p.datalink()))

    # Start sniffing thread and finish main thread.
    try:
        decoder_thread = DecoderThread(p, packet_buffer)
        decoder_thread.daemon = True
        decoder_thread.start()
    except KeyboardInterrupt:
        pass


def get_interface():
    # Grab a list of interfaces that pcap is able to listen on.
    # The current user will be able to listen from all returned interfaces,
    # using open_live to open them.
    ifs = findalldevs()

    # No interfaces available, abort.
    if 0 == len(ifs):
        print("You don't have enough permissions to open any interface on this system.")
        sys.exit(1)

    # Only one interface available, use it.
    elif 1 == len(ifs):
        print('Only one interface present, defaulting to it.')
        return ifs[0]

    # Ask the user to choose an interface from the list.
    count = 0
    for iface in ifs:
        print('%i - %s' % (count, iface))
        count += 1
    idx = int(input('Please select an interface: '))

    return ifs[idx]


class DecoderThread(Thread):

    def __init__(self, pcap_obj, buffer):
        self.pcap = pcap_obj
        self.packet_buffer = buffer
        self.last_datetime = datetime.now()
        self.lookup_table = {}
        self.function_lookup_table = {}

        csv_handler = CSVHandler()
        csv_handler.set_path_and_file_name("csv/", "lookupTable.csv")
        self.lookup_table.update(csv_handler.read_csv_to_dict())
        csv_handler.set_path_and_file_name("csv/", "functionLookupTable.csv")
        self.function_lookup_table.update(csv_handler.read_csv_to_dict())

        try:
            t = Thread.__init__(self)
        except KeyboardInterrupt:
            pass

    def run(self):
        # Sniff ad infinitum.
        # PacketHandler shall be invoked by pcap for every packet.
        try:
            self.pcap.loop(0, self.packet_handler)
        except KeyboardInterrupt:
            pass

    def packet_handler(self, hdr, data):
        # Display the packet in human-readable form.
        timestamp = hdr.getts()[0]
        microseconds = timedelta(microseconds=hdr.getts()[1])
        dt_object = datetime.fromtimestamp(timestamp) + microseconds

        timestamp_delta = timedelta()
        if self.packet_buffer:
            timestamp_delta = dt_object - self.last_datetime

        sniff_intervals = round((timestamp_delta.seconds * 1000000 + timestamp_delta.microseconds) / 15000)

        modifier_key_scan_code = str(data.hex()[30:32])
        list_of_scan_codes = [data.hex()[i:i + 2] for i in range(34, len(data.hex()), 2)]

        modifier_key = self.function_lookup_table[data.hex()[30:32]] if data.hex()[
                                                                 30:32] in self.function_lookup_table else "(error)"
        list_of_keys = []
        for i in range(34, len(data.hex()) - 2, 2):
            pressed_key = self.lookup_table[data.hex()[i:i + 2]] if data.hex()[
                                                                     i:i + 2] in self.lookup_table else "(error)"
            list_of_keys.append(pressed_key)

        self.packet_buffer.append([timestamp_delta, sniff_intervals,
                                   modifier_key_scan_code, list_of_scan_codes,
                                   modifier_key, list_of_keys])
        self.last_datetime = dt_object
