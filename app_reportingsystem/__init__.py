from flask import Flask, render_template, redirect, url_for, request, json, session
import auth
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
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))






#########################                   MICROSERVICE 1                 ###############################


## Menampilkan menu utama user
@app.route('/user', methods=['GET','POST'])
def user():
    # if request.method =='POST':
    #     request_id = request.form['btnCancel']

        
        listRequestLaporanUser = RequestLaporan()
        return render_template('menu.html', listReqUser = listRequestLaporanUser.listRequestUser(session['user_id']))

### Cancel Detail Task to menuTaskProgrammer
@app.route('/cancelTask')
def cancelTask():
    return redirect(url_for('task'))

## Jika programmer mengklik tombol Finish pada menu Task Programmer
@app.route('/finishRequest', methods = ['POST'])
def finishRequest():
    if request.method == 'POST':
        finishreq = RequestLaporan()
        request_id = request.form['finishButton']

        return redirect(url_for("task"), finishreq.finishRequest(request_id))#, finishreq.finishRequest(request_id),listAvailTask = finishreq.availableTask(), listTask = finishreq.listTask())
## Jika user mengklik tombol confirm
@app.route('/confirmRequest', methods = ['POST','GET'])
def confirmRequest():
    if request.method =='POST':
        confirm = RequestLaporan()
        request_id = request.form ['confirmReq']

        return redirect(url_for("user"), confirm.confirmRequest(request_id))






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
            inputFile = request.files['inputFile']
            inputFile.save(secure_filename(f.filename))


            newRequest.requestLaporanBaru( None, session['user_id'], Organization, Department, 'K271', title, description,
                             purpose, Display, Period, deadline, "\bin",
                                None, None)
           # return render_template("menu.html",listReqUser = newRequest.listRequestUser(session['username']))
            return redirect(url_for('user'))
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


        newRequest.requestEditLap( None, session['user_id'],session['kodeLaporan'], 'K271', filterBaru,
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
    availTask = RequestLaporan()
    return render_template('task2.html', listAvailTask = availTask.availableTask(), listTask = availTask.listTask())

@app.route('/detailReq', methods=['GET', 'POST'])
def detailReq():
    detTask = RequestLaporan()
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

# @app.route ('/openDetail', methods=['GET','POST'])
# def openDetail():
#     RequestLaporan().detailTask()
#     return RequestLaporan().getDetailTask()

@app.route('/accRequest', methods = ['POST','GET'])
def confirm1():
    if request.method == 'POST':

        confirm = RequestLaporan()
        request_id = request.form['btnConfirmReq']

        return redirect(url_for("task",  confirmReq = confirm.accRequest(request_id)))
        








if __name__ == "__main__":
    app.run(debug=True)
