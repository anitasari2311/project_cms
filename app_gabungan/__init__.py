from flask import Flask, render_template, redirect, url_for, request, json, session
import auth
from microservice2 import ms2
from microservice1 import RequestLaporan
from templatelaporan import TemplateLaporan
import pymysql
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'session1'

##########################                  LOGIN                          ############################

@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')




#########################                   MICROSERVICE 1                 ###############################


## Menampilkan menu utama user
@app.route('/user', methods=['GET','POST'])
def user():
    # if request.method =='POST':
    #     request_id = request.form['btnCancel']

        
        listRequestLaporanUser = RequestLaporan()
        return render_template('menu.html', listReqUser = listRequestLaporanUser.listRequestUser(session['user_id']))


### Untuk Button Cancel di Menu User
@app.route('/cancel', methods = ['POST'])
def cancel():
    if request.method == 'POST':

        cancel = RequestLaporan()
        request_id = request.form['btnCancel']

        return redirect(url_for("user", listReqUser = cancel.listRequestUser(session['user_id']),cancel_request = cancel.cancelRequest(request_id)))


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

@app.route('/revisi', methods = ['GET', 'POST'])
def revisi():
    revisi = TemplateLaporan()
    revisi_id = request.form['btnRevisi']
    cur = revisi.getRevisiDisplay(revisi_id)
    return render_template("EditRevisi.html",listrevisidisplay = cur)














#######################                  MICROSERVICE 2             #################################


@app.route('/menu2')
def menu2():
    return render_template('taskSPV.html')

@app.route('/task')
def task():
    availTask = ms2()
    return render_template('task2.html', listAvailTask = availTask.availableTask(), listTask = availTask.listTask())

@app.route('/detailReq', methods=['GET', 'POST'])
def detailReq():
    detTask = ms2()
    request_id = request.form['buttonDetail']
    cur = detTask.getDetailTask(request_id)
    return render_template('detailTask.html', detail_task = cur)


###########################################PROSES
@app.route('/authLogin', methods=['GET','POST'])
def authLogin():
    auth.auth_login()
    return auth.auth_login()

@app.route('/listAvailTask', methods=['GET','POST'])
def listAvailTask():
    microservice2.listTask()
    return microservice2.listTask()

@app.route ('/openDetail', methods=['GET','POST'])
def openDetail():
    ms2().detailTask()
    return ms2().detailTask()

@app.route('/confirm1', methods = ['POST','GET'])
def confirm1():
    if request.method == 'POST':

        confirm = ms2()
        request_id = request.form['btnConfirmReq']

        return redirect(url_for("task", listAvailTask = confirm.availableTask(), confirmRequest = confirm.confirmRequest(request_id)))









if __name__ == "__main__":
    app.run(debug=True)
