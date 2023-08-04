from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from BESPOKE-CS-ADD-ON"

@app.route("/item-sync",methods=["POST","GET"])
def item_sync():

    return "200 OKAY"