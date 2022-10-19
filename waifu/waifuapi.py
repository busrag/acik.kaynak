from email import message
import re
from flask import Flask, render_template
import http.client


conn = http.client.HTTPSConnection("api.waifu.im")

payload = ""

conn.request("GET", "/random?is_nsfw=false", payload)

res = conn.getresponse()
data = res.read()

a = data.decode("utf-8")

app = Flask(__name__)

print("\n")

print(a)

print("\n")

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug= True)
