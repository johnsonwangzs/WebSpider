# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-11
# @file    : mysql_usage.py
# @function: MySQL存储。
"""
在Python2中，连接MySQL的库大多是MySQLdb，但其不支持Python3。因此一般使用的库是PyMySQL。
"""

import pymysql


def create_database():
    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306)  # 声明一个MySQL连接对象
    cursor = db.cursor()  # 获得MySQL的操作游标
    cursor.execute('SELECT VERSION()')  # 获得MySQL的当前版本
    data = cursor.fetchone()  # 获得第一条数据
    print('Database version:', data)
    cursor.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET utf8mb4")  # 创建数据库
    db.close()


def create_table():
    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL,' \
          ' age INT NOT NULL, PRIMARY KEY (id))'
    cursor.execute(sql)
    db.close()


def insert_data_simple():
    uid = '20120001'
    user = '李白'
    age = 20
    """
    对于插入、更新、删除等数据库的更改操作，必须使用标准的写法，以确保事务的ACID属性（尤其是一致性）
    """
    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    sql = 'INSERT INTO students(id,name,age) VALUES(%s,%s,%s)'
    try:
        cursor.execute(sql, (uid, user, age))
        db.commit()  # 提交数据库
    except:
        db.rollback()  # 若执行失败，则进行数据回滚
    db.close()


def insert_data_pro():
    """
    通过传入一个字典来插入数据，不需要再修改sql语句和插入操作
    """
    data = {
        'id': '20120002',
        'name': '杜甫',
        'age': 21
    }
    table = 'students'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))  # ['%s', '%s', '%s'] -> '%s, %s, %s'
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)  # 动态的sql语句

    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    try:
        if cursor.execute(sql, tuple(data.values())):
            print('Successful!')
            db.commit()
    except:
        print('Failed!')
        db.rollback()
    db.close()


def update_data_simple():
    """
    更新数据（基础写法）。
    :return:
    """
    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    sql = 'UPDATE students SET age = %s WHERE name = %s'
    try:
        cursor.execute(sql, (25, '李白'))
        db.commit()
    except:
        db.rollback()
    db.close()


def update_data_pro():
    """
    更新数据（高级写法）。
    INSERT语句与ON DUPLICATE KEY配合，可以实现主键不存在便插入数据，逐渐存在则更新数据的功能。
    :return:
    """
    data = {
        'id': '20120001',
        'name': '李白',
        'age': 22
    }
    table = 'students'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=table, keys=keys,
                                                                                          values=values)
    update = ','.join(['{key} = %s'.format(key=key) for key in data])
    sql += update
    try:
        # 实际的sql: INSERT INTO students(id,name,age) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE id=%s,name=%s,age=%s
        if cursor.execute(sql, tuple(data.values())*2):
            print('Successful!')
            db.commit()
    except:
        print('Failed!')
        db.rollback()
    db.close()


def delete_data():
    table = 'students'
    condition = 'age > 21'
    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def select_data():
    sql = 'SELECT * FROM students WHERE age >= 20'
    db = pymysql.connect(host='localhost', user='admin123456', password='123456', port=3306, db='spiders')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        print('Count:', cursor.rowcount)
        one = cursor.fetchone()  # 获取结果中的第一条数据
        print('One:', one)
        # 注意，fetch方法有一个偏移指针，经过以上fetchone得到第一条数据后，fetchall无法再获得该条数据
        results = cursor.fetchall()  # 获取结果中的所有数据
        print('Results:', results)
        print('Results type:', type(results))
        for row in results:
            print(row)
    # 为减少内存的使用，推荐如下写法：
    # try:
    # cursor.execute(sql)
    # print('Count:', cursor.rowcount)
    # row = cursor.fetchone()
    # while row:
    #     print('Row:', row)
    #     row = cursor.fetchone()
    except:
        print('Error')


if __name__ == '__main__':
    select_data()
