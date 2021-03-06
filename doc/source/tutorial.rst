How to Use This Program
=======================

Installation
------------

This program can be installed using pip. To install, ``cd`` into the
project's root directory. This is the directory where the ``setup.py`` file
is located. Then, run

.. sourcecode:: bash

    pip install .

This will install Mr Freeze, along with the minimum amount of dependencies
required for the program to run. The third-party dependencies will be
fetched from PyPI_, so installation will usually require an internet
connection. The connection requirement can be avoided by downloading python
wheels for the dependencies, and installing them prior to installing Mr Freeze.


Usage
-----

This program reports data from three instruments and logs it to a csv file.
Before running, ensure that you have permission to access all the required
ports. It is assumed that connections will be made over emulated serial ports.
The order with which the devices are added is determined by the OS when
connected. It doesn't matter which device maps to which file, but you will
need to remember the mapping

Example Setup
~~~~~~~~~~~~~

The following setup worked on a Thinkpad running Ubuntu 16.04.

1. Connect the Lakeshore 475 gaussmeter.
2. Run

    .. sourcecode:: bash

        chmod ug+rw /dev/ttyUSB0

    This command will allow the owner of the port and the group of the port
    to read and write to the serial port. In my case, the group of the port
    was ``dialout``.
3. Connect the Cryogmagnetics LM-510 level meter, and set the required
    permissions as in step 2.
4. Connect the Cryomagnetics 4G power supply.
5. Run

    .. sourcecode:: bash

        python mr_freeze --gaussmeter-address=/dev/ttyUSB0
        --ln2-gauge-address=/dev/ttyUSB1 --power-supply-adress=/dev/ttyUSB2

    This will start the application. The results will be written to a file
    ``result-<date>.csv``, where ``<date>`` is the current date and time.
6. Stop the process by sending ``SIGINT``.

.. _PyPI: https://pypi.python.org/pypi
