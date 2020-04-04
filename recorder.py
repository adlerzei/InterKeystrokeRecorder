import sys
import csv
from threading import Thread
from datetime import datetime, timedelta
from pcapy import findalldevs, open_live

packet_buffer = []


def clear_packet_buffer():
    packet_buffer.clear()


def read_csv(path, csv_dict):
    with open(path, mode='r') as infile:
        reader = csv.reader(infile, delimiter=";")
        csv_dict.update(dict((str(rows[0]), str(rows[1])) for rows in reader))


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
        DecoderThread(p, packet_buffer).start()
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
    show_only_key_code = False  # e.g. "z"
    show_only_key_value = True  # e.g. "1c"

    def __init__(self, pcap_obj, buffer):
        self.pcap = pcap_obj
        self.packet_buffer = buffer
        self.packets_captured = 0
        self.last_datetime = datetime.now()
        self.lookup_table = {}
        self.function_lookup_table = {}

        read_csv("csv/lookupTable.csv", self.lookup_table)
        read_csv("csv/functionLookupTable.csv", self.function_lookup_table)

        try:
            Thread.__init__(self)
        except KeyboardInterrupt:
            pass

    # def read_csv(self, path, function_path):
    #     with open(path, mode='r') as infile:
    #         reader = csv.reader(infile, delimiter=";")
    #         self.lookup_table = dict((str(rows[0]), str(rows[1])) for rows in reader)
    #     with open(function_path, mode='r') as infile:
    #         reader = csv.reader(infile, delimiter=";")
    #         self.function_lookup_table = dict((str(rows[0]), str(rows[1])) for rows in reader)

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
        if self.packets_captured != 0:
            timestamp_delta = dt_object - self.last_datetime

        list_of_keys = []
        modifier_key = ""
        if DecoderThread.show_only_key_code:
            modifier_key = str(data.hex()[30:32])
            list_of_keys = [data.hex()[i:i + 2] for i in range(34, len(data.hex()), 2)]
        elif DecoderThread.show_only_key_value:
            modifier_key = self.function_lookup_table[data.hex()[30:32]] if data.hex()[
                                                                     30:32] in self.function_lookup_table else "(error)"
            for i in range(34, len(data.hex()) - 2, 2):
                pressed_key = self.lookup_table[data.hex()[i:i + 2]] if data.hex()[
                                                                         i:i + 2] in self.lookup_table else "(error)"
                list_of_keys.append(pressed_key)
        else:
            list_of_keys = [data.hex()[i:i + 2] for i in range(0, len(data.hex()), 2)]

        self.packet_buffer.append([dt_object, timestamp_delta, modifier_key, list_of_keys])
        self.packets_captured += 1
        self.last_datetime = dt_object
