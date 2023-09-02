import pyodbc
import json
import os
import requests as rq

PROFIT_PERCENTAGE = 0.33
DBQ = 'D:\BESPOKE TSR\MData.mdb' #DB Location - Change it later
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBQ+';')

with open("data/necessary_data.json","r") as f:
    data = json.load(f)
    LOCATION = data["Location"]
    # Extract Monthly Expense
    RENT = data["FixedCost"]["Rent"]
    ELECTRICITY = data["FixedCost"]["Electricity"]
    INTERNET = data["FixedCost"]["Internet"]

    TOTAL_FIXED_COST = round(((int(RENT) + int(ELECTRICITY) + int(INTERNET))/30),2)

class Bespoke():

    def sale(date):
        # Remember this will be need to be reflected in the server too
        sale = {"total_amt": 0,"Location":LOCATION,"FixedExp":TOTAL_FIXED_COST}
        total_amt = 0
        cur = conn.cursor()
        cur.execute(f"SELECT nsaleno,nsaleamt,ntotdiscamt,ccreatedtime,ceditedtime FROM salesmast WHERE dsaledate=#{date}# ORDER BY nsaleno ASC;")
        for i in cur.fetchall():
            sale[i[0]] = {"sale_amount": i[1], "discount_amount": i[2],"createdtime":i[3],"editedtime":i[4],"purchase_rate":0,"profit":0,"item_list": []}
            try: 
                total_amt += i[1]
            except:
                total_amt += 0
        sale["total_amt"] = total_amt
        if total_amt == 0:
            sale["total_amt"] = 0
            return sale
        else:
            vs = list(sale.keys())
            vs.remove("total_amt")
            vs.remove("Location")
            vs.remove("FixedExp")
            for iu in vs:
                codes = []
                price = []
                qty = []
                try:
                    cur.execute(f"SELECT citcode,nprice,nqty FROM salestran WHERE nsaleno={iu}")
                    ddp = []
                    purchase_rate = 0
                    profit_rate = 0
                    for xi in cur.fetchall():
                        citcode = xi[0]
                        nprice = xi[1]
                        nqty = xi[2]
                        piprice = nprice/nqty 
                    
                        ITEM_CODE, ITEM_NAME, _, ITEM_SALE_RATE = Bespoke.item(code=citcode)

                        if piprice != ITEM_SALE_RATE: # this will update user if the rate is different 
                            ITEM_PURCHASE_RATE = int(piprice) * (1-PROFIT_PERCENTAGE)
                            ITEM_SALE_RATE = piprice
                        
                        ITEM_PURCHASE_RATE = round(ITEM_SALE_RATE * (1-PROFIT_PERCENTAGE),2)

                        purchase_rate += ITEM_PURCHASE_RATE * nqty
                        PROFIT = (int(ITEM_SALE_RATE) - int(ITEM_PURCHASE_RATE)) * nqty
                        profit_rate += PROFIT

                        ddp.append([citcode,ITEM_NAME,nprice,nqty,ITEM_SALE_RATE,ITEM_PURCHASE_RATE,PROFIT])

                    sale[iu]["item_list"] = ddp
                    sale[iu]["purchase_rate"] = purchase_rate
                    sale[iu]["profit"] = float(profit_rate) - sale[iu]["discount_amount"]


                
                except Exception as e:
                    print(e)
        return sale

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

c = Bespoke.sale("2023-09-02")

with open("data.json","w") as f:
    json.dump(c,f)