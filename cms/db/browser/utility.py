# -*- coding: utf-8 -*-


def filter_cln(cls):
    "过滤指定表类的列,只保留基本属性列"            

    from sqlalchemy.inspection import inspect
    table = inspect(cls)
    columns = [column.name for column in table.c]
    #过滤主键,外键
    columns = filter(lambda elem: not elem.endswith("id"),columns)
    return columns 