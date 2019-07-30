import pymysql,xlwt,aesUtil

def export_excel(table_name):
    import pymysql
    #host, user, passwd, db = '47.97.30.34', 'root', 'j24I2exy04tYjgCX', 'human-resource'
    host, user, passwd, db = '47.97.58.5', 'root', 'Dreamtech%9ZXy', 'human-resource'

    conn = pymysql.connect(user=user,host=host,port=3306,passwd=passwd,db=db,charset='utf8')
    cur = conn.cursor()  # 建立游标
    sql = 'select * from %s ;' %table_name
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

def export_excel_by_sql(sql):
    import pymysql
    #host, user, passwd, db = '47.97.30.34', 'root', 'j24I2exy04tYjgCX', 'human-resource'
    host, user, passwd, db = '47.97.58.5', 'root', 'Dreamtech%9ZXy', 'human-resource'
    conn = pymysql.connect(user=user,host=host,port=3306,passwd=passwd,db=db,charset='utf8')
    cur = conn.cursor()  # 建立游标
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
            if(col == 1 and field):
                field = aesUtil.aes_ecb_decrypt_auto('b42effGcSYwzVH1e138L1JkM8aR4XXwQ',field)
                field = field.strip()
            sheet.write(row, col, field)
        row += 1 #每次写完一行，行数加1
    book.save('tempExport.xls') #保存excel文件

#export_excel('t_member')

sql = '''
select a.f_full_name as '姓名',a.f_phone_number as '手机号码',d.f_name as '组织机构',
(case (a.f_sex) when 0 then '男' when 1 then '女' else null end) as '性别',c.f_value as '民族',e.f_credential_value as '身份证号',
a.f_email as '邮箱' from t_member a inner join t_member_detail b on a.f_id = b.f_member_id 
left join t_member_config c on b.f_ethnicity_id = c.f_id 
left join t_organization d on a.f_organization_id = d.f_id 
left join t_member_detail e on a.f_id = e.f_member_id 
where a.f_phone_number is not null
'''
export_excel_by_sql(sql)