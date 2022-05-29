# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link
session = Session(engine)

# set up flask
app = Flask(__name__)

#create app route
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Create Precipitation Analysis route
@app.route("/api/v1.0/precipitation")

# Create precipitation function
def precipitation():
    
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >=prev_year).all()

    # Format results into a JSON structure
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create Station Analysis route
@app.route("/api/v1.0/stations")

# Create station function
def stations():

    # Perform a query to retrieve the stations
    results = session.query(Station.station).all()

    # Format results into a JSON structure
    stations = list(np.ravel(results))
    return jsonify(station=stations)

# Create temperature observations  route
@app.route("/api/v1.0/tobs")

# Create temperature function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create statistics function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)