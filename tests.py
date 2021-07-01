import unittest
import app

from hardware.soil_monitor import _MockedSoilMonitor
from services.health import HealthService

class TestHealth(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
    
    def test_home(self):
        result = self.app.get('/')
        assert b'saturation' in result.data
        assert b'temp' in result.data

    def test_health(self):
        result = self.app.get('/health')
        assert b'Mocked Soil Monitor' in result.data
        assert b'uptime' in result.data
        result_json  = result.get_json()
        assert result_json['uptime'] >= 0

if __name__ == '__main__':
    unittest.main()