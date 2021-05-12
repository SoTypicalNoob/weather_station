#!/usr/bin/env python3
"""This script checks the temprature/humidity/preassure and put the data into a database."""
from sense_hat import SenseHat
import sys
import os
import sqlite3
import datetime
import time
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')


##### Create table #####
def create_database(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS Weather")
    cur.execute(
        """CREATE TABLE Weather (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        date DATE,
        temperature REAL,
        humidity REAL,
        pressure REAL
        )
    """
    )


def create_new_table(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS OpenWeatherMap")
    cur.execute(
        """CREATE TABLE OpenWeatherMap (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        date DATE,
        temperature REAL,
        humidity REAL,
        pressure REAL
        )
    """
    )


def write_database(filename, date, temperature, humidity, pressure):
    print(filename, date, temperature, humidity, pressure)
    sep_date = date.split("-")
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Weather (
        date,
        temperature,
        humidity,
        pressure
        )
        VALUES (?, ?, ?, ?)
    """,
    (date, temperature, humidity, pressure)
    )
    conn.commit()


def write_database_openweathermap(filename, date, temperature, humidity, pressure):
    print(filename, date, temperature, humidity, pressure)
    sep_date = date.split("-")
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO OpenWeatherMap (
        date,
        temperature,
        humidity,
        pressure
        )
        VALUES (?, ?, ?, ?)
    """,
    (date, temperature, humidity, pressure)
    )
    conn.commit()


def read_database(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM Weather")
    return rows


##### Temperature #####
def read_temp():
    sense = SenseHat()
    temp = sense.get_temperature()
    return temp


##### Humidity #####
def read_hum():
    sense = SenseHat()
    hum = sense.get_humidity()
    return hum


##### Pressure #####
def read_pressure():
    sense = SenseHat()
    pressure = sense.get_pressure()
    return pressure


def create_graph(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute('SELECT date, temperature, humidity, pressure FROM Weather')
    data = cur.fetchall()

    dates = []
    temps = []
    hums = []
    pressures = []
    prev_hum = 0
    line_width = 2

    for row in data:
        dates.append(parser.parse(row[0]))
        temps.append(row[1])
        if int(row[2]) == 0:
            hums.append(pre_hum)
        else:
            hums.append(row[2])
            pre_hum = row[2]
        pressures.append(row[3])

    max_t = max(temps)
    min_t = min(temps)
    max_h = max(hums)
    min_h = min(hums)
    max_p = math.ceil(max(pressures))
    min_p = math.floor(min(pressures))
    if max_t > max_h:
        maxy = math.ceil(max_t)
        pass
    else:
        maxy = math.ceil(max_h)
        pass
    if min_t < min_h:
        miny = math.floor(min_t)
        pass
    else:
        miny = math.floor(min_h)

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(dates, temps, '-', label='Temperature (°C)', linewidth=line_width)
    ax.plot_date(dates, hums, '-', label='Humidity (%rH)', linewidth=line_width)
    ax2 = ax.twinx()
    ax2.plot_date(dates,pressures, '-', label='Atmospheric Pressure (hPa)', color='yellow', linewidth=line_width)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.set_ylim(miny, maxy)
    ax2.set_ylim(min_p, max_p)
    ax.tick_params(axis='x', labelrotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=10)
    ax2.tick_params(axis='y', labelsize=10)
    plt.savefig("/home/n00b/weather_station/static/weather_fig.png", dpi=150, bbox_inches='tight', transparent=True)


def create_graph_24h(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("SELECT date, temperature, humidity, pressure FROM Weather WHERE date > date('now', '-1 day')")
    data = cur.fetchall()

    dates = []
    temps = []
    hums = []
    pressures = []
    prev_hum = 0
    line_width = 2

    for row in data:
        dates.append(parser.parse(row[0]))
        temps.append(row[1])
        if int(row[2]) == 0:
            hums.append(pre_hum)
        else:
            hums.append(row[2])
            pre_hum = row[2]
        pressures.append(row[3])

    max_t = max(temps)
    min_t = min(temps)
    max_h = max(hums)
    min_h = min(hums)
    max_p = math.ceil(max(pressures))
    min_p = math.floor(min(pressures))
    if max_t > max_h:
        maxy = math.ceil(max_t)
        pass
    else:
        maxy = math.ceil(max_h)
        pass
    if min_t < min_h:
        miny = math.floor(min_t)
        pass
    else:
        miny = math.floor(min_h)

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(dates, temps, '-', label='Temperature (°C)', linewidth=line_width)
    ax.plot_date(dates, hums, '-', label='Humidity (%rH)', linewidth=line_width)
    ax2 = ax.twinx()
    ax2.plot_date(dates,pressures, '-', label='Atmospheric Pressure (hPa)', color='yellow', linewidth=line_width)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.set_ylim(miny,maxy)
    ax2.set_ylim(min_p, max_p)
    ax.tick_params(axis='x', labelrotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=10)
    ax2.tick_params(axis='y', labelsize=10)
    plt.savefig("/home/n00b/weather_station/static/weather_fig_24h.png", dpi=150, bbox_inches='tight', transparent=True)


def create_graph_7d(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("SELECT date, temperature, humidity, pressure FROM Weather WHERE date > date('now', '-7 day')")
    data = cur.fetchall()

    dates = []
    temps = []
    hums = []
    pressures = []
    prev_hum = 0
    line_width = 2

    for row in data:
        dates.append(parser.parse(row[0]))
        temps.append(row[1])
        if int(row[2]) == 0:
            hums.append(pre_hum)
        else:
            hums.append(row[2])
            pre_hum = row[2]
        pressures.append(row[3])

    max_t = max(temps)
    min_t = min(temps)
    max_h = max(hums)
    min_h = min(hums)
    max_p = math.ceil(max(pressures))
    min_p = math.floor(min(pressures))
    if max_t > max_h:
        maxy = math.ceil(max_t)
        pass
    else:
        maxy = math.ceil(max_h)
        pass
    if min_t < min_h:
        miny = math.floor(min_t)
        pass
    else:
        miny = math.floor(min_h)

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(dates, temps, '-', label='Temperature (°C)', linewidth=line_width)
    ax.plot_date(dates, hums, '-', label='Humidity (%rH)', linewidth=line_width)
    ax2 = ax.twinx()
    ax2.plot_date(dates,pressures, '-', label='Atmospheric Pressure (hPa)', color='yellow', linewidth=line_width)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.set_ylim(miny, maxy)
    ax2.set_ylim(min_p, max_p)
    ax.tick_params(axis='x', labelrotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=10)
    ax2.tick_params(axis='y', labelsize=10)
    plt.savefig("/home/n00b/weather_station/static/weather_fig_7d.png", dpi=150, bbox_inches='tight', transparent=True)


def create_comp_o(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("SELECT date, humidity FROM Weather WHERE date > date('now', '-7 day')")
    data1 = cur.fetchall()

    dates1 = []
    hums1 = []
    prev_hum = 0
    line_width = 2

    for row in data1:
        dates1.append(parser.parse(row[0]))
        if int(row[1]) == 0:
            hums1.append(pre_hum)
        else:
            hums1.append(row[1])
            pre_hum = row[1]

    cur.execute("SELECT date, humidity FROM OpenWeatherMap WHERE date > date('now', '-7 day')")
    data2 = cur.fetchall()

    dates2 = []
    hums2 = []
    for row in data2:
        dates2.append(parser.parse(row[0]))
        hums2.append(row[1])

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(dates1, hums1, '-', label='Humidity (%rH)', linewidth=line_width)
    ax.plot_date(dates2, hums2, '-', label='Humidity (%rH) - OpenWeatherMap', linewidth=line_width)
    ax.legend(loc='upper left')
    ax.set_ylim(20,60)
    ax.tick_params(axis='x', labelrotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=10)
    plt.savefig("/home/n00b/weather_station/static/comparison_o_fig_7d.png", dpi=150, bbox_inches='tight', transparent=True)


def get_weather_from_openweathermap():
    import json
    import requests
    response_API = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Csomor,Hungary&units=metric&appid=8cd4c675bc3663d4cb9e63e6c61f00ea')
    # print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    temp = parse_json['main']['temp']
    pressure = parse_json['main']['pressure']
    humidity = parse_json['main']['humidity']
    print(temp, pressure, humidity)
    return temp, pressure, humidity


# get CPU temperature
def get_cpu_temp():
  res = os.popen("sudo vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return t


def main():
    filename = "/home/n00b/weather_station/weather_station.sqlite3"
    now = datetime.datetime.now()
    temp = round(read_temp(), 1)
    cpu_temp = get_cpu_temp()
    temp_calibrated = temp - ((cpu_temp - temp)/0.8357)
    time.sleep(3)
    hum = round(read_hum(), 1)
    pressure = round(read_pressure(), 1)
    write_database(filename, now.strftime('%Y-%m-%d %H:%M:%S'), round(temp_calibrated, 1), hum, pressure)
    temp_o, pressure_o, humidity_o = get_weather_from_openweathermap()
    write_database_openweathermap(filename, now.strftime('%Y-%m-%d %H:%M:%S'), temp_o, humidity_o, pressure_o)
    print(round(temp_calibrated, 1))
    create_graph(filename)
    create_graph_24h(filename)
    create_graph_7d(filename)
    create_comp_o(filename)


if __name__ == "__main__":
    main()
