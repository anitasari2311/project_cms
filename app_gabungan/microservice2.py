from flask import Flask, render_template, redirect, url_for, request, json, session
import pymysql
from auth import auth_login
import mysql.connector
from mysql.connector import Error

class ms2:
    def __init__(self):
        self.req_id = ''
        self.org_id = ''
        self.ktgri_id = ''
        self.req_kodeLaporan = ''
        self.req_judul = ''
        self.req_deskripsi = ''
        self.req_tujuan = ''
        self.req_tampilan = ''
        self.req_periode = ''
        self.req_deadline = ''
        self.req_file = ''
        self.req_PIC = ''
        self.req_penerima = ''
        self.sch_id = ''
        self.report_id = ''
        self.query_id = ''
        self.reqSch_hari = ''
        self.reqSch_bulan = ''
        self.reqSch_tanggal = ''
        self.reqSch_groupBy = ''
        self.reqSch_reportPIC = ''
        self.reqSch_orgNama = ''
        self.reqSch_ktgriNama = ''
        self.reqSch_lastUpdate = ''
        self.reqSch_aktifYN = ''

    def availableTask(self):
        try:
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()

            listAvailTask = cursor.execute('''SELECT req_id, req_judul, user_name, ktgri_nama,
                                        req_date, req_deadline, req_prioritas
                                        FROM t_request a
                                        LEFT JOIN m_user b
                                            ON  a.user_id = b.user_id
                                        LEFT JOIN m_kategori c
                                            ON  a.ktgri_id = c.ktgri_id
                                        WHERE req_status LIKE 'Waiting%' ORDER BY req_id''')
            listAvailTask = cursor.fetchall()


            for row in listAvailTask:
                requestId = row[0]
                requestJudul = row[1]
                requestNama = row[2]
                requestKategori = row[3]
                requestTanggal = row[4]
                requestDeadline = row[5]
                requstPrioritas = row[6]

            return listAvailTask
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
            print("MySQL connection is closed")

    def listTask(self):
        try:
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()

            listTask = cursor.execute(''.join(['SELECT req_id, req_judul, user_name, ktgri_nama, req_date, req_deadline, req_prioritas FROM t_request a LEFT JOIN m_user b ON  a.user_id = b.user_id LEFT JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id WHERE req_PIC = "'+session['username']+'" ORDER BY req_id']))
            listTask = cursor.fetchone()

            # for row in listTask:
            #     listId = row[0]
            #     listJudul = row[1]
            #     listNama = row[2]
            #     listKategori = row[3]
            #     listTanggal = row[4]
            #     listDeadline = row[5]
            #     listPrioritas = row[6]
            return listTask



        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
            print("MySQL connection is closed")
            
    def getRequestId(self):
            request_id = request.form['buttonDetail']
            try: 
                connection = mysql.connector.connect(
                host='localhost',
                database='cms_template',
                user='root',
                password='qwerty')
                if connection.is_connected():
                    db_Info= connection.get_server_info()
                print("Connected to MySQL database...",db_Info)

                cursor = connection.cursor()
         
                cursor.execute(''.join(['select req_id from t_request where req_id = "'+request_id+'"']))
                
                listKodeReport = cursor.fetchall()
                
                return listKodeReport

            except Error as e :
                print("Error while connecting file MySQL", e)
            finally:
                    #Closing DB Connection.
                        if(connection.is_connected()):
                            cursor.close()
                            connection.close()
                        print("MySQL connection is closed")
        


    def getDetailTask(self, request_id):
        self.detail_task=''
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
            cursor.execute(''.join(['SELECT *  FROM t_request a LEFT JOIN m_organisasi b ON a.org_id = b.org_id LEFT JOIN m_kategori c ON a.ktgri_id = c.ktgri_id LEFT JOIN t_reqSchedule d ON a.req_id = d.req_id  WHERE a.req_id = "'+request_id+'"']))            
            #cursor.execute(''.join(['SELECT * FROM m_organisasi

            #cursor.execute(''.join(['SELECT a.req_id, IFNULL(req_judul,''), IFNULL(req_deskripsi,''), IFNULL(org_nama,''), IFNULL(ktgri_nama,''), IFNULL(req_tampilan,''), IFNULL(req_periode,''), IFNULL(req_deadline,''), IFNULL(reqSch_hari,''), IFNULL(reqSch_bulan,''), IFNULL(reqSch_tanggal,'') FROM t_request a INNER JOIN m_organisasi b ON  a.org_id = b.org_id INNER JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id INNER JOIN   t_reqSchedule d ON  a.req_id = d.req_id WHERE a.req_id = "'+request_id+'"']))            
            detail_task = cursor.fetchone()
            #clear = str(record).replace("('",'').replace("',)",'')
            # for row in detail_task:
            #     detailId = row[0]
            #     detailJudul = row[1]
            #     detailDeskripsi = row[2]
            #     detailOrganisasi = row[3]
            #     detailKategori = row[4]
            #     detailTampilan = row[5]
            #     detailPeriode = row[6]
            #     detailDeadline = row[7]
            #     detailHari = row[8]
            #     detailBulan = row[9]
            #     detailTanggal = row[10]
            return detail_task

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")


    def confirmRequest(self, request_id):
        self.confirm=''
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()

            cursor.execute('update t_request set req_status = "On Process", req_PIC = "'+session['username']+'" where req_id = "'+request_id+'"')

            connection.commit()
            confirmRequest = cursor.fetchone()


            return confirmRequest
            print ("Record Updated successfully ")
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

