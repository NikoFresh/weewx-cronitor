#
#    Copyright (c) 2021-2023 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""
'ping' cronitor on every archive record.
See, https://cronitor.io/docs

Configuration:
[Cronitor]
    # Whether the service is enabled or not.
    # Valid values: True or False
    # Default is True.
    # enable = True

    # The host to 'ping'
    # Default is cronitor.link/p
    # host = cronitor.link/p

    # The name for the tracker
    # Default is Weewx
    # device_name = Weewx

    # The Cronitor api_key
    api_key = REPLACE_ME

    # The http request timeout
    # The default is 10
    # timeout = 10
"""

import logging
import socket
import threading

from urllib.request import urlopen

import weewx
import weeutil.logger
from weewx.engine import StdService
from weewx.reportengine import ReportGenerator

from weeutil.weeutil import to_bool, to_int

VERSION = "0.2"

log = logging.getLogger(__name__)
def setup_logging(logging_level, config_dict):
    """ Setup logging for running in standalone mode."""
    if logging_level:
        weewx.debug = logging_level

    weeutil.logger.setup('wee_Cronitor', config_dict)

def logdbg(msg):
    """ Log debug level. """
    log.debug(msg)

def loginf(msg):
    """ Log informational level. """
    log.info(msg)

def logerr(msg):
    """ Log error level. """
    log.error(msg)

def send_ping(host, api_key, device_name, timeout, ping_type=None):
    """Send the Cronitor 'ping'."""
    if ping_type:
        url = f"https://{host}/{api_key}/{device_name}?{ping_type}"
    else:
        url = f"https://{host}/{api_key}/{device_name}"

    try:
        urlopen(url, timeout=timeout)
    except socket.error as exception:
        logerr(f"Ping failed: {exception}")

class CronitorService(StdService):
    """ A service to ping a cronitor server.. """
    def __init__(self, engine, config_dict):
        super(CronitorService, self).__init__(engine, config_dict)

        # service_dict = config_dict.get('HealthChecks', {})
        skin_dict = self.config_dict.get('StdReport', {}).get('Cronitor', {})

        self.enable = to_bool(skin_dict.get('enable', True))
        if not self.enable:
            loginf("Not enabled, exiting.")
            return

        self.host = skin_dict.get('host', 'cronitor.link/p')
        self.timeout = to_int(skin_dict.get('timeout', 10))
        self.device_name = skin_dict.get('device_name', 'Weewx')
        if not self.device_name:
            raise ValueError("device_name option is required.")
        self.api_key = skin_dict.get('api_key')
        if not self.api_key:
            raise ValueError("api_key option is required.")

        self._thread = None

        send_ping(self.host, self.api_key, self.device_name, self.timeout, "start")

        # possible option to run as a service only
        # self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)
        # self._thread = HealthChecksServiceThread(self.host, self.api_key, self.timeout)
        # self._thread.start()

    def new_archive_record(self, event): # Need to match signature pylint: disable=unused-argument
        """The new archive record event."""
        self._thread.threading_event.set()

    def shutDown(self):
        """Run when an engine shutdown is requested."""
        loginf("SHUTDOWN - initiated")

        send_ping(self.host, self.api_key, self.device_name, self.timeout, "fail")
        loginf("fail ping sent")

        if self._thread:
            loginf("SHUTDOWN - thread initiated")
            self._thread.running = False
            self._thread.threading_event.set()
            self._thread.join(20.0)
            if self._thread.is_alive():
                logerr(f"Unable to shut down {self._thread.name} thread")

            self._thread = None

class CronitorServiceThread(threading.Thread):
    """A service to send 'pings' to a Cronitor server. """
    def __init__(self, host, api_key, device_name, timeout):
        threading.Thread.__init__(self)

        self.running = False

        self.host = host
        self.device_name = device_name
        self.api_key = api_key
        self.timeout = timeout

        self.threading_event = threading.Event()

    def run(self):
        self.running = True

        while self.running:
            self.threading_event.wait()
            send_ping(self.host, self.api_key, self.device_name, self.timeout)
            self.threading_event.clear()

        loginf("exited loop")

class CronitorGenerator(ReportGenerator):
    """Class for managing the cronitor generator."""
    def __init__(self, config_dict, skin_dict, *args, **kwargs):
        """Initialize an instance of CronitorGenerator"""
        weewx.reportengine.ReportGenerator.__init__(self, config_dict, skin_dict, *args, **kwargs)

        self.host = skin_dict.get('host', 'cronitor.link/p')
        self.timeout = to_int(skin_dict.get('timeout', 10))
        self.device_name = skin_dict.get('device_name', 'Weewx')
        if not self.device_name:
            raise ValueError("device_name option is required.")
        self.api_key = skin_dict.get('api_key')
        if not self.api_key:
            raise ValueError("api_key option is required.")

    def run(self):
        send_ping(self.host, self.api_key, self.device_name, self.timeout)

if __name__ == "__main__":
    pass
