#-*- coding: UTF-8 -*-
from zope.publisher.browser import BrowserView
from zope.interface import implements
from zope.contentprovider.interfaces import IContentProvider


class BaseExtendedHelp(BrowserView):
    """
    z3c form content provider for tipping
    """
    
    implements(IContentProvider)
    def __init__(self, context, request, view):
        super(BaseExtendedHelp, self).__init__(context, request)
        self.__parent__ = view
 
    def update(self):
        self.url = self.context.absolute_url()
 
    def render(self):
        return ""
        
        

class BingRenExtendedHelp(BaseExtendedHelp):      
    """
    z3c form content provider for tipping to adding personal address before
    add bingren base infomation
    """ 
    def update(self):
        self.url = self.context.absolute_url()
        self.add_gerendizhi_url = "%s/@@input_gerendizhi" % self.url
 
    def render(self):
        return """<div class="ex-help text-warning">在添加病人基本信息前,请通过点击如下链接
        <a class="btn btn-default" href="%s" role="button" target="_blank">添加地址</a>
        先添加病人地址信息</div>""" % self.add_gerendizhi_url
        

class DanWeiExtendedHelp(BaseExtendedHelp):      
    """
    z3c form content provider for tipping to adding personal address before
    add bingren base infomation
    """ 
    def update(self):
        self.url = self.context.absolute_url()
        self.add_danweidizhi_url = "%s/@@input_danweidizhi" % self.url
 
    def render(self):
        return """<div class="ex-help text-warning">在添加单位基本信息前,请通过点击如下链接
        <a class="btn btn-default" href="%s" role="button" target="_blank">添加地址</a>
        先添加该单位的地址信息</div>""" % self.add_danweidizhi_url


class YiShengExtendedHelp(BaseExtendedHelp):      
    """
    z3c form content provider for tipping to adding personal address before
    add bingren base infomation
    """ 
    def update(self):
        self.url = self.context.absolute_url()
        self.add_danwei_url = "%s/@@input_danwei" % self.url
 
    def render(self):
        return """<div class="ex-help text-warning">在添加医生基本信息前,请通过点击如下链接
        <a class="btn btn-default" href="%s" role="button" target="_blank">添加单位</a>
        先添加该医生所在的单位信息</div>""" % self.add_danwei_url
