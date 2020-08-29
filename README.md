# InterKeystrokeRecorder

This program can be used to record training data for the InterKeystrokeAnalyzer. The training data consits of the latencies between successive Bluetooth packets and their respective content. This programm includes parts of the BluetoothKeySniffer.

## Requirements

1. A Python interpreter (recommended version 3 or higher)
2. [Libpcap](https://www.tcpdump.org/) 0.9.3 or newer
3. A C++ compiler, e.g. [GCC G++](http://gcc.gnu.org/) 2.95

## Dependencies

To run this program, you need to install the following Python libraries:

  * [pcapy](https://pypi.org/project/pcapy/)
  * [termcolor](https://pypi.org/project/termcolor/)
  * [readchar](https://pypi.org/project/readchar/)
  
### Installation

These packages can be installed by using your favorite packet manager. For instance, if you use [pip](https://pip.pypa.io/en/stable/), just run the following command:

```shell
pip install pcapy termcolor readchar
```

## Usage

In the following, sample instructions are given to execute the relevant parts of the program. Sample code, how the program can be used, can be found in the file:

  * **data_study.py**
  
Within this file it is possible to select the tasks, that should be conducted in the data study. To do so, it is sufficient to comment/uncomment the corresponding lines.

To run the data study, just execute the following command in a terminal:

```shell
sudo python data_study.py
```

After the data study as been finished, the recorded data can be found in the ```./out/``` folder. If you want to pause the recording process, you can stop the program at any time. To resume it later on, just enter the same participant number at the beginning.

