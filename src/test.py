import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from main import login
from model.getResource import getResources
from model.getUnit import getUnits
from model.getZones import getZones
from model.getGeocerca import geocerca
from model.report import getReport
from model.stop import getStop
from model.sensorTracing import sensorTracing
from controllers.calculus import getConsumed
from controllers.getStopsBetweenTrips import getStopsBetweenTrips
from controllers.calculus import getStops
from datetime import datetime, timedelta
import time
path='../db'
units = getUnits()