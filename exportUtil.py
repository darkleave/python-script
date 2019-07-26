import pymysql,xlwt

def export_excel(table_name):
    import pymysql
    host, user, passwd, db = '', '', '', ''
    conn = pymysql.connect(user=user,host=host,port=3306,passwd=passwd,db=db,charset='utf8')
    cur = conn.cursor()  # 建立游标
    sql = 'select * from %s;' %table_name
    cur.execute(sql)  # 执行mysql
    fileds = [filed[0] for filed in cur.description]  # 列表生成式，所有字段
    all_data = cur.fetchall() #所有数据
    #写excel
    book = xlwt.Workbook() #先创建一个book
    sheet = book.add_sheet('sheet1') #创建一个sheet表
    # col = 0
    # for field in fileds: #写表头的
    #     sheet.write(0, col, field)
    #     col += 1
    #enumerate自动计算下标
    for col, field in enumerate(fileds): #跟上面的代码功能一样
        sheet.write(0, col, field)

    #从第一行开始写
    row = 1 #行数
    for data in all_data:  #二维数据，有多少条数据，控制行数
        for col, field in enumerate(data):  #控制列数
            sheet.write(row, col, field)
        row += 1 #每次写完一行，行数加1
    book.save('%s.xls' %table_name) #保存excel文件

export_excel('')