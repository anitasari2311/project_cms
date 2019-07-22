/*                      MS1              */
CREATE TABLE m_organisasi(
	org_id varchar(15) primary key not null,
    org_nama varchar(150) not null,
    org_aktifYN char(1) not null
);

CREATE TABLE m_kategori (
	ktgri_id varchar(15) primary key not null,
    ktgri_nama varchar(150) not null,
    ktgri_aktifYN char(1) not null
);

CREATE TABLE m_programmer(
	prog_id varchar(15) primary key not null,
    prog_nama varchar(150) not null,
    prog_password varchar(150) not null,
    prog_posisi varchar(150) not null,
    prog_email varchar(150) not null,
    prog_taskNormal varchar(50),
    prog_taskImportant varchar(50),
    prog_aktifYN char(1) not null
);

CREATE TABLE m_user (
	user_id varchar(15) primary key not null,
    user_name varchar(150) not null,
    user_password varchar(150) not null,
    user_posisi varchar(150) not null,
    user_email varchar(150) not null,
    user_flag varchar(150) not null,
    user_aktifYN char(1) not null
);

CREATE TABLE t_request (
	req_id varchar(15) primary key not null,
    prog_id varchar(15) references m_programmer(prog_id),
	user_id varchar(15) references m_user(user_id),
    org_id varchar(15) references m_organisasi(org_id),
    ktgri_id varchar(15) references m_kategori(ktgri_id),
    req_kodeLaporan varchar(15) not null,
    req_judul varchar(150) not null,
    req_deskripsi varchar(250),
    req_tujuan varchar(250) not null,
    req_tampilan varchar(150) not null,
    req_periode varchar(15) not null,
    req_deadline datetime,
    req_file blob,
    req_date datetime,
    req_dateAccept datetime,
    req_endDate datetime,
    req_status varchar(150) not null,
    req_PIC varchar(150) not null,
	req_penerima varchar(150),
    req_prioritas char(1) not null
);

CREATE TABLE t_reqSchedule (
	sch_id varchar(15) primary key not null,
    report_id varchar(15) not null,
    query_id varchar(15) not null,
    reqSch_hari varchar(150) not null,
    reqSch_bulan varchar(150) not null,
    reqSch_tanggal varchar(150) not null,
    reqSch_groupBy varchar(150) not null,
    reqSch_reportPIC varchar(150) not null,
    reqSch_orgNama varchar(150) not null,
    reqSch_ktgriNama varchar(150) not null,
    reqSch_lastUpdate datetime,
    reqSch_aktifYN char(1) not null
);

select * from t_reqSchedule;


/*                 MS2               */

/*tambahin report_id*/
CREATE TABLE m_server(
	server_id varchar(15) primary key not null,
    server_nama varchar(150) not null,
    server_loginName varchar(150) not null,
    server_password varchar(150) not null,
    server_aktifYN char(1) not null
);

CREATE TABLE m_query (
	query_id varchar(15) primary key not null,
    query_no varchar(15) not null,
    query_query varchar(500) not null,
    query_lastUpdate datetime,
    query_aktifYN char(1) not null
) ;

CREATE TABLE m_report(
	report_id varchar(15) primary key not null,
    query_id varchar(15) references m_query(query_id),
    server_id varchar(15) references m_server(server_id),  
    sch_id varchar(15) not null,
    report_judul varchar(150) not null,
    report_deskripsi varchar(150) not null,
    report_tujuan varchar(150) not null,
    report_header varchar(150) not null,
    report_footer varchar(150) not null,
    report_tampilan varchar(150) not null,
	report_jumlahTampilan varchar(150) not null,
    report_PIC varchar(150) not null,
	report_periode varchar(150) not null,
    report_createdDate datetime,
    report_userUpdate varchar(150) not null,
    report_penerima varchar(150) not null,
    report_lastUpdate datetime,
    report_aktifYN char(1) not null
);

CREATE TABLE t_schedule (
	sch_id varchar(15) primary key not null,
    report_id varchar(15) references m_report (report_id),
    query_id varchar(15) references m_query (query_id),
    req_id varchar(15) not null,
    sch_hari varchar(150) not null,
    sch_bulan varchar(150) not null,
    sch_tanggal varchar(150) not null,
    sch_groupBy varchar(150) not null,
    Sch_reportPIC varchar(150) not null,
    Sch_orgNama varchar(150) not null,
    Sch_ktgriNama varchar(150) not null,
    sch_lastUpdate datetime,
    sch_aktifYN char(1) not null
);

INSERT INTO m_organisasi VALUES 
("25", "PRORESULT KREASI UTAMA", "Y"),
("26", "PERCETTAKAN MITRA UTAMA","Y"),
("27","PT. CAKRAWALA LARAS ADIWARNA","Y"),
("28","PT. DUTA NIAGA PRATAMA","Y"),
("29","PT. PRIMATAX","Y"),
("30","PT. CENTURY HEALTH CARE","Y"),
("31","PT. CENTURY FRANCHISINDO UTAMA","Y"),
("34","RETAIL GROUP","Y"),
("35","APOLLO","Y"),
("36","PT. PERINTIS PELAYANAN PARIPURNA","Y"),
("37","PT. PHARINDO LABORATORIES","Y"),
("38","PT. SARUA SUBUR","Y"),
("39","TESTORGANISASI","Y"),
("40","SMARTBOX","Y"),
("41","PT. PRIMAXEL","Y"),
("33","PT. PERINTIS GENERIK INDONESIA","Y"),
("18","INTI UTAMA SOLUSINDO","Y"),
("19","AVECCA","Y"),
("20","DIAGNOSTIC","Y"),
("21","SOFTNET GLOBAL SOLUSINDO","Y"),
("24","CENTURY MALL OFFICE","Y"),
("23","PHAROS GROUP","Y"),
("1","APOTIK GENERIK","Y"),
("2","CENTURY STANDALONE","Y"),
("3","PHARMANET","Y"),
("10","PHAROS","Y"),
("11","CENTURY GROUP","Y"),
("12","PT. FARATU","Y"),
("13","NUTRINDO JAYA ABADI","Y"),
("14","PRIMA MEDIKA LABORATORIES","Y"),
("15","NUTRISAINS","Y"),
("16","CENTURY MALL FOKUS","Y"),
("17","MITRA INSAN SEJAHTERA","Y"),
("32","CENTURY MALL KHUSUS","Y");

INSERT INTO m_kategori VALUES 
("BSD-01", "BUSINESS DEVELOPMENT MANAGEMENT", "Y"),
("SCM-01", "SUPPLY CHAIN MANAGEMENT","Y"),
("ME-01", "MAINTENANCE & ENGINEERING","Y"),
("MP-01", "MANAGEMENT PRODUCT","Y"),
("MT-01", "MANAGEMENT TRAINING","Y"),
("FN-01", "FINANCE MANAGEMENT","Y"),
("MG-01", "MANAGEMENT GA","Y"),
("HR-01", "HR MANAGEMENT","Y"),
("MK-01", "MARKETING MANAGEMENT","Y"),
("SL-01", "SALES MANAGEMENT","Y"),
("FM-01", "FACTORY MANAGEMENT","Y"),
("PM", "PURCHASING MANAGEMENT","Y"),
("RD", "RND MANAGEMENT","Y"),
("SP", "SOFTWARE PROJECT MANAGEMENT","Y");

INSERT INTO M_SERVER VALUES 
("1", "OCULUS", "reporting_dept", "r3porting", "Y"),
("2", "PHARMANETDB1","proces","wicdt", "Y"),
("3", "XENIA","genproces","2013p0w3rapril", "Y"),
("4", "AVANZA","Avanza","avanza", "Y"),
("5", "HORUS","proces","wicdt", "Y"),
("6", "KSATRIA","mis_pgi","pgiwicdt", "Y"),
("7", "MUSTANG","crp","oct5spirit2012", "Y"),
("8", "NTSQL","proces","wicdt", "Y"),
("9", "NTCENTURY","proces","wicdt", "Y"),
("10","CAMARO","crp","oct5spirit2012", "Y"),
("11","MAINSERVER","proces","wicdt", "Y"),
("12","IRONMAN","proces","wicdt", "Y"),
("13","GENESIS","chika_mispgi","15ika51", "Y"),
("14","DEMETER","proces","wicdt", "Y"),
("15","GATOTKACA","proces","wicdt", "Y"),
("16","NPDSQL","andre_lembong","aplinpd", "Y"),
("18","KURAWA","mis_pgi","pgiwicdt", "Y"),
("19","PHARMANET","selvia_mis","1234", "Y"),
("21","COSMO","proces","wicdt","Y"),
("22","VUVUZELA","proces","wicdt","Y"),
("23","OSIRIS","proces","wicdt","Y"),
("24","METRIX","chika","150051","Y"),
("25","GENESISSBR","proces","wicdt","Y"),
("26","NUTRINDO","proces","wicdt","Y"),
("27","NUTRISAINS","proces","wicdt","Y"),
("28","ECONOLAB","proces","wicdt","Y"),
("29","SARUASUBUR","proces","wicdt","Y"),
("30","[52.74.0.72]","vending","v3nd1ng*2019#","Y");

use cms_request;


CREATE TABLE test (
	test1 varchar(15) primary key not null,
    test2 varchar(15) references m_report (report_id)
);

CREATE TABLE reqreq (
	req_id varchar(15) primary key not null,
    org_id varchar(15) references m_organisasi(org_id),
    ktgri_id varchar(15) references m_kategori(ktgri_id),
    req_kodeLaporan varchar(15),
    req_judul varchar(150),
    req_deskripsi varchar(250),
    req_tujuan varchar(250),
    req_tampilan varchar(150),
    req_periode varchar(15),
    req_deadline datetime,
    req_file blob,
    req_PIC varchar(150),
	req_penerima varchar(150)
);