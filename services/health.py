import time  
import os

from .soil import SoilMonitor

class HealthService:
    """
    Service class to generate health information about
    the system itself as well as its current configuration

    ...
    Methods
    -------
    get_health() -> dict
        Returns a dictionary with the `saturation` and `temp` keys
    """

    def __init__(self):
        self._start_time = time.time()
        self._soil_monitor = SoilMonitor()

    def _get_total_app_uptime_seconds(self):
        return int(time.time() - self._start_time)

    def _get_current_soil_monitor(self):
        return self._soil_monitor.get_name()

    def get_health(self) -> dict:
        """
        Returns a dict object that returns the `uptime` and
        `soil_monitor` implementation

        Returns
        -------
        health : dict
            Returns a dict with the uptime and current soil monitor implementation
        """
        return {
            'uptime': self._get_total_app_uptime_seconds(),
            'soilMonitor': self._get_current_soil_monitor()
        }