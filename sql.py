import pymysql
import constants

class sql:

    #建立连接
    def open(self):
        conn = pymysql.connect(host=constants.host, user=constants.username, password=constants.password,
                                      database=constants.database, charset=constants.charset)
        return conn

    #关闭连接
    def close(self,conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    #查询语句
    def select(self, sql):
        #打开连接
        conn = self.open()
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        # 关闭连接
        self.close(conn, cursor)
        return data

    #批量插入或修改语句
    def operation(self, sql, items):
        # 打开连接
        conn = self.open()
        cursor = conn.cursor()
        #批量插入
        cursor.executemany(sql, items)
        # 关闭连接
        self.close(conn, cursor)

    #单个插入或修改语句
    def operate(self, sql, item):
        # 打开连接
        conn = self.open()
        cursor = conn.cursor()
        cursor.execute(sql, item)
        # 关闭连接
        self.close(conn, cursor)