#!/usr/bin/env python3
"""This script checks the temprature/humidity/preassure and put the data into a database."""
from sense_hat import SenseHat
import sys
import sqlite3
import datetime
import time
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

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(dates, temps, '-', label='Temperature (°C)', linewidth=line_width)
    ax.plot_date(dates, hums, '-', label='Humidity (%rH)', linewidth=line_width)
    ax2 = ax.twinx()
    ax2.plot_date(dates,pressures, '-', label='Atmospheric Pressure (hPa)', color='yellow', linewidth=line_width)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax2.set_ylim(990, 1010)
    ax.set_ylim(20,60)
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

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(dates, temps, '-', label='Temperature (°C)', linewidth=line_width)
    ax.plot_date(dates, hums, '-', label='Humidity (%rH)', linewidth=line_width)
    ax2 = ax.twinx()
    ax2.plot_date(dates,pressures, '-', label='Atmospheric Pressure (hPa)', color='yellow', linewidth=line_width)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax2.set_ylim(990, 1010)
    ax.set_ylim(20,60)
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

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)
    ax.plot_date(dates, temps, '-', label='Temperature (°C)', linewidth=line_width)
    ax.plot_date(dates, hums, '-', label='Humidity (%rH)', linewidth=line_width)
    ax2 = ax.twinx()
    ax2.plot_date(dates,pressures, '-', label='Atmospheric Pressure (hPa)', color='yellow', linewidth=line_width)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax2.set_ylim(990, 1010)
    ax.set_ylim(20,60)
    ax.tick_params(axis='x', labelrotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=10)
    ax2.tick_params(axis='y', labelsize=10)
    plt.savefig("/home/n00b/weather_station/static/weather_fig_7d.png", dpi=150, bbox_inches='tight', transparent=True)


def main():
    filename = "/home/n00b/weather_station/weather_station.sqlite3"
    now = datetime.datetime.now()
    temp = round(read_temp(), 1)
    time.sleep(3)
    hum = round(read_hum(), 1)
    pressure = round(read_pressure(), 1)
    write_database(filename, now.strftime('%Y-%m-%d %H:%M:%S'), temp, hum, pressure)
    create_graph(filename)
    create_graph_24h(filename)
    create_graph_7d(filename)


if __name__ == "__main__":
    main()
