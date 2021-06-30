from flask import Flask
from services.soil import SoilService
from services.health import HealthService

app = Flask(__name__)

soil_service = SoilService()
health_service = HealthService()

@app.route("/")
def root():
    return soil_service.get_soil_status()

@app.route("/health")
def health():
    return health_service.get_health()