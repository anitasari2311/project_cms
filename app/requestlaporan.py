import datetime
import pymysql
import random
import mysql.connector
from mysql.connector import Error
#from db import get_db_cms_request



class RequestLaporan:
   
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
        


       
#BUAT PROSES 
    
    def getUserID(self,username):
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
     
            cursor.execute(''.join(['select user_id from m_user where user_name = "'+username+'"']))
            
            record = cursor.fetchone()
            clear = str(record).replace("('",'').replace("',)",'')
            return clear

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

    def prosesLogin(self, username, password):
        
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
                # SESSION BELOM BISA
                # cursor.execute ('SELECT * FROM m_user WHERE user_name =?', (username,)).fetchone()
                # if cursor is None:
                #     error = 'Incorrect'
                # elif cursor is None:
                #     error = 'Incorrect'

                # if error is None:
                #     session.clear()
                #     session ['user_id'] = cursor['user_id']
                #     return redirect(url_for('menu'))
                # flash (error)

                cursor.execute(''.join(['select user_password, user_flag from m_user where user_name = "'+username+'"']))
                
                record = cursor.fetchone()
                clear = str(record).replace("('",'').replace("')",'').replace("', '",'#')

                stat = clear.split('#')
                if stat[0] == password:
                    return stat[1]
                else:
                    return "incorrect"

            except Error as e :
                print("Error while connecting file MySQL", e)
            finally:
                    #Closing DB Connection.
                        if(connection.is_connected()):
                            cursor.close()
                            connection.close()
                        print("MySQL connection is closed")
        

#BUAT GENERATE ID SECARA OTOMATIS
    def get_numberID(self):
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
     
            cursor.execute('select count(req_id) from t_request where month(req_date) = month(now())')
            
            record = cursor.fetchone()
            clear = str(record).replace('(','').replace(',)','')
            return int(clear)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")
        
    def generateRequestID(self):
        now  = datetime.datetime.now()
        requestID = 'REQ_'+str(now.strftime('%Y%m'))+str(self.get_numberID()).zfill(5)
        return requestID
    
#BUAT REQUEST UNTUK LAPORAN BARU
    def getOrganisasi(self, organisasi):
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
     
            cursor.execute(''.join(['select org_id from m_organisasi where org_nama = "'+organisasi+'"']))
            
            record = cursor.fetchone()
            clear = str(record).replace("('",'').replace("',)",'')
            return clear

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

    def namaOrganisasi(self):
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
        
            listOrg = cursor.execute('select org_id, org_nama from m_organisasi where org_aktifYN = "Y" order by org_id')
            listOrg = cursor.fetchall()

            #cursor = connection.cursor()
    
        #listOrg = cursor.execute('select org_id, org_nama from m_organisasi where org_aktifYN = "Y" order by org_id')
            
        #listOrg = cursor.fetchall()

            
            return listOrg

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")
    def namaDept(self):
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
     
            cursor.execute('select ktgri_id, ktgri_nama from m_kategori where ktgri_aktifYN = "Y" Order by ktgri_id')
            
            listDept = cursor.fetchall()
   
            return listDept
            

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")
                    
    def listRequestUser(self, username):
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
            cursor.execute  (''.join(['SELECT req_id ,IFNULL(req_judul,""), IFNULL(req_date,""),IFNULL(req_deadline,""), IFNULL(req_status,""), IFNULL(req_PIC,"") from t_request WHERE user_id="'+RequestLaporan().getUserID(username)+'"']))
            listReqUser = cursor.fetchall()
            return listReqUser
        
        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")


                    
    def requestLaporanBaru(self, prog_id, user_id, org_id, ktgri_id, req_kodeLaporan, req_judul, req_deskripsi,
                           req_tujuan, req_tampilan, req_periode, req_deadline, req_file, req_PIC, req_penerima,
                           req_dateAccept = None, req_endDate=None, req_status='Waiting', req_prioritas='1'):
        self.req_id = self.generateRequestID()
        self.prog_id = prog_id
        self.user_id  = user_id
        self.org_id = self.namaOrganisasi()
        self.ktgri_id = ktgri_id
        self.req_kodeLaporan = req_kodeLaporan
        self.req_judul = req_judul
        self.req_deskripsi = req_deskripsi
        self.req_tujuan = req_tujuan 
        self.req_tampilan = req_tampilan
        self.req_periode = req_periode                                          
        self.req_deadline = req_deadline
        self.req_file = req_file
        self.req_date  = datetime.datetime.now()
        self.req_dateAccept = req_dateAccept
        self.req_endDate = req_endDate
        self.req_status = req_status
        self.req_PIC = req_PIC
        self.req_penerima = req_penerima
        self.req_prioritas = req_prioritas


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
            cursor.execute('INSERT INTO t_request VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (self.req_id, prog_id, user_id, org_id, ktgri_id, req_kodeLaporan, req_judul, req_deskripsi,
                           req_tujuan, req_tampilan, req_periode,req_deadline,req_file, self.req_date,
                            req_dateAccept, req_endDate, self.req_status, req_PIC, req_penerima, req_prioritas))
            connection.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

#BUAT INSERT INTO T_Req_SCH
    def requestSchedule(self, sch_id, report_id, query_id, reqSch_hari, reqSch_bulan, reqSch_tanggal, reqSch_groupBy, reqSch_reportPIC, reqSch_orgNama,reqSch_ktgriNama,reqSch_lastUpdate, reqSch_aktifYN):
        self.sch_id = sch_id
        self.report_id = report_id
        self.query_id = query_id
        self.reqSch_hari = reqSch_hari
        self.reqSch_bulan = reqSch_bulan
        self.reqSch_tanggal = reqSch_tanggal
        self.reqSch_groupBy = reqSch_groupBy
        self.reqSch_reportPIC = reqSch_reportPIC
        self.reqSch_orgNama = reqSch_orgNama
        self.reqSch_ktgriNama = reqSch_ktgriNama
        self.reqSch_lastUpdate = datetime.datetime.now()
        self.reqSch_aktifYN = reqSch_aktifYN
    
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
            cursor.execute('INSERT INTO t_reqSchedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (sch_id, report_id, query_id, reqSch_hari, reqSch_bulan, reqSch_tanggal, reqSch_groupBy,
                            reqSch_reportPIC, reqSch_orgNama, reqSch_ktgriNama, reqSch_lastUpdate, reqSch_aktifYN))
            connection.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")
#======================================================================================================================
#BUAT GET DATA REPORT_ID
    def getReportID(self):
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
     
            cursor.execute('select report_id from m_report')
            
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
        
    def requestEditLap(self, req_tampilan, req_deskripsi, req_deadline):
        self.req_id = self.generateRequestID()
        self.new_display = req_deskripsi
        self.perubahan_filter = perubahanFilter
        self.deadline = req_deadline
        self.req_date  = datetime.datetime.now()

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
        
            cursor.execute('INSERT INTO t_request VALUES (%s, %s, %s, %s), %s)',
                           (self.req_id, prog_id, user_id, org_id, ktgri_id, req_kodeLaporan, req_judul, req_deskripsi,
                           req_tujuan, req_tampilan, req_periode,req_deadline,req_file, self.req_date,
                            req_dateAccept, req_endDate, self.req_status, req_PIC, req_penerima, req_prioritas))
           #connection.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

                    
                          
#=========================================BUAT PANGGIL=======================================
#RequestLaporan().requestSchedule('SCH-004', 'DGM-0330', 'Q123', 'Senin', 'Januari', '4','Dr. Andre Lembong',
#                       'Monic', 'Pharos', 'Sales Management', datetime.datetime.now(), 'Y')        
#           
#RequestLaporan().requestLaporanBaru('BM-01', 'UU-01', '2', 'BD-01', 'DGM-001', 'Laporan Sales', 'filter<5000', 'untuk mengetahui',
#                               'outcode', 'B1', datetime.date(2019,7,12), 'laporan', None, None,
#                               'confirmed', 'Monic', 'jhgygvy', 'N')
#

#print(RequestLaporan().test())
#print(RequestLaporan().prosesLogin('Monica','1234'))
#print (RequestLaporan().getUserID('yoona'))
