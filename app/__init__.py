from flask import Flask, render_template, redirect, url_for, request, json, session
from requestlaporan import RequestLaporan
import pymysql
import datetime


app = Flask(__name__, static_folder='app/static')
app.secret_key = 'session1'
app.static_folder = 'static'



@app.route('/')
def start():
    return redirect(url_for('login'))

#BUAT VALIDASI LOGIN
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/atasanprogrammer', methods=['GET','POST'])
def atasan():
     return render_template('taskSPV.html')

@app.route('/programmer', methods=['GET','POST'])
def programmer():
     return render_template('task2.html')

@app.route('/user', methods=['GET','POST'])
def user():
    listRequestLaporanUser = RequestLaporan()
    return render_template('menu.html', listReqUser = listRequestLaporanUser.listRequestUser(session['username']))

@app.route ('/menu', methods=['GET','POST'])
def menu():
    newRequest = RequestLaporan()
    error = None
    session['username'] = request.form['username']
    session['user_ID'] = newRequest.getUserID( request.form['username'])
    if request.method == 'POST':
        flag = newRequest.prosesLogin(request.form['username'], request.form['password'])
        print(flag)
        if flag is "incorrect":
            error = 'Invalid Username/Password.'
            return render_template('login.html',error = error)
        elif flag == 'Admin':
            return redirect(url_for('programmer'))
        elif flag == 'User':
            return redirect(url_for('user'))
        elif flag == 'Atasan':
            return redirect(url_for('atasan'))


#BUAT CALL REQUEST
@app.route('/formRequest', methods=['GET', 'POST'])
def formRequest():
    newRequest = RequestLaporan()
    return render_template("requestLaporan.html", listOrg = newRequest.namaOrganisasi(), listDept = newRequest.namaDept())

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


            newRequest.requestLaporanBaru( None, session['user_ID'], Organization, Department, 'K271', title, description,
                             purpose, Display, Period, datetime.date(int(tanggalSelesai),int(bulanSelesai),int(tahunSelesai) ), "\bin",
                                None, None)
            return render_template("menu.html",listReqUser = newRequest.listRequestUser(session['username']))

#EDIT REQUEST
@app.route('/editRequest')
def edit():
    # if request.method == 'POST':
    editLaporan = RequestLaporan()

     #    kodeLaporan = request.form['kodeLaporan']

    #     editLaporan.getReportID()
    return render_template("Edit2.html", listKodeReport = editLaporan.getReportID())
    
    
@app.route('/formEdit', methods=['GET', 'POST'])
def formEdit():
    editLaporan = RequestLaporan()
    return render_template("EditKolom.html")

@app.route('/newEdit', methods = ['POST'])
def newEdit():
    if request.method == 'POST':
        editLaporan = RequestLaporan()

        newDisplay = request.form['inputNewDisplay']
        filterBaru = request.form['inputFilter']
        

if __name__ == "__main__":
    app.run(debug=True)


