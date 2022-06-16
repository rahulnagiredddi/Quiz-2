from decimal import Decimal
import pyodbc
import datetime as dt
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

driver = '{ODBC Driver 18 for SQL Server}'
server = 'assignment-2.database.windows.net'
database = 'adb_summer_assignments'
username = 'adb-sql-database'
password = 'Admin@_2022'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server +
                      ';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()


@app.route("/")
def hello_world():
    cursor.execute("SELECT * FROM [dbo].[earthquake]")
    num = cursor.fetchall()
    return render_template('index.html', num=num)


@app.route('/Filter', methods=['GET', 'POST'])
def Filter():
    if request.method == "POST":
        longitude = request.form["longitude"]
        degrees = request.form['degrees']
        longitude1 = int(longitude)+int(degrees)
        longitude2 = int(longitude)-int(degrees)
        print(longitude1)
        print(longitude2)
        cursor.execute(
            "SELECT * FROM [dbo].[earthquake] where longitude < "+str(longitude1)+" AND longitude >"+str(longitude2))
        print("SELECT * FROM [dbo].[earthquake] where longitude < " +
              str(longitude1)+" AND longitude >"+str(longitude2))
        result = cursor.fetchall()
    return render_template('filter.html', num=result)


@app.route('/Filter1', methods=['GET', 'POST'])
def Filter1():
    if request.method == "POST":
        minlongitude = request.form["minlongitude"]
        maxlongitude = request.form["maxlongitude"]
        degrees = request.form['number']
        longitude1 = int(minlongitude)
        longitude2 = int(maxlongitude)
        if(longitude1 > 180):
            longitude1 = 180-longitude1

        if(longitude2 > 180):
            longitude2 = 180-longitude2
        l1 = min(longitude1, longitude2)
        l2 = max(longitude1, longitude2)
        print(l1, l2)
        cursor.execute(
            "SELECT TOP "+str(degrees) + " * FROM [dbo].[earthquake] where longitude > "+str(l1)+" AND longitude <"+str(l2)+"ORDER BY mag DESC")
        result = cursor.fetchall()
        cursor.execute(
            "SELECT TOP "+str(degrees) + " * FROM [dbo].[earthquake] where longitude > "+str(l1)+" AND longitude <"+str(l2)+"ORDER BY mag ASC")
        result1 = cursor.fetchall()
    return render_template('filter.html', num=result, num1=result1)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
