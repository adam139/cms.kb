#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.site.hooks import getSite
from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from cms.policy import fmt
from cms.db.browser.utility import get_container_by_type
from cms.db.browser.utility import chown
from cms.db.browser.utility import UnrestrictedUser
from plone import api
import datetime

def recorder_created_handler(event):
    """relative db has been created a recorder,
    This handler operate the event"""
                   
    id = str(event.id)
    cls = event.cls
    title = safe_unicode(event.ttl)
    import pdb
    pdb.set_trace()
    #find parent container through cls
    container = get_container_by_type(cls)
    if bool(container):
        # check id if is existed
        try:
            wk = container[id]
        except:
            wk = None
        if bool(wk):
            raise("the object has been existed")
            return       
    #call create object function        
        # bypass permission check
        old_sm = getSecurityManager()
        portal = api.portal.get()
        tmp_user = UnrestrictedUser(old_sm.getUser().getId(),'', ['Manager'],'')        
        tmp_user = tmp_user.__of__(portal.acl_users)
        newSecurityManager(None, tmp_user)        
        item = api.content.create(type=cls,id=id,title=title,container=container)
#         chown(item,userid)
        # recover old sm
        setSecurityManager(old_sm)
        return
                

      


   

def check_size(dbapi,percentage,max,userid,url):
    "check table size and send warning message"
    
    # check log size
    recorders = dbapi.get_rownumber()
    tmp = int(max * percentage)
    if recorders >= tmp and recorders <= tmp + 1:
#         userid = 'test17'
#         url = ''
        send_warning(percentage,userid,url)        
    

def AdminLogoutEventHandler(event):
    """the system administrators logout event handler"""

    from emc.kb.interfaces import IAdminLogLocator
    dbapi,timeout,bsize,percentage,max = fetch_log_parameter('adminlog')  
    # check log size and send warning
    userid = '777777888888999999'
    url = "%s/@@admin_logs" % api.portal.get().absolute_url()      
    check_size(dbapi,percentage,max,userid,url)      
    # truncate log      
    task = CheckLog(8,dbapi,timeout,bsize,max,percentage)
    task.start()
    
    values = {'adminid':event.adminid,'userid':' ','datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':5,'result':1,'description':u''}                
    if not bool(event.description):
        values['description'] = u"%s登出了EMC系统" % (event.adminid)
    else:
        values['description'] = u"%s%s" % (event.adminid,event.description)
        values['operlevel'] = 4         
    locator = getUtility(IAdminLogLocator)
    locator.add(values)

