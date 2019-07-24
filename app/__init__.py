from flask import Flask, render_template, redirect, url_for, request, json, session
from requestlaporan import RequestLaporan
from templatelaporan import TemplateLaporan
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
            error = 'Invalid Username or Password!'
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
            # tanggalSelesai = request.form['tanggalSelesai']
            # bulanSelesai = request.form['bulanSelesai']
            # tahunSelesai = request.form['tahunSelesai']
            deadline = request.form['deadline']
            inputFile = request.form['inputFile']


            newRequest.requestLaporanBaru( None, session['user_ID'], Organization, Department, 'K271', title, description,
                             purpose, Display, Period, deadline, "\bin",
                                None, None)
            return render_template("menu.html",listReqUser = newRequest.listRequestUser(session['username']))

#EDIT REQUEST
@app.route('/editRequest',methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        newRequest = TemplateLaporan()
        return render_template("Edit2.html", listKodeReport = newRequest.getReportID())
    
    
@app.route('/formEdit', methods=['POST','GET'])
def formEdit():
        newRequest = TemplateLaporan()
        session['kodeLaporan'] = request.form['kodeLaporan']
        print("test",session['kodeLaporan'])
        cur = newRequest.getCurrentDisplay(session['kodeLaporan'])
        return render_template("EditKolom.html",listcurrentdisplay = cur)

@app.route('/newEdit', methods = ['POST'])
def newEdit():
    if request.method == 'POST':
        newRequest = RequestLaporan()

        filterBaru = request.form['inputFilterBaru']
        newDisplay = request.form['inputNewDisplay']
        deadline = request.form['deadline']
        # tanggalSelesai = request.form['tanggalSelesai']
        # bulanSelesai = request.form['bulanSelesai']
        # tahunSelesai = request.form['tahunSelesai']
        #inputFile = request.form['inputFile']


        newRequest.requestEditLap( None, session['user_ID'],session['kodeLaporan'], 'K271', filterBaru,
                             newDisplay, deadline, "\bin",
                                None, None)
        
        return render_template("menu.html",listReqUser = newRequest.listRequestUser(session['username']))

if __name__ == "__main__":
    app.run(debug=True)


