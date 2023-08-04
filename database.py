import pyodbc
import json

DBQ = 'D:\BESPOKE TSR\MData.mdb' #DB Location - Change it later
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBQ+';')

class Bespoke():
    def sale(date):
        cur = conn.cursor()
        cur.execute("SELECT * FROM salesmast")
        print(cur.fetchall())

    def item(code):
        cur = conn.cursor()
        ITEM_CODE = code
        cur.execute(f"SELECT citname FROM item WHERE citcode='{code}'")
        ITEM_NAME = cur.fetchone()[0]
        cur.execute(f"SELECT nsalerate,nprrate FROM itembatch WHERE citbatcode='{code}'")
        ITEM_SALE_RATE, ITEM_PURCHASE_RATE = cur.fetchone()

        return ITEM_CODE, ITEM_NAME, ITEM_PURCHASE_RATE, ITEM_SALE_RATE
    
    def item_list():
        cur = conn.cursor()
        ITEM_LIST = []
        cur.execute("SELECT citcode FROM item ORDER BY citcode ASC;")
        for i in cur.fetchall():
            ITEM_LIST.append(i[0])

        return ITEM_LIST


# Bespoke.sale(date="15")
# cp = Bespoke.item(code="P2393")
cp = Bespoke.item_list()
print(cp)