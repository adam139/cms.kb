# -*- coding: utf-8 -*-

def to_utf_8(lts):
    rt = []
    for i in lts:
        if isinstance(i,str):            
            rt.append(i.decode('utf-8'))
            continue
        else:
            rt.append(i)
    return rt
            
        

def map_field2cls(fieldname):
    "为编辑表单的getcontent()提供字段名到中间对象class name映射"
    dt = {'yaoes':"Yao_ChuFang_AssoUI",'bingrens':"ChuFang_BingRen_AssoUI"}
    return dt[fieldname]

def filter_cln(cls):
    "过滤指定表类的列,只保留基本属性列"            

    from sqlalchemy.inspection import inspect
    table = inspect(cls)
    columns = [column.name for column in table.c]
    #过滤主键,外键
    columns = filter(lambda elem: not elem.endswith("id"),columns)
    return columns 