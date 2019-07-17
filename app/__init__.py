from flask import Flask, render_template, redirect, url_for, request
from requestlaporan import RequestLaporan
import pymysql
import datetime


app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
@app.route('/')
def start():
    return redirect(url_for('login'))

#BUAT VALIDASI LOGIN
@app.route('/login')
def login():
    return render_template('login.html')

@app.route ('/menu', methods=['GET','POST'])
def menu():
    newRequest = RequestLaporan()
    error = None
    if request.method == 'POST':
        flag = newRequest.prosesLogin(request.form['username'], request.form['password'])
        print(flag)
        if flag is "incorrect":
            error = 'Invalid Username/Password.'
            return render_template('login.html',error = error)
        elif flag == 'admin':
            return render_template('menu.html')
        elif flag == 'User':
            return render_template('menu.html')
        elif flag == 'Atasan':
            return render_template('menu.html')
   


#BUAT CALL REQUEST
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


