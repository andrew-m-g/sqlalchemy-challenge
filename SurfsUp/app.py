# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import date, timedelta
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

most_recent_date = date(2017, 8, 23)
one_year_ago = most_recent_date - timedelta(days=365)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all avalible API routes"""
    return (
                f"/api/v1.0/precipitation"
                f"/api/v1.0/stations"
                f"/api/v1.0/tobs"
                f"/api/v1.0/temp/<start>"
                f"/api/v1.0/temp/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    #query 12 months of precip data
    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= one_year_ago
    ).all()
    #convert to dict.
    precipitation_dict = {date: prcp for date, prcp in results}
    #close session
    session.close()
    # Return the JSON rep of the dcit
    return jsonify(precipitation_dict)
    

@app.route("/api/v1.0/stations")
def stations():
    #query stations
    station_list = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    stations_list = [{"station": station, "name": name} for station, name in station_list]
    
    #close session
    session.close()
    #return json of station dict
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station).label('count')).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first().station

    # Query the last 12 months of temperature observations for the most active station
    temp_query = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == most_active_station,
        Measurement.date >= one_year_ago
    ).all()

    # Convert the query results to a list of dictionaries
    temperature_list = [{"date": date, "temperature": tobs} for date, tobs in temp_query]
    session.close()
    # Return the JSON representation of the list
    return jsonify(temperature_list)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def temperature_stats(start, end=None):

    #return f"start: {start}, end: {end}"

        #Define the selection list for TMIN, TAVG, TMAX
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end:
        # Calculate TMIN, TAVG, TMAX for dates from the start date to the end date, inclusive
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        # Calculate TMIN, TAVG, TMAX for dates greater than or equal to the start date
        results = session.query(*sel).filter(Measurement.date >= start).all()

    # Convert the query results to a list
    temperature_stats_list = list(np.ravel(results))
    session.close()
    # Return the JSON representation of the list
    return jsonify(temperature_stats_list)


if __name__ == "__main__":
    app.run(debug=True)