# 股票列表api
stockListUrl = 'http://86.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124064028201763104_1562133297741&pn=1&pz' \
               '=100000&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:13,' \
               'm:0+t:80,m:1+t:2&fields=f12,f14&_=1562133297790 '

# 股票列表文件夹
stockListPath = "stock/stockList/"

# 股票历史数据文件夹
stockInfoPath = "stock/stockInfo/"

# 股票列表文件标题栏
stockListTitle = ('代码', '名称')

# IP地址
host = "127.0.0.1"

# 用户名
username = "root"

# 用户密码
password = "root"

# 数据库
database = "stock"

# 字符集
charset = "utf8"

# 股票列表csv
stockListName = "stockList_.csv"

# 插入头表语句
insert_head_sql = "insert into HEAD(CODE, NAME) values(%s, %s)"

# 修改头表语句
update_head_sql = "update HEAD set NAME = %s where CODE = %s"

# 插入身体表语句
insert_body_sql = "insert into BODY (CODE, ORG_FORM, AREA, CHN_ABBR, OFFICE_ADDRESS, FULL_NAME, " \
                  "TELEPHONE, ENG_NAME, MAIL, REG_CAPITAL, CHAIRMAN, STAFF_NUM, SECRETARY, REPRESENTATIVE, SECRETARY_PHONE, " \
                  "MANAGER, SECRETARY_FOX, COMPANY_WEB, SECRETARY_MAIL, DISCLOSURE_WEB, DISCKOSURE_NEWS, MAIN_BUSINESS, " \
                  "NATURE_BUSINESS, HISTORY, ESTABLISHMENT_TIME, MARKET_TIME, DISTRIBUTION, FACE_VALUE, NUMBER, PRICE, " \
                  "FUND, FEE, WINNING, PE, EPS, PNE, OPENING_PRICE, CLOSING_PRICE, TURNOVER_RATE, UNDERWRITER, SPONSOR, " \
                  "ACCOUNTING_FIRM) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# 上市公司基本信息url
companyInfoUrl = "http://quotes.money.163.com/f10/gszl_%s.html"

# 个股历史数据url开始
stockInfoUrlStart = 'http://quotes.money.163.com/service/chddata.html?code='

# 个股历史数据时间开始
stockInfoTimeStart = '&start='

# 个股历史数据时间结束
stockInfoTimeEnd = '&end='

# 个股历史数据url结束
stockInfoUrlEnd = '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

#个股数据插入语句
insert_limb_sql = "insert into LIMB(TRADE_DATE, CODE, NAME, TCLOSE, HIGH, LOW, TOPEN, LCLOSE, CHG, PCHG, " \
                  "TURNOVER, VOTURNOVER, VATURNOVER, TCAP, MCAP) values(%s, %s, %s, %s, %s, %s, %s, %s, %s," \
                  " %s, %s, %s, %s, %s, %s)"

#某上市公司收盘价查询语句
select_tclose_sql = "select TCLOSE from LIMB where code = %s and TRADE_DATE in (select max(TRADE_DATE) from LIMB)"

#某时间范围内上市公司平均成交量查询语句
select_turnover_sql = "select CODE, avg(TURNOVER), avg(TCLOSE) from LIMB where TRADE_DATE >= %s and TRADE_DATE <= %s  group by CODE order by avg(TURNOVER) desc"

#某上市公司收盘价、成交量查询语句
select_tclose_turnover_sql = "select TCLOSE, TURNOVER from LIMB where code = %s order by TRADE_DATE"

#最新日期收盘价在某区间范围查询语句
select_tclose_range_sql = "select CODE, TCLOSE from LIMB where TRADE_DATE in (select max(TRADE_DATE) from LIMB) and TCLOSE >= %s and TCLOSE <= %s"

# 序列段长度
time_step = 90

# 隐藏层节点数目
rnn_unit = 8

# cell层数
lstm_layers = 2

# 序列段批处理数目
batch_size = 29

# 输入维度
input_size = 1

# 输出维度
output_size = 1

# 学习率
learning_rate = 0.006

#迭代次数
iterations = 100

#模型文件名称
file_name = 'model_lstm.ckpt'

#共享变量范围
scope_name = 'scope_lstm'

#模型文件夹
modelPath = 'model/lstm/'