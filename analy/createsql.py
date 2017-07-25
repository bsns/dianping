
def createdianpingshop():
    import MySQLdb
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='okgoogle', charset="utf8")
    cursor=conn.cursor()
    cursor.execute("""create database if not exists dianpingshop""")
    conn.select_db('dianpingshop')
    sql = """CREATE TABLE dianpingshop (
        shopname  CHAR(45) NOT NULL,
         shoplevel  CHAR(45),
         shopurl CHAR(45) primary key,
         reviewnum INT(10),
         avgcost INT(10),
         taste FLOAT,
         env FLOAT,
         service FLOAT,
         foodtype CHAR(45),
         location CHAR(45)
        ) DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    cursor.close()
    print "Create database&table dianpingshop sucessful!"
#db.close()

def create_user():
    import MySQLdb
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='okgoogle', charset="utf8")
    cursor=conn.cursor()
    conn.select_db('dianpingshop')
    sql = """CREATE TABLE user (
         city CHAR(45) NOT NULL,
         gender  CHAR(45),
         birthday CHAR(45) ,
         is_vip INT(11),
         contribution INT(11),
         _id INT(11) primary key,
         user_name CHAR(45)
        ) DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    cursor.close()
    print "Create table user sucessful!"

def create_pagecomment():
    import MySQLdb
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='okgoogle', charset="utf8")
    cursor=conn.cursor()
    conn.select_db('dianpingshop')
    sql = """CREATE TABLE pagecomment (
         content LONGTEXT,
         user_id  INT(11) primary key,
         stars TEXT(45),
         avg_cost TEXT(45),
         shop_id INT(11),
         label_1 TEXT(45),
         label_2 TEXT(45),
         label_3 TEXT(45),
         _id INT(11),
         user_name CHAR(45),
         likes TEXT(45)
        ) DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    cursor.close()
    print "Create table pagecomment sucessful!"

def create_user_list_shop():
    import MySQLdb
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='okgoogle', charset="utf8")
    cursor=conn.cursor()
    conn.select_db('dianpingshop')
    sql = """CREATE TABLE user_shop (
         shopname CHAR(45) NOT NULL,
         shopurl  CHAR(45),
         shoplevel INT(5),
         _id INT(11)
         ) DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    cursor.close()
    print "Create table user_shop sucessful!"

def createyangzhoushop():
    import MySQLdb
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='okgoogle', charset="utf8")
    cursor=conn.cursor()
    #cursor.execute("""create database if not exists dianpingshop""")
    conn.select_db('dianpingshop')
    sql = """CREATE TABLE yangzhoushop (
        shopname  CHAR(45) NOT NULL,
         shoplevel  CHAR(45),
         shopurl CHAR(45) primary key,
         reviewnum INT(45),
         avgcost INT(10),
         taste FLOAT,
         env FLOAT,
         service FLOAT,
         foodtype CHAR(45),
         location CHAR(45)
        ) DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    cursor.close()
    print "Create database&table yangzhoushop sucessful!"

if __name__ == '__main__':
    print "Enter 1:create database"
    print "Enter 2:create user"
    print "Enter 3:create pagecomment"
    print "Enter 4:create user_shop"
    print "Enter 5:create yangzhoushop"
    print "Enter 6:create all tables"
    choice = int(raw_input("Input your choice:"))
    if choice == 1:
        createdianpingshop()
    elif choice == 2:
         create_user()
    elif choice == 3:
         create_pagecomment()
    elif choice == 4:
         create_user_list_shop()
    elif choice == 5:
        createyangzhoushop()
    elif choice == 6:
        createdianpingshop()
        create_pagecomment()
        create_user()
        create_user_list_shop()
        createyangzhoushop()
    else:
        print "Error!"
