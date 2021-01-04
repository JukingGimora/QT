create database stock;
use stock;

create table HEAD
(
ID int(10) primary key auto_increment comment '主键',
CODE varchar(30) comment '代码',
NAME varchar(50) comment '名称',
);

create table BODY
(
ID int(10) primary key auto_increment comment '主键',
CODE varchar(30) comment '代码',
ORG_FORM varchar(50) comment '组织形式',
AREA varchar(50) comment '地区',
CHN_ABBR varchar(50) comment '中文简称',
OFFICE_ADDRESS varchar(100) comment '办公地址',
FULL_NAME varchar(50) comment '公司全称',
TELEPHONE varchar(50) comment '公司电话',
ENG_NAME  varchar(100) comment '英文名称',
MAIL varchar(50) comment '电子邮箱',
REG_CAPITAL varchar(20) comment '注册资本',
CHAIRMAN varchar(50) comment '董事长',
STAFF_NUM varchar(50) comment '员工人数',
SECRETARY varchar(50) comment '董事会秘书',
REPRESENTATIVE varchar(50) comment '法人代表',
SECRETARY_PHONE varchar(50) comment '董秘电话',
MANAGER varchar(50) comment '总经理',
SECRETARY_FOX varchar(50) comment '董秘传真',
COMPANY_WEB varchar(50) comment '公司网址',
SECRETARY_MAIL varchar(50) comment '董秘邮箱',
DISCLOSURE_WEB varchar(50) comment '信息披露网址',
DISCKOSURE_NEWS varchar(100) comment '信息披露报纸',
MAIN_BUSINESS text comment '主营业务',
NATURE_BUSINESS text comment '经营范围',
HISTORY text comment '公司沿革',
ESTABLISHMENT_TIME varchar(10) comment '成立时间',
MARKET_TIME varchar(10) comment '上市时间',
DISTRIBUTION text comment '发行方式',
FACE_VALUE varchar(20) comment '面值',
NUMBER varchar(20) comment '发行数量',
PRICE varchar(20) comment '发行价格',
FUND varchar(50) comment '募资资金总额',
FEE varchar(20) comment '发行费用',
WINNING varchar(10) comment '中签率',
PE varchar(10) comment '市盈率',
EPS varchar(20) comment '发行后每股收益',
PNE varchar(20) comment '发行后每股净资产',
OPENING_PRICE varchar(20) comment '上市首日开盘价',
CLOSING_PRICE varchar(20) comment '上市首日收盘价',
TURNOVER_RATE varchar(20) comment '上市首日换手率',
UNDERWRITER varchar(50) comment '主承销商',
SPONSOR varchar(50) comment '上市保荐人',
ACCOUNTING_FIRM varchar(50) comment '会计事务所'
);

create table LIMB
(
ID int(10) primary key auto_increment comment '主键',
TRADE_DATE varchar(10) comment '日期',
CODE varchar(30) comment '股票代码',
NAME varchar(30) comment '名称',
TCLOSE decimal(7,2) comment '收盘价',
HIGH decimal(7,2) comment '最高价',
LOW decimal(7,2) comment '最低价',
TOPEN decimal(7,2) comment '开盘价',
LCLOSE decimal(7,2) comment '前收盘',
CHG decimal(7,2) comment '涨跌额',
PCHG decimal(10,5) comment '涨跌幅',
TURNOVER decimal(10,5) comment '换手率',
VOTURNOVER bigint(20) comment '成交量',
VATURNOVER decimal(20,2) comment '成交金额',
TCAP decimal(20,2) comment '总市值',
MCAP decimal(20,2) comment '流通市值'
);