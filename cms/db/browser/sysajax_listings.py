#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFCore.interfaces import ISiteRoot
# from plone.directives import dexterity
from plone.memoize.instance import memoize

from Products.Five.browser import BrowserView
# from collective.gtags.interfaces import ITagSettings


class SysAjaxListingView(BrowserView):
    """
    system AJAX 查询，返回分页结果,for some contenttypes relative to project
    """                 
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
    
    
    def splitTag(self,value):
            """Split a tag into (category, tag) parts. category may be None.
            input: value like abc-a1 or a1
            output:dict like  {'category':abc,'value':a1}
            """
            parts = value.split("-")
            output = {'category':'','value':''}        
    
            if len(parts) == 1:
                output['value'] = value
                return output
            else:
                output['category'] = parts[0]
                output['value'] = parts[1]
                return output
            
    @memoize
    def getTagregistryProxy(self):
        "input keywords vocabulary,\
        output all tags,compose a list,member of the list is unicode"
        factory = queryUtility(IVocabularyFactory, 'plone.app.vocabularies.Keywords')
#         import pdb
#         pdb.set_trace()
        if not factory:
            raise VocabLookupException(
                'No factory with name "%s" exists.' % factory_name)

        vocabulary = factory(self.context)
        tags = [ term.title for term in vocabulary]
#         settings = getUtility(IRegistry).forInterface(ITagSettings)
        return tags
    
    @memoize
    def getTagGroups(self):
        "fetch all tag groups ,it is category part of 'category-value'" 
        tagsets = self.getTagregistryProxy()
        if tagsets ==None:return None
#         import pdb
#         pdb.set_trace()
        # get rid of duplicate
        groups = set(self.splitTag(value)['category'] for value in tagsets if value != "")
        groups = list(groups)
        groups.sort(reverse=True)
        return groups           
    
    def getAllTags(self,category,start=0,size=None):
        """fetch all predefine  tags under the specify category"""
        tagsets = self.getTagregistryProxy()
#         import pdb
#         pdb.set_trace()
#         out = []
        if tagsets ==None:return None
        def cfilter(tag):
            loopc = self.splitTag(tag)
            return loopc['category'] == category and loopc['value'] != ""
        
        def mapf(tag):
            loopc = self.splitTag(tag)
            return loopc['value']        
#         import pdb
#         pdb.set_trace()
        out = filter(cfilter,tagsets)
        out = map(mapf,out)
        out.sort()
        lth = len(out)        
        if size == None:
            if start == 0:
                tags = out
            else:                                
                tags = out[start:]
        else:
            size = min(size,lth)
            tags = out[start:size]            
        #set output dic
        o = dict()
        # this is total
        o['t'] = lth
        # this is output html
        o['h'] = tags                      
        return  o            

    def getTagHtml(self,category,start=0,size=None):
        """
                        <span data-name="1"><a href="javascript:void(0)">分析</a></span>
                        <span data-name="2"><a href="javascript:void(0)">设计</a></span>

        """
        o = self.getAllTags(category,start,size)
        tags = o['h']
        max = o['t']
        if tags == None: return "no any tag"
        out = ""
        if start == 0:       
            i = 1
        else:
            i = start + 1              
        for tag in tags:
            num = str(i)                       
            out2 = """<span data-name="%s">\
            <a class="btn btn-default" href="javascript:void(0)" role="button">%s</a>\
            </span>""" % (num,tag)
            out = "%s%s" %(out,out2)
            i = i + 1
        if size != None and max > size:
            txt = u"更多".encode('utf-8')
            more = """<span class="%s" data-name="%s" data-group="%s" data-start="%s">\
            <a class="btn btn-default" href="javascript:void(0)" role="button">%s</a>\
            </span>""" % ('more',str(i),category,str(size),txt)             
            out = "%s%s" % (out,more) 
        return out    
    
    @memoize
    def getAllTagsHtml(self):
        "output all tag groups html"
        groups = self.getTagGroups()
#         i= 0
        out = ""
        prefix = """
                    <ul class="row tagSelectSearch list-inline">                    
                    <li class="title">按%s：</li>
                    <li class="hidden">
                        <input type="hidden" value="0" class="taggroup" data-category="%s-">                            
                    </li>                    
                    <li class="all">
                        <span class="over" data-name="0"><a class="btn btn-default" href="javascript:void(0)" role="button">所有</a></span><!-- 所有 -->
                    </li>
                    <li class="tag_list_div fenlei_a">
        """
        postfix = "</li></ul>"
        for group in groups:
            if group != "":                
                prefixing = prefix % (group,group)
            else:
                fixgroup = u"未分类".encode('utf-8')
                fixprefix = """
                    <ul class="row tagSelectSearch list-inline" id="no-category">                    
                    <li class="title">%s：</li>
                    <li class="hidden">
                        <input type="hidden" value="0" class="taggroup" data-category="%s-">                            
                    </li>                    
                    <li class="all">
                        <span class="over" data-name="0"><a class="btn btn-default" href="javascript:void(0)" role="button">所有</a></span><!-- 所有 -->
                    </li>
                    <li class="tag_list_div fenlei_a">
        """
                prefixing = fixprefix % (fixgroup,fixgroup)
            loopitem = self.getTagHtml(group,0,5)

            loopitem = "%s%s%s" % (prefixing,loopitem,postfix)
            out = "%s%s" % (out,loopitem)
        return out                                         
         
    def canbeRead(self):
        return True
#        status = self.workflow_state()
# checkPermission function must be use Title style permission
#         canbe = self.pm().checkPermission(viewReport,self.context)
#         return canbe is not None

    def hasSummaryView(self):
        try:
            sview = getMultiAdapter((self.context, self.request),name=u"summary_view")
        except:
            sview = None
        return  sview is not None
    
    def hasListingView(self):
        try:
            sview = getMultiAdapter((self.context, self.request),name=u"listing_view")
        except:
            sview = None
        return  sview is not None       
        
    def getPathQuery(self,objid=None,justchildrens=True):
 
        """返回 all organizations  catalog(path={'query': folder_path, 'depth': 1})

        """
        query = {}      
        path = "/".join(self.context.getPhysicalPath())
        if justchildrens:
            pathdic = {'depth':1}
            pathdic['query'] = path
            query['path'] = pathdic            
        elif bool(objid):
            query2 = {}
            query2['id'] = objid
            bn = self.catalog()(query2)
            if len(bn) >=1:
                path = bn[0].getPath()
                query['path'] = path
            else:
                query['path'] = path                                             
        else:
            query['path'] = path                             
        return query
#任务类型属性：分析/设计/实验/仿真/培训          
    def getTaskType(self,typekey):
        if typekey == 1:
            return "analysis"
        elif typekey == 2:
            return "design"
        elif typekey == 3:
            return "experiment"
        elif typekey == 4:
            return "simulation"                
        else:
            return "train"
         
#密级属性：公开/内部/机密 
    def getSecurityLevel(self,key):
        if key == 1:
            return "public"
        elif key == 2:
            return "inner"
        else:
            return "secret"
         
    def search_multicondition(self,query):  
        return self.catalog()(query)


class YaoAjaxListingView(SysAjaxListingView):
    """ ajax listing view for yao content types"""
    
    def search_multicondition(self,query):
        query['portal_type'] = "cms.db.yao"  
        return self.catalog()(query)
        
    
class JingLuoAjaxListingView(SysAjaxListingView):
    """ ajax listing view for yao content types"""
    
    def search_multicondition(self,query):
        query['portal_type'] = "cms.db.jingluo"  
        return self.catalog()(query)
    
    
class YaoWeiAjaxListingView(SysAjaxListingView):
    """ ajax listing view for yao content types"""
    
    def search_multicondition(self,query):
        query['portal_type'] = "cms.db.yaowei"  
        return self.catalog()(query)
    
    
class YaoXingAjaxListingView(SysAjaxListingView):
    """ ajax listing view for yao content types"""
    
    def search_multicondition(self,query):
        query['portal_type'] = "cms.db.yaoxing"  
        return self.catalog()(query)
            
       
class sysloadMore(BrowserView):
    """AJAX action for loardmore.
    """    
   
    def queryview(self):
        searchview = getMultiAdapter((self.context, self.request),name=u"sysajax_listings")
        return searchview
        
    def __call__(self):
        searchview = self.queryview()                   
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        group = datadic['category']  # 对应 tag category
#         import pdb
#         pdb.set_trace()
        out = searchview.getTagHtml(group,start,None)
#         getTagHtml(self,category,start=0,size=None)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(out)   


 # ajax multi-condition search       
class Ajaxsearch(BrowserView):
    """AJAX action for search.
    """    

    def Datecondition(self,key):        
        "构造日期搜索条件"
        end = datetime.datetime.today()
#最近一周        
        if key == 1:  
            start = end - datetime.timedelta(7) 
#最近一月             
        elif key == 2:
            start = end - datetime.timedelta(30) 
#最近一年            
        elif key == 3:
            start = end - datetime.timedelta(365) 
#最近两年                                                  
        elif key == 4:
            start = end - datetime.timedelta(365*2) 
#最近五年               
        else:
            start = end - datetime.timedelta(365*5) 
#            return    { "query": [start,],"range": "min" }                                                             
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition  
          
    def filter_category(self,value):
        if "-" not in value:return value
        return value.split('-')[1]    
    
    def __call__(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"sysajax_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()
        objid =  (datadic['objid']).strip()
        if objid == "":   
            origquery = searchview.getPathQuery()
        else:
            origquery = searchview.getPathQuery(objid = objid)

        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'       
#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)         
        # remove repeat values 
        tag = tag.split(',')
        tag = set(tag)
        tag = list(tag)
        all = u"所有".encode("utf-8")
        unclass = u"未分类".encode("utf-8")        
# filter contain "u'所有'"
        tag = filter(lambda x: all not in x, tag)
# recover un-category tag (remove:u"未分类-")
        def recovery(value):
            if unclass not in value:return value
            return value.split('-')[1]
            
        tag = map(recovery,tag)        
        if '0' in tag and len(tag) > 1:
            tag.remove('0')
            rule = {"query":tag,"operator":"and"}
            origquery['Subject'] = rule                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)       
       
    def output(self,start,size,totalnum,braindata):
        "根据参数total,braindata,返回jason 输出"
        outhtml = ""      
        k = 0
        for i in braindata:          
            out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-3 text-left"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="col-md-7">%(description)s</td>
                                <td class="col-md-1 text-center">%(date)s</td>                                
                            </tr> """% dict(objurl="%s/@@base_view" % i.getURL(),
                                            num=str(k + 1),
                                            title=i.Title,
                                            description= i.Description,
                                            date = i.created.strftime('%Y-%m-%d'))           
            outhtml = "%s%s" %(outhtml ,out)
            k = k + 1           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data      

class YaoAjaxsearch(Ajaxsearch):
    """AJAX action for search.
    """    
    def __call__(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"yaoajax_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()
        objid =  (datadic['objid']).strip()
        if objid == "":   
            origquery = searchview.getPathQuery()
        else:
            origquery = searchview.getPathQuery(objid = objid)

        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'       
#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)         
        # remove repeat values 
        tag = tag.split(',')
        tag = set(tag)
        tag = list(tag)
        all = u"所有".encode("utf-8")
        unclass = u"未分类".encode("utf-8")        
# filter contain "u'所有'"
        tag = filter(lambda x: all not in x, tag)
# recover un-category tag (remove:u"未分类-")
        def recovery(value):
            if unclass not in value:return value
            return value.split('-')[1]
            
        tag = map(recovery,tag)        
        if '0' in tag and len(tag) > 1:
            tag.remove('0')
            rule = {"query":tag,"operator":"and"}
            origquery['Subject'] = rule                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)

        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
    
    
class JingLuoAjaxsearch(Ajaxsearch):
    """AJAX action for search.
    """    
    def __call__(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"jingluoajax_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()
        objid =  (datadic['objid']).strip()
        if objid == "":   
            origquery = searchview.getPathQuery()
        else:
            origquery = searchview.getPathQuery(objid = objid)

        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'       
#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)         
        # remove repeat values 
        tag = tag.split(',')
        tag = set(tag)
        tag = list(tag)
        all = u"所有".encode("utf-8")
        unclass = u"未分类".encode("utf-8")        
# filter contain "u'所有'"
        tag = filter(lambda x: all not in x, tag)
# recover un-category tag (remove:u"未分类-")
        def recovery(value):
            if unclass not in value:return value
            return value.split('-')[1]
            
        tag = map(recovery,tag)        
        if '0' in tag and len(tag) > 1:
            tag.remove('0')
            rule = {"query":tag,"operator":"and"}
            origquery['Subject'] = rule                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)

        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)

class YaoWeiAjaxsearch(Ajaxsearch):
    """AJAX action for search.
    """    
    def __call__(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"yaoweiajax_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()
        objid =  (datadic['objid']).strip()
        if objid == "":   
            origquery = searchview.getPathQuery()
        else:
            origquery = searchview.getPathQuery(objid = objid)

        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'       
#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)         
        # remove repeat values 
        tag = tag.split(',')
        tag = set(tag)
        tag = list(tag)
        all = u"所有".encode("utf-8")
        unclass = u"未分类".encode("utf-8")        
# filter contain "u'所有'"
        tag = filter(lambda x: all not in x, tag)
# recover un-category tag (remove:u"未分类-")
        def recovery(value):
            if unclass not in value:return value
            return value.split('-')[1]
            
        tag = map(recovery,tag)        
        if '0' in tag and len(tag) > 1:
            tag.remove('0')
            rule = {"query":tag,"operator":"and"}
            origquery['Subject'] = rule                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)

        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)


class YaoXingAjaxsearch(Ajaxsearch):
    """AJAX action for search.
    """    
    def __call__(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"yaoxingajax_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()
        objid =  (datadic['objid']).strip()
        if objid == "":   
            origquery = searchview.getPathQuery()
        else:
            origquery = searchview.getPathQuery(objid = objid)

        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'       
#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)         
        # remove repeat values 
        tag = tag.split(',')
        tag = set(tag)
        tag = list(tag)
        all = u"所有".encode("utf-8")
        unclass = u"未分类".encode("utf-8")        
# filter contain "u'所有'"
        tag = filter(lambda x: all not in x, tag)
# recover un-category tag (remove:u"未分类-")
        def recovery(value):
            if unclass not in value:return value
            return value.split('-')[1]
            
        tag = map(recovery,tag)        
        if '0' in tag and len(tag) > 1:
            tag.remove('0')
            rule = {"query":tag,"operator":"and"}
            origquery['Subject'] = rule                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)

        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)            