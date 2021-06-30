from ..hardware.soil_monitor import SoilMonitor

soil_monitor = SoilMonitor()

class SoilService():
    """
    Service class to interact with the soil monitor implementation
    and generate data for the service endpoint.

    ...
    Methods
    -------
    get_soil_status() -> dict
        Returns a dictionary with the `saturation` and `temp` keys
    """

    def get_soil_status(self):
        """
        Returns a dictionary with the `saturation` and `temp` keys

        Returns
        -------
        soil_status : dict
            Returns the saturation as a percentage and the temp in degrees celcius
        """

        saturation = soil_monitor.get_soil_saturation()
        temp = soil_monitor.get_air_temp()

        return {
            'saturation': saturation,
            'temp': temp
        }