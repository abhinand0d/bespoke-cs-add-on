import pyodbc
import json

DBQ = 'D:\BESPOKE TSR\MData.mdb' #DB Location - Change it later
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBQ+';')

class Bespoke():
    def sale(date):
        cur = conn.cursor()
        cur.execute("SELECT * FROM salesmast")
        print(cur.fetchall())

Bespoke.sale(date="15")