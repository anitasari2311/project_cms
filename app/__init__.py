from flask import Flask, render_template, redirect, url_for, request
from requestlaporan import RequestLaporan
import pymysql
import datetime

app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'

@app.route('/')
def menu():
	return render_template('login.html')

@app.route ('/login', methods=['GET','POST'])
def login():
	error = 'None'
	if request.method == 'POST':
		if request.form['username'] !='admin' or request.form['password'] !='admin123':
			error='Invalid credentials. Please try again.'
		else:
			return redirect(url_for('menu'))
	return render_template('login.html', error=error)


@app.route('/formRequest', methods=['GET', 'POST'])
def formRequest():
   # newRequest.requestLaporanBaru
    return render_template("requestLaporan.html")

@app.route('/newReq', methods = ['POST'])
def newReq():
     if request.method == 'POST':
            newRequest = RequestLaporan()
           
            title = request.form['inputTitle']
            purpose = request.form['inputPurpose']
            description = request.form['keteranganlaporan']
            Organization = request.form['Organization']
            Department = request.form['Department']
            Display = request.form['inputDisplay']
            Period = request.form['inputPeriode']
            tanggalSelesai = request.form['tanggalSelesai']
            bulanSelesai = request.form['bulanSelesai']
            tahunSelesai = request.form['tahunSelesai']
            inputFile = request.form['inputFile']


            newRequest.requestLaporanBaru( 'P190402', 'A123', 'J345', 'Y927', 'K271', title, description,
                              purpose, Display, Period, datetime.date(int(tanggalSelesai),int(bulanSelesai),int(tahunSelesai) ), "\bin",
                                None, None)
            return render_template("menu.html")


if __name__ == "__main__":
    app.run(debug=True)


