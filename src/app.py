import os
import pandas as pd
import numpy as np

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from dotenv import load_dotenv

from model.getUnit import getUnits
from model.position import position
from model.reportByHour import reportByHour
from model.sensorTracing import sensorTracing
from model.report import getReport
from controllers.modelHour import modelHour
from controllers.calculus import getConsumed

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": os.getenv('URL')}})
units = getUnits()

@app.route('/api/units', methods=['GET'])
def getUnits():
    return jsonify(units)


if (__name__ == "__main__"):
    app.run(debug=True, host='0.0.0.0', port=8083)
