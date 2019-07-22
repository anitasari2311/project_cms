select * from m_kategori;

ALTER TABLE m_kategori
CHANGE kategori_aktifYN kategori_aktifYN
CHAR(1) not null;

select * from m_organizationm_kategori;

CREATE DATABASE template;

ALTER TABLE t_request
ADD COLUMN kategori_id varchar(15);

alter table t_request
add foreign key (kategori_id) references m_kategori(kategori_id);

CREATE TABLE m_server (
	server_id varchar(15) primary key not null,
    server_name varchar(150) not null,
    server_loginName varchar(150) not null,
    server_password varchar(150) not null,
    server_aktifYN char(1)
);


CREATE TABLE m_query (
	query_id varchar(15) primary key not null,
    query_no varchar(15) not null,
    query varchar(500) not null,
    query_aktifYN char(1) not null,
    query_lastUpdate datetime
) ;

CREATE TABLE m_report(
	report_id varchar(15) primary key not null,
    query_id varchar(15) not null,
    server_id varchar(15) not null,  
    sch_id varchar(15) not null,
    report_nama varchar(150) not null,
    report_description varchar(150) not null,
    report_header varchar(150) not null,
    report_footer varchar(150) not null,
    report_display varchar(150) not null,
    report_PIC varchar(150) not null,
    report_createdDate datetime,
    report_endedDate datetime,
    report_lastUpdate datetime,
    report_period varchar(150) not null,
    report_aktifYN char(1),
    report_jumlahDisplay varchar(150) not null
);

CREATE TABLE t_schedule (
	sch_id varchar(50) primary key not null,
    req_id varchar(50) not null,
    sch_hari varchar(150) not null,
    sch_bulan varchar(150) not null,
    sch_tanggal varchar(150) not null,
    groupBy varchar(150) not null,
    sch_lastUpdate datetime
);
use cms_request;

select org_id, org_nama from m_organisasi;
select * from t_request;
select * from m_user;

select * from m_user where user_name = 'monica';
create table latihan (
	latihan_id varchar(15) primary key,
    latihan_desk varchar(225) not null
);

INSERT INTO m_user VALUES ('P190377','Anita','anita123','GM Reporting','anita2311@gmail.com','Atasan','Y' );
INSERT INTO m_user VALUES ('P190360','Yoshua','yoshua234','Staff','yoshua.agung@gmail.com','User','Y' );

use cms_template;
INSERT INTO m_report VALUES 
('DGM-0002','Q123','5','SCH-0001','LAPORAN MALL FOKUS',
'STOCK<500000','UNTUK MENGETAHUI BERAPA BANYAK STOCK',
'4','7','Out code, Out comco, Outlet nama','3','Nit','B0',
now(), 'Knight', 'Budi', 12/06/2019, 'Y');


select * from T_request order by org_id ;
SELECT req_id ,IFNULL(req_judul,""), IFNULL(req_date,""),
IFNULL(req_deadline,""), IFNULL(req_status,""), IFNULL(req_PIC,"")
from t_request;

use cms_template;
select * from t_request;
select * from m_report;
use cms_request;
select * from m_user;
truncate table t_request;

select * from t_request 
left join t_reqSchedule
on 

