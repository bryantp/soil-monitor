from abc import ABC, abstractmethod
import os
import random
import sys

try:
    import time
    import board
    from adafruit_seesaw.seesaw import Seesaw
    print('Loaded adafruit components')
except NotImplementedError:
    # Will not run on anything other than a raspberry pi
    print('Unable to load adafruit components')

class SoilMonitorInterface(ABC):
    """
    Interface for defining interactions with soil monitor
    implementations

    ...
    Methods
    -------
    get_soil_saturation() -> int
        Returns the soil saturation as a percentage
    get_air_temp()
        Returns the air temperature in degrees celcius
    get_name()
        Returns a human readable name for the implementation
    """

    @abstractmethod
    def get_soil_saturation(self) -> int:
        """ 
        Return the soil saturation from 0 to 100 as percentage
        
        Returns
        -------
        int
            The soil saturation as a percentage
        """
        pass

    @abstractmethod
    def get_air_temp(self) -> int:
        """ 
        Return the air temperature in celcius
        
        Returns
        -------
        int
            The air temperature in degrees celcius
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """ 
        Return the name of the soil monitor
        
        Returns
        -------
        str
            The humand readable name for the soil monitor implementation
        """
        pass

class SoilMonitorFactory():
    """
    Returns an appropriate instance of a soil monitor
    for the given requested implementation

    ...
    Methods
    -------
    register_soil_monitor(key: str, soil_monitor: SoilMonitorInterface)
        Register a soil monitor implementation with a key
    get_soil_monitor(key: str)
        Returns a given soil monitor implementation for the given registered key
    """

    def __init__(self):
        self._soil_monitors = {}

    def register_soil_monitor(self, key: str, soil_monitor: SoilMonitorInterface):
        """
        Register a soil monitor implementation with a key

        Parameters
        ----------
        key : str
            The key to register the implementation with
        soil_monitor : SoilMonitorInterface
            The soil monitor implementation
        """
        self._soil_monitors[key] = soil_monitor

    def get_soil_monitor(self, key: str) -> SoilMonitorInterface:
        """
        Returns a given soil monitor implementation for the given registered key

        Parameters
        ----------
        key : str
            The key to retrieve the associated soil monitor for
        
        Returns
        -------
        SoilMonitorInterface
            The implementation of a soil monitor for the given key
        """
        soil_monitor = self._soil_monitors[key]
        if not soil_monitor:
            raise ValueError(key)
        return soil_monitor()

class SoilMonitor(SoilMonitorInterface):
    """
    Public implementation of a soil monitor that
    delegates to the appropriate hardware implementation.

    Hardware implementation is determined using an environment 
    variable `soil_monitor`

    ...
    Methods
    -------
    get_soil_saturation() -> int
        Returns the soil saturation as a percentage
    get_air_temp() -> int
        Returns the air temperature in degrees celcius
    get_name() -> str
        Returns a human readable name for the implementation
    """

    def __init__(self):
        self._soil_monitor_name = os.getenv('soil_monitor')
        if not self._soil_monitor_name:
            self._soil_monitor_name = 'mocked'
        self._soil_monitor = _soil_monitor_factory.get_soil_monitor(self._soil_monitor_name)
    
    def get_soil_saturation(self) -> int:
        """ 
        Return the soil saturation from 0 to 100 as percentage
        
        Returns
        -------
        int
            The soil saturation as a percentage
        """
        return self._soil_monitor.get_soil_saturation()

    def get_air_temp(self) -> int:
        """ 
        Return the air temperature in celcius
        
        Returns
        -------
        int
            The air temperature in degrees celcius
        """
        return self._soil_monitor.get_air_temp()

    def get_name(self) -> str:
        """ 
        Return the name of the soil monitor
        
        Returns
        -------
        str
            The humand readable name for the soil monitor implementation
        """
        return self._soil_monitor.get_name()

class _AdafruitStemmaSoilMonitor(SoilMonitorInterface):
    """ 
    Hardware implementation for the Adafruit Stemma I2C Soil Monitor

    ...

    Attributes
    ----------
    loaded : bool
        Flag used to determine if everything has been set up correctly and the monitor is ready to use

    Methods
    -------
    get_soil_saturation() -> int
        Returns the soil saturation as a percentage
    get_air_temp() -> int
        Returns the air temperature in degrees celcius
    get_name() -> str
        Returns a human readable name for the implementation
    """
    
    def __init__(self):
        self.loaded = True
        if 'board' not in sys.modules:
            print('board was not loaded')
            self.loaded = False
        if 'adafruit_seesaw.seesaw' not in sys.modules:
            print('adafruit_seesaw.seesaw was not loaded')
            self.loaded = False

        if self.loaded:
                i2c_bus = board.I2C()
                self.ss = Seesaw(i2c_bus, addr=0x36)

    def get_soil_saturation(self) -> int:
        """ 
        Return the soil saturation from 0 to 100 as percentage
        
        Returns
        -------
        int
            The soil saturation as a percentage
        """
        if self.loaded:
            return self.ss.moisture_read()
        print('Adafruit stemma device not set up, returning -1 for soil saturation')
        return -1

    def get_air_temp(self) -> int:
        """ 
        Return the air temperature in celcius
        
        Returns
        -------
        int
            The air temperature in degrees celcius
        """
        if self.loaded:
            return round(self.ss.get_temp(),1)
        print('Adafruit stemma device not set up, returning -1 for soil saturation')
        return -1 

    def get_name(self) -> str:
        """ 
        Return the name of the soil monitor
        
        Returns
        -------
        str
            The humand readable name for the soil monitor implementation
        """
        return 'Adafruit Stemma'

class _MockedSoilMonitor(SoilMonitorInterface):
    """
    Mocked soil monitor for testing and local running

    ...
    Methods
    -------
    get_soil_saturation() -> int
        Returns the soil saturation as a percentage
    get_air_temp() -> int
        Returns the air temperature in degrees celcius
    get_name() -> str
        Returns a human readable name for the implementation
    """

    def get_soil_saturation(self) -> int:
        """ 
        Return a random soil saturation from 0 to 100 as percentage
        
        Returns
        -------
        int
            The soil saturation as a percentage
        """
        return random.randint(0, 101)

    def get_air_temp(self) -> int:
        """ 
        Return a random air temperature in celcius
        
        Returns
        -------
        int
            The air temperature in degrees celcius
        """
        return random.uniform(0, 50)

    def get_name(self) -> str:
        """ 
        Return the name of the soil monitor
        
        Returns
        -------
        str
            The humand readable name for the soil monitor implementation
        """
        return 'Mocked Soil Monitor'

_soil_monitor_factory = SoilMonitorFactory()
_soil_monitor_factory.register_soil_monitor('adafruitstemma', _AdafruitStemmaSoilMonitor)
_soil_monitor_factory.register_soil_monitor('mocked', _MockedSoilMonitor)