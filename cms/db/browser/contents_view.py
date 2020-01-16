#-*- coding: UTF-8 -*-
from plone import api
import datetime
from zope.event import notify
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import Interface
from Products.Five.browser import BrowserView 
from zope.component import getMultiAdapter
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.resources import add_resource_on_request
from Products.CMFPlone.resources import add_bundle_on_request
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize
from zope.interface import Interface
# from plone.directives import dexterity
from plone.memoize.instance import memoize
from cms.db.browser.utility import gonglinian2ganzhi
from cms.db.browser.utility import getDanWeiId
from cms.db.interfaces import IDbapi
from cms.db.contents.yaofolder import IYaofolder
from cms.db.contents.ormfolder import IOrmfolder
from cms.db.contents.yao import IYao
from cms.db.orm import ChuFang
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao_JingLuo_Asso
from cms.db.orm import Yao,Yao_ChuFang_Asso,ChuFang
from cms.db.orm import Yao_DanWei_Asso
from cms.db.orm import ChuFang_BingRen_Asso, BingRen
from cms.db import  Session
from cms.db.dbutility import map_yao_chufang_table
from cms.db.dbutility import ex_map_yao_chufang_total
from cms.db.dbutility import ex_map_yao_chufang_danwei
from cms.db.dbutility import map_chufang_bingren_table 

from cms.theme.interfaces import IThemeSpecific

from cms.db import _


class BaseView(BrowserView):
    "base view"  
    
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
#         add_resource_on_request(self.request, 'bootstrap-tabs')
        add_bundle_on_request(self.request, 'contents-view')    
    
    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context)
       
    def getobj_url(self,type):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type=type)
        if bool(brains):
            return brains[0].getURL()
        else:
            return ''
    
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')

        title = translation_service.translate(
                                                  value,
                                                  domain='plone',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default='')
        return title
    
    @memoize
    def getags(self):
        "get context's subject and output"
        context = self.context
        base = context.aq_parent.absolute_url()
        sts = context.subject
        items = ['<li class="first"><span class="glyphicon glyphicon-tags" aria-hidden="true"></span></li>']
        for j in sts:
            item = """<li>
            <a class="btn btn-default" href='%s/@@sysajax_listings?subject=%s'>%s</a></li>""" % (base,j,j)
            items.append(item)
        if len(items) > 1:
            return "".join(items)
        else:
            return ""
    
#     def danwei_id(self):
#         ""
#         return        
         
    
class YaoView(BaseView):
    "content type:yao view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    
    @memoize
    def get_chufang(self,yaoid):
        "search this some chufangs that contained the yao,"
        "return chufangs list"
        
        yaoid = long(yaoid)
        chufangs = Session.query(ChuFang).filter(ChuFang.yaoes.any(id = yaoid)).all()
        rt =[]

        if bool(chufangs):
            base = self.getobj_url("cms.db.chufangfolder")
            for j in chufangs:
                url = "%s/%s" % (base,str(j.id))
                item = "<li><a href=%s>%s</a></li>" % (url,j.mingcheng)
                rt.append(item)
            return ''.join(rt) 
        
        return "<li>None</li>"    
    
    @memoize
    def get_yaowei(self,yaoid):
        "search this some chufangs that contained the yao,"
        "return chufangs list"
        
        yaoid = long(yaoid)
        locator = queryUtility(IDbapi, name='yao')
        wei =locator.pk_obj_property(yaoid,'yaowei','wei')
        return wei
    
    @memoize
    def get_yaoxing(self,yaoid):
        "search this some chufangs that contained the yao,"
        "return chufangs list"
        
        yaoid = long(yaoid)
        locator = queryUtility(IDbapi, name='yao')   
        xing =locator.pk_obj_property(yaoid,'yaoxing','xing')        
        return xing
    
    @memoize    
    def get_guijing(self,yaoid):
        
        yaoid = long(yaoid)
        locator = queryUtility(IDbapi, name='yao')        
        out = locator.pk_ass_title(yaoid,Yao,Yao_JingLuo_Asso,JingLuo,'jingluo_id','mingcheng')
        return out


class BingRenView(BaseView):
    "content type:yao view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    @memoize
    def relative_chufang(self,id):
        ""
        cnlist = self.get_chufang(id)
        if cnlist[0]:
            rt =[]        
            base = self.getobj_url("cms.db.chufangfolder")
            for j in cnlist[1]:
                url = "%s/%s/@@base_view" % (base,str(j.id))
                item = "<li><a href=%s>%s</a></li>" % (url,j.mingcheng)
                rt.append(item)
            return ''.join(rt)             
        return False    
    
    def get_chufang(self,id):
        "get all chufang by bingren id"
        id = long(id)
        chufangs = Session.query(ChuFang).filter(ChuFang.bingrens.any(id = id)).all()
        if bool(chufangs):
            return (True,chufangs)
        else:
            return (False,[])
       

class ChuFangView(BaseView):
    "content type:chufang view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize
    def asso_recorders(self,id):
        ""
        
        _id = long(id)
        id = getDanWeiId()
        locator = queryUtility(IDbapi, name='chufang')
        #pk,factorycls,asso,asso_p1,asso_p2,midcls,midp,asso2,asso2_p1,asso2_p2,p2,fk,comp,mapf        
        recorders = locator.ex_pk_ass_obj_title(_id,ChuFang,Yao_ChuFang_Asso,'yaoliang','paozhi',
                                          Yao,'mingcheng',Yao_DanWei_Asso,'danjia','kucun',
                                          'danwei_id',id,'yao_id')

        chufang = locator.getByCode(_id)
        return (recorders,chufang)        
        
    
    def chufang_structure(self,id):
        ""
        #pk,factorycls,asso,asso_p1,asso_p2,midcls,midp,asso2,asso2_p1,asso2_p2,p2,fk,comp,mapf        
        rt = self.asso_recorders(id)
        recorders = rt[0]        
        more = map(ex_map_yao_chufang_danwei,recorders)       
        jiliang = rt[1].jiliang
        zhenjin = rt[1].zhenjin
        subtotal = map(ex_map_yao_chufang_total,recorders)
        subtotal = sum(map(float,subtotal))
        out2 = """<td colspan="2" class="text-right">%s</td><td class="text-left">%s</td>""" \
         % (u"小计".encode('utf-8'),subtotal)         
        out3 = """<td colspan="2" class="text-right">%s</td><td class="text-left">%s</td>""" \
         % (u"剂量".encode('utf-8'),jiliang)
        out4 = """<td colspan="2" class="text-right">%s</td><td class="text-left">%s</td>""" \
         % (u"诊金".encode('utf-8'),zhenjin)
        total = """<td colspan="2" class="text-right">%s</td><td class="text-left">%s</td>""" \
         % (u"合计".encode('utf-8'),subtotal * jiliang + zhenjin)
        more.append(out2)
        more.append(out3)
        more.append(out4)
        more.append(total)
        out = ";".join(more)
        out = out.replace(";","</tr><tr>")
        out = "<tr>%s</tr>" % out       
        return out        
    
    def bingrens_table(self,id):
        "output bingren list"
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='chufang')        
        out = locator.pk_ass_obj_title(_id,ChuFang,ChuFang_BingRen_Asso,
                                       BingRen,'bingren_id','xingming',map_chufang_bingren_table)

        out = out.replace(";","</tr><tr>")
        out = "<tr>%s</tr>" % out       
        return out            

       
class YaoXingView(BaseView):
    "content type:yaoxing view"
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    def relative_yaoes(self,id):
        "fetch all yaoes that have same yaoxing"
        
        if "yaoxing" in id:
            id = id.split('yaoxing')[1]
        yaoes = self.yaoes_generator(id)
        base = self.getobj_url("cms.db.yaofolder")
        items = []
        for j in yaoes:
            item = """<tr><td><a href='%s/%s/@@base_view'>%s</a></td><td>%s</td></tr>
            """ %(base,j.id,j.mingcheng,j.yaowei.wei)
            items.append(item)
        return ''.join(items)        
    
    def yaoes_generator(self,id):
        _id = long(id)
        locator = queryUtility(IDbapi, name='yaoxing')
        rder = locator.getByCode(_id)
        for j in rder.yaoes:
            if bool(j.mingcheng):
                yield j
            else:
                continue               


class YaoWeiView(YaoXingView):
    "content type:yaowei view"

    def relative_yaoes(self,id):
        "fetch all yaoes that have same yaowei"
        
        if "yaowei" in id:
            id = id.split('yaowei')[1]
        yaoes = self.yaoes_generator(id)
        base = self.getobj_url("cms.db.yaofolder")
        items = []
        for j in yaoes:
            item = """<tr><td><a href='%s/%s/@@base_view'>%s</a></td><td>%s</td></tr>
            """ %(base,j.id,j.mingcheng,j.yaoxing.xing)
            items.append(item)
        return ''.join(items)        
    
    def yaoes_generator(self,id):
        _id = long(id)
        locator = queryUtility(IDbapi, name='yaowei')
        rder = locator.getByCode(_id)
        for j in rder.yaoes:
            if bool(j.mingcheng):
                yield j
            else:
                continue
        
        
class JingLuoView(BaseView):
    "content type:jingluo view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True) 
        

class YiShengView(BaseView):
    "content type:jingluo view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        

class DanWeiView(BaseView):
    "content type:danwei view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

class WuYunView(BaseView):
    "content type:wuyun view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    def preyear(self,id):
        ""
        id = int(id) - 1
        if id==0:id=60
        parent = self.getobj_url("cms.db.wuyunfolder")
        return "%s/%s/@@base_view" % (parent,str(id))

    def nextyear(self,id):
        ""
        id = int(id) + 1
        if id==65:id=1
        parent = self.getobj_url("cms.db.wuyunfolder")
        return "%s/%s/@@base_view" % (parent,str(id))
        
    def currentyear(self):
        "get current year wuyuliuqi"
        
        parent = self.getobj_url("cms.db.wuyunfolder")
        jinnian = int(datetime.datetime.today().strftime("%Y"))
        wuyunid = gonglinian2ganzhi(jinnian)
        return "%s/%s/@@base_view" % (parent,wuyunid)                     
        
    def closed30nianfen(self,id):
        "由干支序号id,取最近30年同干支年份"
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='nianganzhi')                
        ganzhi = locator.getByCode(_id).ganzhi        
        nlist = []
#         nlist.append(u"%s:" % ganzhi)
        wuyun = u"年五运六气".encode('utf-8')
        for j in self.ganzhi_generator(_id):
            nlist.append("%s%s" % (j,wuyun))
        return "%s:%s" %(ganzhi, ",".join(nlist))           
        
    def ganzhi_generator(self,id):

        jinnian = int(datetime.datetime.today().strftime("%Y"))
        for j in xrange(jinnian-60,jinnian+61):
            if gonglinian2ganzhi(j)==id:
                yield j
            else:
                continue      
    
    def get_dayun(self,id):
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='nianganzhi')                
        out = locator.getByCode(_id)
        out = out.dayun      
        return out        
    
    def get_sitian(self,id):
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='nianganzhi')                
        out = locator.getByCode(_id)
        out = out.sitian      
        return out 
    
    def get_zaiquan(self,id):
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='nianganzhi')                
        out = locator.getByCode(_id)
        out = out.zaiquan      
        return out
    
    def get_zhuqi_keqi(self,id):
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='nianganzhi')                
        rder = locator.getByCode(_id)
        zhuqi = rder.zhuqi.split(",")
        keqi = rder.keqi.split(",")
        jialin = rder.jialin.split(",")
        out = []
        dayun = """<tr>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        <th>%s</th>
        </tr>
        """ % ("&nbsp;",
               u"初之气",
               u"二之气",
               u"三之气",
               u"四之气",
               u"五之气", 
               u"终之气"                                                                           
               )
        liuqijiaosi = """<tr>
        <th>%s</th>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        """ % (u"交司时段",
               u"大寒-惊蛰",
               u"春分-立夏",
               u"小满-小暑",
               u"大暑-白露",
               u"秋分-立冬", 
               u"小雪-小寒"                                                                           
               )        
        out.append(dayun)
        tr = self.strlist2tr(zhuqi,u"主气")
        out.append(tr)
        tr = self.strlist2tr(keqi,u"客气")
        out.append(tr)
        tr = self.strlist2tr(jialin,u"加临")
        out.append(tr)
        out.append(liuqijiaosi)                
        return ''.join(out)
        
    def get_zhuyun_keyun(self,id):
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='nianganzhi')                
        rder = locator.getByCode(_id)
        zhuyun = rder.zhuyun.split(",")
        keyun = rder.keyun.split(",")
        jiaosi = rder.jiaosi.split(",")
        out = []
        dayun = """<tr><th>%s</th><th class="text-center" colspan="5">%s</th></tr>
        """ % (u"大运".encode('utf-8'),self.get_dayun(_id))
        out.append(dayun) 
        tr = self.strlist2tr(zhuyun,u"主运")
        out.append(tr)
        tr = self.strlist2tr(keyun,u"客运")
        out.append(tr)
        tr = self.strlist2tr(jiaosi,u"交司")
        out.append(tr)                                
        return ''.join(out)
    
    def strlist2tr(self,strlist,title):
        "将一个list 数据转换 html的 tr"
        
        from Products.CMFPlone.utils import safe_unicode
        title = safe_unicode(title)
        prefix = u"<tr><th>%s</th>" % title
        postfix = u"</tr>"
        lt = []
        lt.append(prefix)
        for i in strlist:
            item = "<td>%s</td>" % i
            lt.append(item)
        lt.append(postfix)
        return ''.join(lt)           
        
        
        
                                                             

