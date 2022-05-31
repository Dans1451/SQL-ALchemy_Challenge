
from unittest import result
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt
from datetime import datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement


app=Flask(__name__)

@app.route("/")
def index():
    return(
        f"/api/v1.0/precipitation"    
        f"/api/v1.0/stations"    
        f"/api/v1.0/tobs"   
        f"/api/v1.0/<start>  date format mm-dd-yyyy"     
        f"/api/v1.0/<start>/<end>  date format mm-dd-yyyy"     
    )


@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close
    all_dates = []
    for date, prcp in results:
        results_dict={}
        results_dict["date"] = date
        results_dict["prcp"] = prcp
        all_dates.append(results_dict)
    return jsonify(all_dates)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(measurement.station).all()
    session.close
    all_results=list(np.ravel(results))
    return jsonify(all_results)


@app.route("/api/v1.0/tobs")
def active():
    session = Session(engine)
    active= session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).all()
    session.close
    active_df=pd.DataFrame(active, columns = ['Station', 'Count'])
    sorted_active_df=active_df.sort_values(by='Count', ascending=False, ignore_index=True)
    sorted_active_df
    most_active=sorted_active_df.loc[0,'Station']
    date=session.query(measurement).order_by(measurement.date.desc()).first()
    date.date
    desc_meas=session.query(measurement).order_by(measurement.date.desc())
    lastest_date=session.query(measurement).order_by(measurement.date.desc()).first().date
    year_before=dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results=session.query(measurement.tobs).\
        filter(measurement.date > year_before).\
        filter(measurement.date<lastest_date).\
        filter(measurement.station==most_active).all()
    all_results=list(np.ravel(results))
    return jsonify(all_results)

@app.route('/api/v1.0/<start_date>')
def start(start_date):
    start_date = datetime.strptime(start_date, "%m-%d-%Y")
    session = Session(engine)
    results =session.query(measurement.tobs).filter(measurement.date >= start_date).all()
    all_results=list(np.ravel(results))
    # return jsonify(all_results)
    session.close
    tmin = min(all_results)
    tmax = max(all_results)
    tavg= np.average(all_results)
    return(f'Minimum is {tmin}, the maximum is {tmax} and the average is {tavg}')
    #return jsonify(start_results)

@app.route('/api/v1.0/<start_date>/<end_date>') 

def date_range(start_date, end_date):
    start_date = datetime.strptime(start_date, "%m-%d-%Y")
    end_date = datetime.strptime(end_date, "%m-%d-%Y")
    session = Session(engine)
    results=session.query(measurement.tobs).\
        filter(measurement.date > start_date).\
        filter(measurement.date < end_date).all()
    session.close
    date_range_results=list(np.ravel(results))
    tmin = min(date_range_results)
    tmax = max(date_range_results)
    tavg= sum(date_range_results)/len(date_range_results)
    return(f'Minimum is {tmin}, the maximum is {tmax} and the average is {tavg}')
    # return jsonify(results)




if __name__ == "__main__":
    app.run(debug=True)
