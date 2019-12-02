from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify, send_from_directory
# from base64 import b64encode
import base64
import auth
from werkzeug.utils import secure_filename 
import pickle
import pymysql
import mysql.connector
from mysql.connector import Error
import requests
import datetime
import os
import pandas as pd
# import urllib.request
#from PIL import Image



app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'frontEnd'


# ALLOWED_EXTENSION  =  set('png','jpeg','jpg','pdf')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['UPLOAD_FINISHED_REQUEST'] = 'finishedRequest'
app.config['FOLDER_PREVIEW'] = 'previewReport'
app.config['UPLOAD_FINISHED_REQUEST'] = 'finishedRequest'
app.config['FOLDER_SCHEDULE'] = 'Schedule'



@app.route('/test')
def test():

    return render_template('order.html')

@app.route('/menubar')
def menubar():
    return render_template('tesMenuBar.html')

##########################                  LOGIN                          ############################
@app.route('/')
def home():
    return redirect (url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        
        # auth.auth_login()
        return auth.auth_login()

    return render_template('ms1login.html')

@app.route('/logout')
def logout():
    # session.clear()
    # return redirect(url_for('login'))
    return auth.logout()

@app.route('/changePass')
def changePass():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        a = session['user_id']
        print("=== [ changePass ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("======================")
        return render_template('ms1changePass.html')

@app.route('/sendDataPassword', methods=['GET', 'POST'])
def sendDataPassword():
    if request.method == 'POST':
        uId                 = session['user_id']
        passwordLama        = request.form['oldPass']
        passwordBaru        = request.form['newPass']
        konfirmasiPassword  = request.form['confPass']

        request_data = {
            'uId'       : uId,
            'passLama'  : passwordLama,
            'passBaru'  : passwordBaru,
            'konfPass'  : konfirmasiPassword
        }

        dataRequest = json.dumps(request_data)

        print("=== [ sendDataPassword ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("============================")

        if session.get('position') == 'User':
            requests.post('http://127.0.0.1:5001/updateDataPassword/'+dataRequest)
            return redirect(url_for('user'))
        elif session.get('position') == 'Admin' :
            requests.post('http://127.0.0.1:5001/updateDataPassword/'+dataRequest)
            return redirect(url_for('admin'))
        else:
            requests.post('http://127.0.0.1:5001/updateDataPassword/'+dataRequest)
            return redirect(url_for('spv'))


#=========================================================================================
#=========================================================================================
#=========================[           USER             ]==================================
#=========================================================================================
#=========================================================================================


@app.route('/user', methods=['POST','GET'])
def user():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    elif session.get('position') != 'User':
        return 'PAGE NOT FOUND', 404
    else:
        now = datetime.datetime.now()

        day = now.strftime("%A")
        clock = now.strftime("%H:%M:%S")

        print("=== [ homeUser ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("====================")

        return render_template('ms1home1.html', day=day, clock=clock)

#================[List request user]=================
@app.route('/list', methods = ['POST','GET'])
def list():
    if session.get('user_id') is None:
        return render_template('ms1Login.html')
    else:
        a = session['user_id']

        listReq     = requests.get(''.join(['http://127.0.0.1:5001/listRequestUser/'+a]))
        listResp    = json.dumps(listReq.json())
        loadListReq = json.loads(listResp)

        print("=== [ listRequestUser ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("===========================")

        return render_template('ms1listReq.html', listReqUser = loadListReq)

#==============[List request yang telah selesai ]===========
@app.route('/listFinished', methods = ['POST','GET'])
def listFinished():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        uId = session['user_id']

        listFinished = requests.get(''.join(['http://127.0.0.1:5001/listFinished/'+uId]))
        finishedResp = json.dumps(listFinished.json())
        loadFinished = json.loads(finishedResp)

        print("=== [ listFinished ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("========================")

        return render_template('ms1listFinished.html', listKelar = loadFinished)
@app.route('/downloadRequest',methods=['POST','GET'])
def downloadRequest():
    if request.method == 'POST':
        request_id=request.form['downloadButton']

        print(request_id)


        # resp=requests.get('http://127.0.0.1:5004/downloadRequest/'+request_id)


        # directory = 'C:/Request/'

        # if not os.path.exists(directory):
        #     os.makedirs(directory)
 
        # output = open(directory+request_id+'.xls', 'wb')
        # output.write(resp.content)
        # output.close()
        return send_from_directory(app.config['UPLOAD_FINISHED_REQUEST'],request_id+'.xls', attachment_filename=request_id+'.xls', as_attachment=True)
        # return  'OK'

#============[Read Report]========================
@app.route('/readReport', methods=['POST','GET'])
def readReport():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        uId = session['user_id']

        eml         = requests.get('http://127.0.0.1:5001/getEmail/'+uId)
        emlResp     = json.dumps(eml.json())
        loadEmail   = json.loads(emlResp)
        for i in loadEmail:
            emailUser = i[0]

        

        listRep         = requests.get('http://127.0.0.1:5004/viewReport/'+emailUser)
        listResp        = json.dumps(listRep.json())
        loadListReport  = json.loads(listResp)

        print("=== [ readReport ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("======================")
        return render_template('ms4viewReport.html', readReport = loadListReport)

#================[Saat user memberi rating]=================
@app.route('/sendRating', methods=['POST','GET'])
def sendRating():
    if request.method == 'POST':

        data = {
        'request_id'    : request.form['finishRat'],
        'rating'        : request.form['fRating'],
        'keterangan'    : request.form['inputKeterangan'] 
        }

        dataRating = json.dumps(data)

        requests.post('http://127.0.0.1:5001/finishRating/'+dataRating)

        print("=== [ sendRating ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("======================")

        return redirect(url_for('listFinished'))

#================[Menampilkan layar Request Laporan]=================
@app.route('/newRequest', methods = ['GET','POST'])
def newRequest():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        org     = requests.get('http://127.0.0.1:5001/namaOrganisasi')
        orgResp =json.dumps(org.json())
        loadOrg = json.loads(orgResp)

        cat     = requests.get('http://127.0.0.1:5001/namaDept')
        catResp = json.dumps(cat.json())
        loadCat = json.loads(catResp)

        PIC     = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPIC = json.loads(picResp)

        Pen     = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPen = json.loads(penResp)

        print("=== [ newRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("======================")

        return render_template('ms1requestLaporan.html', listOrg = loadOrg, 
                                listDept = loadCat, listPIC = loadPIC, listPen = loadPen)

#================[Mengirim data request ke MS1/addNewRequest]================= 
@app.route('/sendDataRequest', methods=['POST','GET'])
def sendDataRequest():
    PIC = requests.get('http://127.0.0.1:5001/namaPIC')
    picResp = json.dumps(PIC.json())
    loadPIC = json.loads(picResp)

    Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
    penResp = json.dumps(Pen.json())
    loadPen = json.loads(penResp)

    if request.method == 'POST':
        reqSch_hari         = ''
        reqSch_bulan        = ''
        reqSch_tanggal      = ''
        reqSch_reportPIC    = ''
        reqSch_penerima     = ''

        title           = request.form['inputTitle']
        purpose         = request.form['inputPurpose']
        description     = request.form['keteranganlaporan']
        Organization    = request.form['Organization']
        Department      = request.form['Department']
        Display         = request.form['inputDisplay']
        Period          = request.form['inputPeriode']
        deadline        = request.form['deadline']
        file            = request.files['inputFile']

        if title == '' or file =='':
            return redirect(url_for('newRequest'))
        else:
        
        
            getFileName = requests.get('http://127.0.0.1:5001/generateRequestId')
            fiName      = json.dumps(getFileName.json())
            resName     = json.loads(fiName)
            fileN       = [x['requestId'] for x in resName]
            fileName    = str(fileN).replace("['","").replace("']","")


            print(fileName)

            # fileName = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName+'.jpg'))
            
            
            
            
            if 'file' not in request.files:
                fileName = ''

            if file.filename == '':
                fileName = ''
            

            print('OKEEEEEEEEEEEEEEEEEEEEEEE')
            


            for checkHari in ['mon','tue','wed','thu','fri','sat','sun']:
                if request.form.get(checkHari) is not None:
                    if reqSch_hari == '':
                        reqSch_hari += request.form.get(checkHari)
                    else:
                        reqSch_hari +=  ", "+request.form.get(checkHari)
            print(reqSch_hari)

            for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                if request.form.get(checkBulan) is not None:
                    if reqSch_bulan == '':
                        reqSch_bulan += request.form.get(checkBulan)
                    else:
                        reqSch_bulan +=  ", "+request.form.get(checkBulan)
            print (reqSch_bulan) 

            for checkTgl in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31']:
                if request.form.get(checkTgl) is not None:
                    if reqSch_tanggal == '':
                        reqSch_tanggal += request.form.get(checkTgl)
                    else:
                        reqSch_tanggal +=  ", "+request.form.get(checkTgl)
            print (reqSch_tanggal)


            #Validasi radio button
            for checkRadio in ['rutin']:
                if request.form.get(checkRadio) == 'hb':
                    reqSch_tanggal = ''
                else:
                    reqSch_hari = ''


            
            ####
            for checkPIC in loadPIC:
                
                if request.form.get(checkPIC['Id']) is not None:
                    if reqSch_reportPIC == '':
                        reqSch_reportPIC += checkPIC['Email']
                    else:
                        reqSch_reportPIC += ", "+checkPIC['Email']
            print (reqSch_reportPIC)

            for checkPen in loadPen:
                
                if request.form.get(checkPen['Email']) is not None:
                    if reqSch_penerima == '':
                        reqSch_penerima += checkPen['Email']
                    else:
                        reqSch_penerima += ", "+checkPen['Email']
            print (reqSch_penerima)


            
            

            request_data = {
            'ProgId'            : None,
            'UserId'            : session['user_id'],
            'OrgId'             : Organization,
            'KtgriId'           : Department,
            'kodLap'            : None,
            'Judul'             : title,
            'Deskripsi'         : description,
            'Tujuan'            : purpose,
            'Tampilan'          : Display,
            'Periode'           : Period,
            'Deadline'          : deadline,
            'File'              : fileName,
            'PIC'               : None,
            'Hari'              : reqSch_hari,
            'Bulan'             : reqSch_bulan,
            'Tanggal'           : reqSch_tanggal,
            'schOrg'            : Organization,
            'schKtgri'          : Department,
            'schLastUpdate'     : None,
            'schPIC'            : reqSch_reportPIC,
            'schPenerima'       : reqSch_penerima
            }

            
            dataRequest = json.dumps(request_data)

            requests.post('http://127.0.0.1:5001/addNewRequest/'+dataRequest)

            print("=== [ sendDataRequest ] ===")
            print('ID   : ',session['user_id']),print('Name : ',session['username'])
            print('Time : ',datetime.datetime.now().strftime('%X'))
            print("===========================")

            return redirect(url_for('list'))

#==[Ketika user membatalkan request. Mengirim ReqID yang dicancel ke MS1/cancR]========
@app.route('/cancelRequest', methods=['POST','GET'])
def cancelRequest():

    if request.method == 'POST':

        rId  = request.form['btnCancel']

        data={
        'request_id' : rId
        }

        dataFix = json.dumps(data)


        requests.post('http://127.0.0.1:5001/cancR/'+dataFix)

        print("=== [ cancelRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=========================")

        return redirect(url_for('list'))

#================[Menampilkan kode laporan yang ingin di edit]=================
#================[Menampilkan form edit laporan]=================
@app.route('/editReport', methods=['POST','GET'])
def editReport():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        uId = session['user_id']
        listReportId    = requests.get('http://127.0.0.1:5001/getReportId')
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep     = json.loads(listReportIdResp)
        
        if request.method == 'POST':
            kode_laporan = request.form['kodeLaporan']

            sendKodeLaporan = requests.get(''.join(['http://127.0.0.1:5001/getCurrentDisplay/'+kode_laporan]))
            KodeLaporanResp = json.dumps(sendKodeLaporan.json())
            loadLap = json.loads(KodeLaporanResp)

            PIC     = requests.get('http://127.0.0.1:5001/namaPIC')
            picResp = json.dumps(PIC.json())
            loadPICe = json.loads(picResp)

            Pen     = requests.get('http://127.0.0.1:5001/namaPenerima')
            penResp = json.dumps(Pen.json())
            loadPene = json.loads(penResp)

            print("=== [ editReport ] ===")
            print('ID   : ',session['user_id']),print('Name : ',session['username'])
            print('Time : ',datetime.datetime.now().strftime('%X'))
            print("======================")

            return render_template("ms1Edit2.html", listcurrentdisplay = loadLap, 
                                    listPIC = loadPICe, listPen = loadPene, kode_laporan=kode_laporan)
        print("=== [ editReport ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("======================")

        return render_template('ms1Edit2.html', listKodeReport = loadListRep)

#===[Mengirim data edit laporan sebagai request baru ke MS1/editRequest]=================
@app.route('/sendEditRequest', methods = ['POST','GET'])
def sendEditRequest():
    if request.method == 'POST':
        PIC     = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPICe = json.loads(picResp)

        Pen     = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPene = json.loads(penResp)

        kode_laporan = request.form['labelKodLap']

        getJudulTujuan = requests.get('http://127.0.0.1:5001/getDataReport/'+kode_laporan)
        result          = json.dumps(getJudulTujuan.json())
        loadJudulTujuan = json.loads(result)

        for i in loadJudulTujuan:
            req_tujuan  = i['reportTujuan']
            req_judul   = i['reportJudul']
            org_id      = i['reportOrg']
            ktgri_id    = i['reportKtgri']




        reqSch_hari         = ''
        reqSch_bulan        = ''
        reqSch_tanggal      = ''
        reqSch_reportPIC    = ''
        reqSch_penerima     = ''
        

        

        newFilter   = request.form['inputFilterBaru']
        newDisplay  = request.form['inputNewDisplay']
        deadline    = request.form['deadline']
        Period      = request.form['inputPeriode']
        if 'inputFile' not in request.files:
            print('empty')
        file = request.files['inputFile'].read()

        


        for checkHari in ['mon','tue','wed','thu','fri','sat','sun']:
            if request.form.get(checkHari) is not None:
                if reqSch_hari == '':
                    reqSch_hari += request.form.get(checkHari)
                else:
                    reqSch_hari +=  ", "+request.form.get(checkHari)
        print(reqSch_hari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if request.form.get(checkBulan) is not None:
                if reqSch_bulan == '':
                    reqSch_bulan += request.form.get(checkBulan)
                else:
                    reqSch_bulan +=  ", "+request.form.get(checkBulan)
        print (reqSch_bulan) 

        for checkTgl in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31']:
            if request.form.get(checkTgl) is not None:
                if reqSch_tanggal == '':
                    reqSch_tanggal += request.form.get(checkTgl)
                else:
                    reqSch_tanggal +=  ", "+request.form.get(checkTgl)
        print (reqSch_tanggal)


        #Validasi radio button
        for checkRadio in ['rutin']:
            if request.form.get(checkRadio) == 'hb':
                reqSch_tanggal = ''
            else:
                reqSch_hari = ''
        
        ####
        for checkPIC in loadPICe:
            
            if request.form.get(checkPIC['Id']) is not None:
                if reqSch_reportPIC == '':
                    reqSch_reportPIC += checkPIC['Email']
                else:
                    reqSch_reportPIC += ", "+checkPIC['Email']
        print (reqSch_reportPIC)

        for checkPen in loadPene:
            
            if request.form.get(checkPen['Email']) is not None:
                if reqSch_penerima == '':
                    reqSch_penerima += checkPen['Email']
                else:
                    reqSch_penerima += ", "+checkPen['Email']
        print (reqSch_penerima)


        edit_data = {
        'ProgId'        : None,
        'UserId'        : session['user_id'],
        'OrgId'         : org_id,
        'KtgriId'       : ktgri_id,
        'kodLap'        : kode_laporan,
        'Judul'         : req_judul,
        'Deskripsi'     : newFilter,
        'Tujuan'        : req_tujuan,
        'Tampilan'      : newDisplay,
        'Periode'       : Period,
        'Deadline'      : deadline,
        'File'          : None,
        'PIC'           : None,
        'Hari'          : reqSch_hari,
        'Bulan'         : reqSch_bulan,
        'Tanggal'       : reqSch_tanggal,
        'schOrg'        : org_id,
        'schKtgri'      : ktgri_id,
        'schLastUpdate' : None,
        'schPIC'        : reqSch_reportPIC,
        'schPenerima'   : reqSch_penerima
        }

        dataEdit = json.dumps(edit_data)

        requests.post('http://127.0.0.1:5001/editRequest/'+dataEdit)

        print("=== [ sendEditRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("===========================")

        return redirect(url_for('list'))



#=========================================================================================
#=========================================================================================
#=========================[         SUPERVISOR             ]==============================
#=========================================================================================
#=========================================================================================


@app.route('/availableTaskSPV')
def listRequestSPV():
    # sessionId = session['user_id']

    listAvailableTask = requests.get('http://127.0.0.1:5001/availableTask')
    avTask          = json.dumps(listAvailableTask.json())
    loadAvailTask   = json.loads(avTask)

    # listTask = requests.get('http://127.0.0.1:5001/listTask/'+sessionId)
    # Task = json.dumps(listTask.json())
    # loadTask = json.loads(Task)
    print("=== [ availableTaskSPV ] ===")
    print('ID   : ',session['user_id']),print('Name : ',session['username'])
    print('Time : ',datetime.datetime.now().strftime('%X'))
    print("============================")

    return render_template('ms1availableTaskSPV.html', listAvailTaskSPV = loadAvailTask)
                            # listTask = loadTask)



@app.route('/onProgressTask')
def onProgressTask():

    onProgTask = requests.get('http://127.0.0.1:5001/onProgressTask')
    onTask  = json.dumps(onProgTask.json())
    loadOnProgTask = json.loads(onTask)

    print("=== [ onProgressTask ] ===")
    print('ID   : ',session['user_id']),print('Name : ',session['username'])
    print('Time : ',datetime.datetime.now().strftime('%X'))
    print("==========================")
    return render_template('ms1onProgressTaskSPV.html', onProgTask = loadOnProgTask)

@app.route('/spv')
def spv():
    print("=== [ homeSPV ] ===")
    print('ID   : ',session['user_id']),print('Name : ',session['username'])
    print('Time : ',datetime.datetime.now().strftime('%X'))
    print("==========================")
    return render_template('ms2homeSPV.html')

@app.route('/rejectRequest', methods=['POST','GET'])
def rejectRequest():
    if request.method == 'POST':

        data = {
        'request_id'    : request.form['btnYes'],
        'userName'      : session['username']
        }

        dataReject = json.dumps(data)

        requests.post('http://127.0.0.1:5001/reject/'+dataReject)

        print("=== [ rejectRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=========================")

        return redirect(url_for('listRequestSPV'))

@app.route('/prioritasRequest', methods = ['POST', 'GET'])
def prioritasReq():
    if request.method == 'POST':

        data = {
        'request_id' : request.form['btnYesP'],
        }

        dataPrioritas = json.dumps(data)

        requests.post('http://127.0.0.1:5001/prioritas/'+dataPrioritas)

        print("=== [ prioritasRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("============================")

        return redirect(url_for('listRequestSPV'))

@app.route('/undoPrioritasRequest', methods = ['POST', 'GET'])
def undoPrioritasRequest():
    if request.method == 'POST':

        data = {
        'request_id' : request.form['btnUndo'],
        }

        dataUndoPrioritas = json.dumps(data)

        requests.post('http://127.0.0.1:5001/undoPrioritas/'+dataUndoPrioritas)

        print("=== [ undoPrioritasRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("================================")

        return redirect(url_for('listRequestSPV'))

#=========================================================================================
#=========================================================================================
#=========================[         PROGRAMMER             ]==============================
#=========================================================================================
#=========================================================================================

#============[Menampilkan homepage programmer]============
@app.route('/admin')
def admin():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        now = datetime.datetime.now()

        day = now.strftime("%A")
        clock = now.strftime("%H:%M:%S")

        print("=== [ homeAdmin ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=====================")
        return render_template('ms2home.html', day=day, clock=clock)

#============[Menampilkan list task yang bisa dikerjakan]============
@app.route('/availableTask')
def availableTask():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        sessionName = session['username']
        sessionId   = session['user_id']

        listAvailableTask = requests.get('http://127.0.0.1:5001/availableTask')
        avTask          = json.dumps(listAvailableTask.json())
        loadAvailTask   = json.loads(avTask)


        listReportId    = requests.get('http://127.0.0.1:5001/getReportId')
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep     = json.loads(listReportIdResp)

        detailNormal = requests.get('http://127.0.0.1:5001/taskProgrammer/'+sessionId)
        detNormal       = json.dumps(detailNormal.json())
        loadTaskProg = json.loads(detNormal)


        print("=== [ availableTask ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=========================")

        return render_template('ms1availableTask.html', listAvailTask = loadAvailTask,
                                listKodeLap = loadListRep, taskProg = loadTaskProg)

#============[Menampilkan list task yang harus dikerjakan]============
@app.route('/listTask')
def listTask():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        sessionName = session['username']
        sessionId = session['user_id']

        listReportId    = requests.get('http://127.0.0.1:5001/getReportId')
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep     = json.loads(listReportIdResp)

        listTask = requests.get('http://127.0.0.1:5001/listTask/'+sessionId)
        Task    = json.dumps(listTask.json())
        loadTask = json.loads(Task)

        print("=== [ listTask ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("====================")

        return render_template('ms1listTask.html', listTask = loadTask, 
                                listKodeLap = loadListRep)

#============[Menampilkan list task yang sudah selesai dikerjakan]============
@app.route('/historyTask')
def historyTask():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        sessionName = session['username']
        sessionId   = session['user_id']

        listReportId    = requests.get('http://127.0.0.1:5001/getReportId')
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep     = json.loads(listReportIdResp)

        histTask = requests.get('http://127.0.0.1:5001/historyTask/'+sessionName)
        hist    = json.dumps(histTask.json())
        loadHist = json.loads(hist)

        print("=== [ historyTask ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=======================")
        return render_template('ms1historyTask.html', historyTask = loadHist, 
                                listKodeLap = loadListRep)

#=====[Saat programmer mengklik request yang ada]===========
@app.route('/detailRequest', methods=['POST','GET'])
def detailRequest():
    if request.method=='POST':
        request_id = request.form['buttonDetail']
        # sessionName = session['username']

        detailTask      = requests.get('http://127.0.0.1:5001/getDetailTask/'+request_id)
        detTask         = json.dumps(detailTask.json())
        loadDetailTask = json.loads(detTask)

        #CEK REQUEST TSB ADA IMAGE/TIDAK
        try:
            checkImage= open(os.path.join(app.config['UPLOAD_FOLDER'], request_id+'.jpg'))
        except Exception as e:
                    checkImage = 'NOIMAGE'

        namaImage = request_id+'.jpg'

        # UNTUK MENGAMBIL VALUE DALAM JSON
        for x in loadDetailTask:
            aaa = x['requestId']
            bbb = x['requestTujuan']

        print("=== [ detailRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=========================")

        return render_template('ms1detailTask.html', detail_task = loadDetailTask, imageR=namaImage, checkImage=checkImage)



#============[Mengirim data accept request ke MS1/accRequest]============
@app.route('/acceptRequest', methods=['POST','GET'])
def acceptRequest():
    if request.method == 'POST':
        request_id  = request.form['btnConfirmReq']
        uId         = session['user_id']
        uName       = session['username']


        detailAccept = {
        'request_id': request_id,
        'uId'       : uId,
        'uName'     : uName
        }

        detAcc = json.dumps(detailAccept)

        requests.post('http://127.0.0.1:5001/accRequest/'+detAcc)

        print("=== [ acceptRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=========================")
        # return redirect(url_for("task"))
        if session['position'] == 'Admin':
            return redirect(url_for("listTask"))
        else:
            return redirect(url_for("listRequestSPV"))


#============[Mengirim data finish request ke MS1/finReq]============
@app.route('/finishRequest', methods=['POST','GET'])
def finishRequest():
    if request.method == 'POST':
        request_id = request.form['finishReq']
        kodeL       = request.form['kodLap']
        file        = request.files['inputFile']


        fileName = request_id
        file.save(os.path.join(app.config['UPLOAD_FINISHED_REQUEST'], fileName+'.xls'))
        
        if 'file' not in request.files:
            fileName = ''

        if file.filename == '':
            fileName = ''


        a = {
        'request_id'    : request_id,
        'kode_laporan'  : kodeL
        }

        b = json.dumps(a)

        requests.post('http://127.0.0.1:5001/finReq/'+b)


        print("=== [ finishRequest ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=========================")

        # return redirect(url_for('task'))
        if session['position'] == 'Admin':

            return redirect(url_for("listTask"))
        else:
            return redirect(url_for("listRequestSPV"))


#=========================================================================================
#=========================================================================================
#=========================[    PROGRAMMER MICROSERVICE2     ]=============================
#=========================================================================================
#=========================================================================================


#=========================================================================================
#=========================================================================================
#=================================[    SCHEDULE     ]=====================================
#=========================================================================================
#=========================================================================================

#============[Menampilkan menu add new Schedule]============
@app.route('/addNewSchedule', methods = ['POST','GET'])
def addNewSchedule():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        getKodeS = requests.get('http://127.0.0.1:5002/listKodeReportAddNewSchedule')
        kodeNewS = json.dumps(getKodeS.json())
        loadKodeNewSchedule = json.loads(kodeNewS)

        PIC = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPIC = json.loads(picResp)

        Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPen = json.loads(penResp)

        print("=== [ addNewSchedule ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("==========================")
        
        return render_template('ms2addNewSchedule.html', listKodeReportS = loadKodeNewSchedule,
                                listPIC = loadPIC,listPen = loadPen)

#============[Mengirim data add new schedule ke MS2/addSchedule]============
@app.route('/sendAddNewSchedule', methods=['POST','GET'])
def sendAddNewSchedule():
    if request.method == 'POST':
        PIC = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPICs = json.loads(picResp)

        Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPens = json.loads(penResp)

        kode_laporan = request.form['valKode']

        #Untuk mendapatkan ID Organisasi & Kategori untuk didapatkan namanya.
        detailLap = requests.get('http://127.0.0.1:5002/getIdOrgKat/'+kode_laporan)
        orgKat = json.dumps(detailLap.json())
        loadOrgKat = json.loads(orgKat)
        for i in loadOrgKat:
            idOrg = i['report_org']
            idKat = i['report_kat']

        #Mendapatkan nama Organisasi
        gOrg = requests.get('http://127.0.0.1:5001/getNamaOrg/'+idOrg)
        org2 = json.dumps(gOrg.json())
        namaOrg = json.loads(org2)
        for x in namaOrg:
            nmOrg = x['org_name']

        #Mendapatkan nama Kategori
        gKat = requests.get('http://127.0.0.1:5001/getNamaKat/'+idKat)
        kat2 = json.dumps(gKat.json())
        namaKat = json.loads(kat2)
        for y in namaKat:
            nmKat = y['kat_name']



        header      = request.form['header']
        keterangan  = request.form['keterangan']
        note        = request.form['note']
        grouping    = request.form['grouping']
        org         = nmOrg
        kategori    = nmKat
        
        reportPIC       = ''
        reportPenerima  = ''
        
        jadwalBln   = ''
        jadwalHari  = ''
        jadwalTgl   = ''
        
        


        for checkHari in ['mon','tue','wed','thu','fri','sat','sun']:
            if request.form.get(checkHari) is not None:
                if jadwalHari == '':
                    jadwalHari += request.form.get(checkHari)
                else:
                    jadwalHari +=  ", "+request.form.get(checkHari)
        print("Hari ",jadwalHari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if request.form.get(checkBulan) is not None:
                if jadwalBln == '':
                    jadwalBln += request.form.get(checkBulan)
                else:
                    jadwalBln +=  ", "+request.form.get(checkBulan)
        print ("Bulan ",jadwalBln) 

        for checkTgl in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31']:
            if request.form.get(checkTgl) is not None:
                if jadwalTgl == '':
                    jadwalTgl += request.form.get(checkTgl)
                else:
                    jadwalTgl +=  ", "+request.form.get(checkTgl)
        print ("Tanggal ",jadwalTgl)


        #Validasi radio button
        for checkRadio in ['rutin']:
            if request.form.get(checkRadio) == 'hb':
                reqSch_tanggal = ''
            else:
                reqSch_hari = ''

        for checkPIC in loadPICs:
            #print(checkPIC[0])
            if request.form.get(checkPIC['Id']) is not None:
                if reportPIC == '':
                    reportPIC += checkPIC['Email']
                else:
                    reportPIC += ", "+checkPIC['Email']
        print ("PIC ",reportPIC)

        for checkPen in loadPens:
            #print(checkPen[2])
            if request.form.get(checkPen['Email']) is not None:
                if reportPenerima == '':
                    reportPenerima += checkPen['Email']
                else:
                    reportPenerima += ", "+checkPen['Email']
        print ("Penerima ", reportPenerima)  

       

        addS_data = {
        'report_id'         : kode_laporan,
        'sch_header'        : header,
        'sch_keterangan'    : keterangan,
        'sch_note'          : note,
        'sch_reportPIC'     : reportPIC,
        'sch_reportPen'     : reportPenerima,
        'sch_grouping'      : grouping,
        'sch_bulan'         : jadwalBln,
        'sch_hari'          : jadwalHari,
        'sch_tanggal'       : jadwalTgl,
        'sch_org'           : org,
        'sch_kategori'      : kategori
        }


        data_schedule = json.dumps(addS_data)

        requests.post('http://127.0.0.1:5002/addSchedule/'+data_schedule)

        print("=== [ sendAddNewSchedule ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("==============================")

        return redirect(url_for('admin'))

#============[Memilih kode laporan yang akan diubah schedulenya]============
#============[Menampilkan form edit schedule]============
@app.route('/editSchedule', methods=['POST','GET'])
def editSchedule():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        kodeReport = requests.get('http://127.0.0.1:5002/listKodeReportEditSchedule')
        kodeAll = json.dumps(kodeReport.json())
        loadKodeAll = json.loads(kodeAll)

        if request.method == 'POST':
            kode_laporan = request.form['valKode']

            PIC = requests.get('http://127.0.0.1:5001/namaPIC')
            picResp = json.dumps(PIC.json())
            loadPICs = json.loads(picResp)

            Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
            penResp = json.dumps(Pen.json())
            loadPens = json.loads(penResp)

            detSch = requests.get('http://127.0.0.1:5002/showDetailSchedule/'+kode_laporan)
            detDumps = json.dumps(detSch.json())
            loadDetSch = json.loads(detDumps)

            print("=== [ editSchedule ] ===")
            print('ID   : ',session['user_id']),print('Name : ',session['username'])
            print('Time : ',datetime.datetime.now().strftime('%X'))
            print("========================")

            return render_template('ms2editSchedule2.html', detailSchedule = loadDetSch,
                kode_laporan=kode_laporan, listPIC = loadPICs, listPen = loadPens)

        return render_template('ms2editSchedule.html', listKodeLap = loadKodeAll)

#============[Mengirim data edit schedule ke MS2/editSched]============
@app.route('/sendEditSchedule', methods=['POST','GET'])
def sendEditSchedule():
    PIC = requests.get('http://127.0.0.1:5001/namaPIC')
    picResp = json.dumps(PIC.json())
    loadPICs = json.loads(picResp)

    Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
    penResp = json.dumps(Pen.json())
    loadPens = json.loads(penResp)



    if request.method == 'POST':
        kode_laporan    = request.form['kodLap2']
        header          = request.form['header']
        keterangan      = request.form['keterangan']
        note            = request.form['note']
        grouping        = request.form['grouping']
        reportPIC       = ''
        reportPenerima  = ''
        jadwalBln       = ''
        jadwalHari      = ''
        jadwalTgl       = ''


        aktifYN = request.form['aktifYND']
        lastUpdate = datetime.datetime.now()

        for checkHari in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
            if request.form.get(checkHari) is not None:
                if jadwalHari == '':
                    jadwalHari += request.form.get(checkHari)
                else:
                    jadwalHari +=  ", "+request.form.get(checkHari)
        print("Hari ",jadwalHari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if request.form.get(checkBulan) is not None:
                if jadwalBln == '':
                    jadwalBln += request.form.get(checkBulan)
                else:
                    jadwalBln +=  ", "+request.form.get(checkBulan)
        print ("Bulan ",jadwalBln) 

        for checkTgl in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']:
            if request.form.get(checkTgl) is not None:
                if jadwalTgl == '':
                    jadwalTgl += request.form.get(checkTgl)
                else:
                    jadwalTgl +=  ", "+request.form.get(checkTgl)
        print ("Tanggal ",jadwalTgl)

        #Validasi radio button
        for checkRadio in ['rutin']:
            if request.form.get(checkRadio) == 'hb':
                jadwalTgl = ''
            else:
                jadwalHari = ''

        for checkPIC in loadPICs:
            #print(checkPIC[0])
            if request.form.get(checkPIC['Id']) is not None:
                if reportPIC == '':
                    reportPIC += checkPIC['Email']
                else:
                    reportPIC += ", "+checkPIC['Email']
        print ("PIC ",reportPIC)

        for checkPen in loadPens:
            #print(checkPen[2])
            if request.form.get(checkPen['Email']) is not None:
                if reportPenerima == '':
                    reportPenerima += checkPen['Email']
                else:
                    reportPenerima += ", "+checkPen['Email']
        print ("Penerima ", reportPenerima)

        
        

        dataEdit = {
        'reportId'      : kode_laporan,
        'header'        : header,
        'keterangan'    : keterangan,
        'note'          : note,
        'grouping'      : grouping,
        'PIC'           : reportPIC,
        'Penerima'      : reportPenerima,
        'jadwalBln'     : jadwalBln,
        'jadwalHari'    : jadwalHari,
        'jadwalTgl'     : jadwalTgl,
        'aktifYN'       : aktifYN,
        'lastUpdate'    : str(lastUpdate)
        }

        editData = json.dumps(dataEdit)

        requests.post('http://127.0.0.1:5002/editSched/'+editData)

        print("=== [ sendEditSchedule ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("============================")

        return redirect(url_for('admin'))



#=========================================================================================
#=========================================================================================
#=================================[    QUERY     ]========================================
#=========================================================================================
#=========================================================================================

#============[Menampilkan layar insert query]============
@app.route('/insertQuery', methods=['POST','GET'])
def addQuery():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        kQuery = requests.get('http://127.0.0.1:5002/getKodeNewQuery')
        kDump = json.dumps(kQuery.json())
        kLoad = json.loads(kDump)

        print("=== [ insertQuery ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=======================")

        return render_template('ms2insertQuery.html', kodeNewQuery = kLoad)

#============[Mengirim data query ke MS2/addQuery]============
@app.route('/sendNewQuery', methods=['POST','GET'])
def sendNewQuery():
    quer = []
    kode_laporan = request.form['kodLap']
    kode_laporan.upper()

    if request.method == 'POST':
        for query in ['query1', 'query2', 'query3', 'query4', 'query5', 'query6', 'query7', 'query8', 'query9', 'query10', 'query11', 'query12', 'query13', 'query14']:
            
            if (request.form[query] is not  None) and (request.form[query] is not ''):
                quer.append(request.form[query])
                queryDump = json.dumps(quer)



        requests.post('http://127.0.0.1:5002/addQuery/'+kode_laporan+'/'+queryDump)

        print("=== [ sendNewQuery ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("========================")

        return redirect(url_for('admin'))

#============[Memilih kode laporan yang akan diubah querynya]============
#============[Menampilkan menu insert Query]============
@app.route('/editQuery', methods=['POST','GET'])
def editQuery():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        kEQuery = requests.get('http://127.0.0.1:5002/getKodeEditQuery')
        kEDump = json.dumps(kEQuery.json())
        kELoad = json.loads(kEDump)

        if request.method == 'POST':
            kode_laporan = request.form['kodLap']

            Query = requests.get('http://127.0.0.1:5002/viewEditQuery/'+kode_laporan)
            QDump = json.dumps(Query.json())
            QLoad = json.loads(QDump)

            print("=== [ editQuery ] ===")
            print('ID   : ',session['user_id']),print('Name : ',session['username'])
            print('Time : ',datetime.datetime.now().strftime('%X'))
            print("=====================")

            return render_template('ms2insertEditQuery.html', editQ = QLoad, kode_laporan=kode_laporan)

        return render_template('ms2editQuery.html', listKodeReportQuery = kELoad)



#=========================================================================================
#=========================================================================================
#==================================[    TEMPLATE     ]====================================
#=========================================================================================
#=========================================================================================

#============[Menampilkan menu untuk membuat template baru]============
@app.route('/addTemplate', methods=['POST','GET'])
def addTemplate():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        org = requests.get('http://127.0.0.1:5001/namaOrganisasi')
        orgResp=json.dumps(org.json())
        loadOrg = json.loads(orgResp)

        cat = requests.get('http://127.0.0.1:5001/namaDept')
        catResp = json.dumps(cat.json())
        loadCat = json.loads(catResp)

        ser = requests.get('http://127.0.0.1:5002/getServer')
        serResp = json.dumps(ser.json())
        loadSer = json.loads(serResp)

        print("=== [ addTemplate ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=======================")

        return render_template('ms2addNewTemplate.html', listKategori = loadCat, listOrg = loadOrg,
                                listServer = loadSer)

#============[Mengirim data template baru ke MS2/addNewTemplate]============
@app.route('/sendNewTemplate', methods=['POST','GET'])
def sendNewTemplate():

    if request.method == 'POST':

        userName = session['username']

        kode_laporan        = request.form['kodeLaporan2']+'-'+request.form['kategori']+request.form['noLap']
        server_id           = request.form['server']
        report_judul        = request.form['namaLaporan']
        report_deskripsi    = request.form['filter']
        report_header       = request.form['jmlHeader']
        report_footer       = request.form['jmlFooter']
        report_jmlTampilan  = request.form['jmlTampilan']
        report_periode      = request.form['periode']
        #report_createDate   = datetime.datetime.now(),
        report_userUpdate   = userName
        #report_lastUpdate   = datetime.datetime.now(),
        report_aktifYN      = 'Y'
        org_id              = request.form['organisasi']
        ktgri_id            = request.form['kategori']
        report_printAllYN   = request.form['printAll']
        report_createdUser  = userName
        report_scheduleYN   = 'N'
        report_tujuan       = request.form['tujuan']

        
        data= {
        'kode_laporan'        : str(kode_laporan),
        'server_id'           : str(server_id),
        'report_judul'        : str(report_judul),
        'report_deskripsi'    : str(report_deskripsi),
        'report_header'       : str(report_header),
        'report_footer'       : str(report_footer),
        'report_jmlTampilan'  : str(report_jmlTampilan),
        'report_periode'      : str(report_periode),
        #'report_createDate'   : report_createDate,
        'report_userUpdate'   : str(report_userUpdate),
        #'report_lastUpdate'   : report_lastUpdate,
        'report_aktifYN'      : str(report_aktifYN),
        'org_id'              : str(org_id),
        'ktgri_id'            : str(ktgri_id),
        'report_printAllYN'   : str(report_printAllYN),
        'report_createdUser'  : str(report_createdUser),
        'report_scheduleYN'   : str(report_scheduleYN),
        'report_tujuan'       : str(report_tujuan)
        }
        
        dataTemplate = json.dumps(data)

        requests.post('http://127.0.0.1:5002/addNewTemplate/'+dataTemplate)

        detTem = requests.get('http://127.0.0.1:5002/formatTemplate/'+kode_laporan)
        detDump = json.dumps(detTem.json())
        loadDetail = json.loads(detDump)
        
        jumKol = loadDetail[0]['reportJmlTampilan']

        print("=== [ sendNewTemplate ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("===========================")

        return render_template('addTemplate.html', detailFormatTemplate = loadDetail,
            jumKol=jumKol)

# [Save detail kolom ke detailh dan detailf]
@app.route('/sendFormatTemplate',  methods =  ['POST', 'GET'])
def sendFormatTemplate():
    
    kode_laporan = request.form['kodLap']
    jmlTamp      = request.form['jmlKolom']
    kolom_merge = request.form['kolomMerge']
    kolom_kanan = request.form['rataKanan']
    kolom_tengah = request.form['rataTengah']

    kolom_footer1 = request.form['kolomFooter1']
    kolom_footer2 = request.form['kolomFooter2']
    posisi_footer1 = ''
    posisi_footer2 = ''

    kolomTemp = []
    posisiTemp = []
    tipeTemp = []
    lebarTemp = []

    kolomFTemp = []
    posisiFTemp = []

    if request.method == 'POST':

        for isiKolom in ['kolom1', 'kolom2', 'kolom3', 'kolom4', 'kolom5', 'kolom6', 'kolom7',
        'kolom8', 'kolom9', 'kolom10', 'kolom11', 'kolom12', 'kolom13', 'kolom14']:
            if(request.form[isiKolom] is not None) and (request.form[isiKolom] is not ''):
                kolomTemp.append(request.form[isiKolom])
                kolomTemp1 = json.dumps(kolomTemp)
        print(kolomTemp1)

        for isiPosisi in ['posisi1', 'posisi2', 'posisi3', 'posisi4', 'posisi5', 'posisi6', 'posisi7',
        'posisi8', 'posisi9', 'posisi10', 'posisi11', 'posisi12', 'posisi13', 'posisi14']:
            if(request.form[isiPosisi] is not None) and (request.form[isiPosisi] is not ''):
                posisiTemp.append(request.form[isiPosisi])
                posisiTemp1 = json.dumps(posisiTemp)
        print(posisiTemp1)
        
        for isiTipe in ['tipe1', 'tipe2', 'tipe3', 'tipe4', 'tipe5', 'tipe6', 'tipe7',
        'tipe8', 'tipe9', 'tipe10', 'tipe11', 'tipe12', 'tipe13', 'tipe14']:
            if (request.form[isiTipe] is not None) and (request.form[isiTipe] is not ''):
                tipeTemp.append(request.form[isiTipe])
                tipeTemp1 = json.dumps(tipeTemp)
        print(tipeTemp1)

        for isiLebar in ['lebar1', 'lebar2', 'lebar3', 'lebar4', 'lebar5', 'lebar6', 'lebar7',
        'lebar8', 'lebar9', 'lebar10', 'lebar11', 'lebar12', 'lebar13', 'lebar14']:
            if (request.form[isiLebar] is not None) and (request.form[isiLebar] is not ''):
                lebarTemp.append(request.form[isiLebar])
                lebarTemp1 = json.dumps(lebarTemp)
        print(lebarTemp1)

        for posisiFooter in ['B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1', 'K1', 'L1', 'M1', 'N1']:
            if request.form.get(posisiFooter) is not None:
                if posisi_footer1 == '':
                    posisi_footer1 += request.form.get(posisiFooter)
                else:
                    posisi_footer1 += ", "+request.form.get(posisiFooter)
        print(posisi_footer1)

        for posisiFooter2 in ['B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'J2', 'K2', 'L2', 'M2', 'N2']:
            if request.form.get(posisiFooter2) is not None:
                if posisi_footer2 == '':
                    posisi_footer2 += request.form.get(posisiFooter2)
                else:
                    posisi_footer2 += ", "+request.form.get(posisiFooter2)
        print(posisi_footer2)

        detailKolom = {
            'reportId'      : kode_laporan,
            'mergeKolom'    : kolom_merge,
            'rataKanan'     : kolom_kanan,
            'rataTengah'    : kolom_tengah,
            'jmlTampilan'   : jmlTamp,
            'namaFooter1'   : kolom_footer1,
            'namaFooter2'   : kolom_footer2,
            'posisiFooter1' : posisi_footer1,
            'posisiFooter2' : posisi_footer2
        }

        detailKolom1 = json.dumps(detailKolom)

        requests.post('http://127.0.0.1:5002/saveFormatTemplate/'+detailKolom1+'/'+kolomTemp1+
            '/'+posisiTemp1+'/'+tipeTemp1+'/'+lebarTemp1)
        requests.post('http://127.0.0.1:5002/saveFooterTemplate/'+detailKolom1)

        return redirect (url_for('admin'))
    return redirect (url_for('admin'))

#============[Memilih kode laporan]============
#============[Menampilkan form format template]============
@app.route('/formatTemplate', methods=['POST','GET'])
def formatTemplate():
    kodeReport = requests.get('http://127.0.0.1:5002/getKodeReportAll')
    kodeAll = json.dumps(kodeReport.json())
    loadKodeAll = json.loads(kodeAll)

    if request.method == 'POST':
        kode_laporan = request.form['kodLap']

        detTem = requests.get('http://127.0.0.1:5002/detailFormatTemplate/'+kode_laporan)
        detDump = json.dumps(detTem.json())
        loadDetail = json.loads(detDump)

        # try:
        jumKol          = loadDetail[0]['reportJmlTampilan']
        formatMerge     = loadDetail[0]['formatMerge']
        formatTengah    = loadDetail[0]['formatTengah']
        formatKanan    = loadDetail[0]['formatKanan']
        # namaKolomF = loadDetail[0]['namaKolomF']
        # urutanFooter = loadDetail[0]['urutanFooter']

        namaKolom   = []
        lokasiKolom = []
        tipeData    = []
        lebarKolom  = []

        x=0
        for i in loadDetail:
            naKol   = loadDetail[x]['namaKolomH']
            lok     = loadDetail[x]['lokasiH']
            tipeD   = loadDetail[x]['formatKolomH']
            leb     = loadDetail[x]['lebarKolomH']
            namaKolom.append(naKol)
            lokasiKolom.append(lok)
            tipeData.append(tipeD)
            lebarKolom.append(leb)
            x=x+1
        
        detFoot = requests.get('http://127.0.0.1:5002/detailFooter/'+kode_laporan)
        detFootDump = json.dumps(detFoot.json())
        loadDetailFooter = json.loads(detFootDump)
                
        namaKolomFooter = []
        lokasiFooter = []

        x=0
        for a in loadDetailFooter:
            naKolF = loadDetailFooter[x]['namaKolomF']
            lokF = loadDetailFooter[x]['lokasiF']
            namaKolomFooter.append(naKolF)
            lokasiFooter.append(lokF)
            x=x+1

        print("=== [ formatTemplate ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("==========================")
        # except Exception as e:
            
        #     err = 'Template "'+kode_laporan+'" not found'
            

        #     return  render_template('404notFound.html', error=err)

        return render_template('ms2formatTemplate2.html', kode_laporan=kode_laporan
            ,detailTemplate=loadDetail,
            jumKol=jumKol, namKol=namaKolom, lokasiKolom=lokasiKolom, tipeData=tipeData,
            lebarKolom=lebarKolom, formatMerge=formatMerge, formatTengah=formatTengah,
            formatKanan=formatKanan, namaKolomFooter=namaKolomFooter, lokasiFooter=lokasiFooter)


    return render_template('ms2formatTemplate1.html', listKodeReport = loadKodeAll)
        

#=========================================================================================
#=========================================================================================
#==================================[    PREVIEW      ]====================================
#=========================================================================================
#=========================================================================================

@app.route('/runSchedule', methods=['POST','GET'])
def runSchedule():
    getKodeToday = requests.get('http://127.0.0.1:5002/getKodeReportRunToday')
    kodeTodayResp = json.dumps(getKodeToday.json())
    loadKodeToday = json.loads(kodeTodayResp)

    getStatus = requests.get('http://127.0.0.1:5003/getStatusRunSchedule')
    statusResp = json.dumps(getStatus.json())
    loadStatus = json.loads(statusResp)

    print("=== [ runSchedule ] ===")
    print('ID   : ',session['user_id']),print('Name : ',session['username'])
    print('Time : ',datetime.datetime.now().strftime('%X'))
    print("=======================")

    return render_template('ms3runSchedule.html', kodeToday = loadKodeToday,
        statusSchedule = loadStatus)

@app.route('/reRun', methods=['POST'])
def reRun():
    if request.method == 'POST':
        kode_laporan = request.form['kodLap']

        requests.get('http://127.0.0.1:5003/runSchedule/'+kode_laporan)

        print("=== [ reRun ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=================")

        return redirect(url_for('runSchedule'))


#============[Menampilkan seluruh list report yang ada]============
@app.route('/listReport', methods=['POST','GET'])
def listReport():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        detR = requests.get('http://127.0.0.1:5002/getListReport')
        detResp = json.dumps(detR.json())
        loadListReport = json.loads(detResp)

        print("=== [ listReport ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("======================")
        return render_template('ms2listReport.html', listReport = loadListReport)

#============[Menampilkan seluruh list report yang ada berdasarkan schedule]============
@app.route('/listReportSchedule', methods=['POST','GET'])
def listReportSchedule():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        detR = requests.get('http://127.0.0.1:5002/getListReportSchedule')
        detResp = json.dumps(detR.json())
        loadListReport = json.loads(detResp)

        print("=== [ listReport ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("======================")
        return render_template('ms2listReportSch.html', listReport = loadListReport)

#============[Memilih kode laporan yang akan dipreview]============
#============[Mengirim kode laporan ke MS3/previewLaporan]============


@app.route('/preview', methods=['POST','GET'])
def preview():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        kEQuery = requests.get('http://127.0.0.1:5002/getKodeEditQuery')
        kEDump = json.dumps(kEQuery.json())
        kELoad = json.loads(kEDump)


        if request.method == 'POST':
            
            kode_laporan = request.form['kodLap']
            
            # VALIDASI ERROR / TIDAK
            a = requests.get('http://127.0.0.1:5003/testPreviewLaporan/'+kode_laporan)
            
            if a.status_code != 200:
                b = json.dumps(a.json())
                c = json.loads(b)
                
                return str(c)
            else:
                b=json.loads(a.json())

                namaFileExcel =  kode_laporan+'_'+str(b)+datetime.datetime.now().strftime('%d%m%Y')

                # tgl = datetime.datetime.now().strftime('%d')
                # bln = datetime.datetime.now().strftime('%B')
                # directory = 'C:/Report/'+bln+'/'+tgl

                # if not os.path.exists(directory):
                #     os.makedirs(directory)

                # output = open(directory+'/'+kode_laporan+'.xls','wb')
                # output.write(a.content)
                # output.close()
                print("=== [ preview ] ===")
                print('ID   : ',session['user_id']),print('Name : ',session['username'])
                print('Time : ',datetime.datetime.now().strftime('%X'))
                print("===================")

                return send_from_directory(app.config['FOLDER_PREVIEW'],namaFileExcel+'.xls',attachment_filename=namaFileExcel+'.xls', as_attachment=True)
                # return redirect(url_for('admin'))

            
        
        return render_template('ms3preview.html', kodeReportAdaQuery = kELoad)

@app.route('/downloadReport', methods=['POST','GET'])
def downloadReport():
    if request.method == 'POST':
        kode_laporan = request.form['kodLap']
        print(kode_laporan)

        tgl = datetime.datetime.now().strftime('%d')
        bln = datetime.datetime.now().strftime('%B')

        # resp = requests.get('http://127.0.0.1:5004/downloadReport/'+kode_laporan)

        namaF = requests.get('http://127.0.0.1:5004/getNamaFile/'+kode_laporan)
        namaResp = json.dumps(namaF.json())
        namaFi = json.loads(namaResp)
        namaFile = str(namaFi).replace("['","").replace("']","")
        
        # directory = 'C:/Report/'+bln+'/'+tgl

        # if not os.path.exists(directory):
        #     os.makedirs(directory)

        # output = open(directory+'/'+namaFile+'.xls', 'wb')
        # output.write(resp.content)
        # output.close()
        print("=== [ downloadReport ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("==========================")

        return send_from_directory(app.config['FOLDER_SCHEDULE'],namaFile+'.xls',attachment_filename=namaFile+'.xls', as_attachment=True)
        # return 'Downloaded'

@app.route('/readNow', methods=['POST','GET'])
def readNow():
    if request.method == 'POST':
        kode_laporan = request.form['kodRead']
        namaF       = requests.get('http://127.0.0.1:5004/getNamaFile/'+kode_laporan)
        namaResp    = json.dumps(namaF.json())
        namaFi      = json.loads(namaResp)
        namaFile    = str(namaFi).replace("['","").replace("']","")
        
        df = pd.read_excel(app.config['FOLDER_SCHEDULE']+'/'+namaFile+'.xls')
        # read = pickle.loads(base64.b64decode(excel.encode()))
        print("=== [ readNow ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("===================")
        
        return df.to_html()


@app.route('/testJSON', methods=['POST','GET'])
def testJSON():
    if request.method == 'POST':
        data = request.get_json()
        uName = data['data']['user']
        pwd = data['data']['pass']
        
        print('Data JSON: ',data)
        print('=====[ POST  ]======')
        print('ID   : ',uName)
        print('Pass : ',pwd)
        

    elif request.method == 'GET':
        print('=====[ GET  ]======')
        print('Hello, ini GET')

    return  'OK'


if __name__ == "__main__":
    # website_url = 'reportingsystem.pharos:5000'
    # app.config['SERVER_NAME'] = website_url
    app.run(host='0.0.0.0',debug=True)