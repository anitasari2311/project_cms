from flask import Flask, render_template
#from requestlaporan import RequestLaporan
import pymysql
app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'



@app.route('/request', methods=['GET', 'POST'])
def request():
    #newRequest = RequestLaporan()
   # newRequest.requestLaporanBaru
    return render_template("requestLaporan.html")

@app.route('/menu')
def menu():
    return render_template("menu.html")
if __name__ == "__main__":
    app.run(debug=True)
