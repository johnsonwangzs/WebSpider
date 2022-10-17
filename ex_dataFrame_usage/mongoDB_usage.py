# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-14
# @file    : mongoDB_usage.py
# @function: MongoDB的使用。
"""
MongoDB是非关系型数据库的一种，是一个基于分布式文件存储的开源数据库系统。
其内容的存储形式类似JSON对象，它的字段值可以包含其他文档、数组及文档数组，非常灵活。
"""

import pymongo

# 连接MongoDB
client = pymongo.MongoClient(host='localhost', port=27017)
# client = pymongo.MongoClient('mongodb://localhost:27017/')  # 直接传入MongoDB的连接字符串

# 指定数据库
print(client.list_database_names())
# db = client.test
db = client['test']
print('-'*32)

# 指定集合
print(db.list_collection_names())
# collection = db.students
collection = db['students']
print('='*32)


def insert_data_single():
    """
    插入单条数据
    :return:
    """
    student = {
        'id': '20170101',
        'name': '李白',
        'age': 20,
        'gender': 'male'
    }
    result = collection.insert_one(student)
    print(result)


def insert_data_multi():
    """
    插入多条数据
    :return:
    """
    student_1 = {
        'id': '20170101',
        'name': '李白',
        'age': 20,
        'gender': 'male'
    }
    student_2 = {
        'id': '20170102',
        'name': '杜甫',
        'age': 21,
        'gender': 'male'
    }
    result = collection.insert_many([student_1, student_2])
    print(result)


def find_data_single():
    """
    查询单个数据
    :return:
    """
    result = collection.find_one({'name': '李白'})
    print(type(result))
    print(result)


def find_data_multi():
    """
    查询多个数据
    :return:
    """
    results = collection.find({'age': 20})
    print(results)  # 返回一个生成器
    for result in results:
        print(result)
    print('-'*32)
    # 查询age>20的数据：
    results = collection.find({'age': {'$gt': 20}})
    for result in results:
        print(result)
    print('-'*32)
    # 正则表达式
    results = collection.find({'age': {'$regex': '^M.*'}})
    for result in results:
        print(result)


def sort_data():
    """
    排序
    :return:
    """
    results = collection.find().sort('name', pymongo.ASCENDING)
    print([result['name'] for result in results])


def update_data_single():
    """
    更新单条数据
    :return:
    """
    condition = {'name': '李白'}
    result = collection.update_one(condition, {'$set': {'age': 40}})
    print(result)
    print(result.matched_count, result.modified_count)  # 匹配的数据条数和影响的数据条数


def update_data_multi():
    """
    更新多条数据
    :return:
    """
    condition = {'age': {'$gt': 20}}
    result = collection.update_many(condition, {'$inc': {'age': 1}})
    print(result)


def delete_data_single():
    """
    删除单条数据
    :return:
    """
    result = collection.delete_one({'name': '杜甫'})
    print(result)
    print(result.deleted_count)


def delete_data_multi():
    """
    删除多条数据
    :return:
    """
    result = collection.delete_many({'name': '李白'})
    print(result)
    print(result.deleted_count)


if __name__ == '__main__':
    delete_data_multi()
