"""
Implements a Cryomagnetics 4G Power supply for InstrumentKit
"""
from mr_freeze.devices.abstract_cryomagnetics_device \
    import AbstractCryomagneticsDevice
import quantities as pq
from time import sleep
import re
import logging

log = logging.getLogger(__name__)


class Cryomagnetics4G(AbstractCryomagneticsDevice):
    """
    Base class for a Cryomagnetics 4G Superconducting Magnet Power supply
    """
    CHANNELS = {1, 2}

    UNITS = {
        "A": pq.amp,
        "G": pq.gauss
    }

    REVERSE_UNITS = {
        pq.amp: "A",
        pq.gauss: "G"
    }

    MAXIMUM_MESSAGE_SIZE = 1000

    instrument_measurement_timeout = 0.5

    @property
    def terminator(self):
        """

        :return: The termination character for the device. The terminator is
         the carriage return character (ASCII 10), followed by the newline
         character (ASCII 13)
        """
        return '\n'

    @property
    def unit(self):
        """
        The power supply is capable of expressing the output current going
        into the magnet in amperes, but it can also convert the current to a
        predicted magnetic field using a particular relation.

        :return: The units in which the power supply expresses its measurement
        """
        response = self.query("UNITS?")
        return self.UNITS[response]

    @unit.setter
    def unit(self, unit_to_set):
        """
        Set the unit to either amperes or gauss. The valid units to which
        this value can be set are the keys in the ``UNITS`` dictionary of
        this object

        :param str unit_to_set: The unit to set
        :raises: :exc:`ValueError` if the unit cannot be set
        """
        if unit_to_set not in self.UNITS.keys():
            raise ValueError("Attempted to set unit to an invalid value")
        self.query("UNITS %s" % unit_to_set)

    @property
    def current(self):
        """

        :return: The current in amperes being sent out of the power supply
        """
        self.unit = self.REVERSE_UNITS[pq.amp]
        sleep(self.instrument_measurement_timeout)

        return self.parse_current_response(self.query("IOUT?"))

    @staticmethod
    def parse_current_response(response):
        value_match = re.search("^(\d|\.)*(?=(A|G))", response)
        unit_match = re.search(".(?=$)", response)

        value = float(value_match.group(0))
        unit = Cryomagnetics4G.UNITS[unit_match.group(0)]

        return_value = value * unit

        log.debug("parsed quantity %s from response %s", return_value, unit)

        return return_value
