#-*- coding: UTF-8 -*-
import unittest
import transaction
from datetime import date
from datetime import datetime
from plone.testing.z2 import Browser
from zope import event

from cms.db.testing import FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles,login,logout

from cms.db.contents.folder import Ifolder
from cms.db.contents.ormfolder import Iormfolder

from sqlalchemy import and_

from cms.db import  Session
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao
from cms.db.orm import ChuFang,BingRen,DiZhi,DanWei,YiSheng
from cms.db.orm import Yao_ChuFang_Asso,ChuFang_BingRen_Asso


class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):

        yaowei1 = YaoWei("酸")
        yaowei2 = YaoWei("苦")
        yaowei3 = YaoWei("甘")
        yaowei4 = YaoWei("辛")
        yaowei5 = YaoWei("咸")
        Session.add_all([yaowei1,yaowei2,yaowei3,yaowei4,yaowei5])
        yaoxing1 = YaoXing("大热")
        yaoxing2 = YaoXing("热")
        yaoxing3 = YaoXing("温")
        yaoxing4 = YaoXing("凉")
        yaoxing5 = YaoXing("寒")
        yaoxing6 = YaoXing("大寒")
        Session.add_all([yaoxing1,yaoxing2,yaoxing3,yaoxing4,yaoxing5,yaoxing6])
        jingluo1 = JingLuo("足太阳膀胱经")
        jingluo2 = JingLuo("足阳明胃经")
        jingluo3 = JingLuo("足少阳胆经")
        jingluo4 = JingLuo("足厥阴肝经")
        jingluo5 = JingLuo("足少阴肾经")
        jingluo6 = JingLuo("足太阴脾经")
        Session.add_all([jingluo1,jingluo2,jingluo3,jingluo4,jingluo5,jingluo6])
        yao1 = Yao("白芍")
        yao1.yaowei = yaowei1
        yao1.yaoxing = yaoxing1
        yao1.guijing = [jingluo1]         
        yao2 = Yao("大枣")
        yao2.yaowei = yaowei2
        yao2.yaoxing = yaoxing2
        yao2.guijing = [jingluo2]
        Session.add_all([yao1,yao2])        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
        bingren.dizhi = dizhi
        dizhi2 = DiZhi("中国","湖北","十堰市","茅箭区施洋路83号")
        danwei = DanWei("任之堂")
        yisheng = YiSheng('余浩',1, date(2015, 4, 2),'13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi2
        chufang = ChuFang("桂枝汤","加热稀粥",5)
        yao_chufang = Yao_ChuFang_Asso(yao1,chufang,7,"晒干")
        yao_chufang2 = Yao_ChuFang_Asso(yao2,chufang,10,"掰开")
        chufang_bingren = ChuFang_BingRen_Asso(bingren,chufang,datetime.now())
        yisheng.chufangs = [chufang]
        Session.add_all([dizhi,bingren,danwei,dizhi2,yisheng,chufang,yao_chufang,yao_chufang2,chufang_bingren])                         
        Session.commit()        
        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ('Manager',))


        portal.invokeFactory('cms.db.folder', 'folder')
        portal['folder'].invokeFactory('cms.db.ormfolder', 'ormfolder')       
        self.portal = portal

    def tearDown(self):
        
        items = Session.query(YaoWei).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(JingLuo).all())
        items.extend(Session.query(Yao).all())
        items.extend(Session.query(ChuFang).all())
        items.extend(Session.query(BingRen).all())
        items.extend(Session.query(YiSheng).all())
        items.extend(Session.query(DanWei).all())
        items.extend(Session.query(DiZhi).all())                
        for item in items:
            Session.delete(item)            
        Session.commit()
                
        
    def testfolderView(self):

        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        transaction.commit()

        browser.open(portal['folder'].absolute_url())
        
        self.assertTrue('class="pat-structure"' in browser.contents)

   
    def testormfolderView(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))

        transaction.commit()
        browser.open(portal['folder']['ormfolder'].absolute_url())
        
        self.assertTrue('class="pat-structure"' in browser.contents)
    
    def testYaoXingView(self):
        # add data to yaoxing table

        suan = Session.query(YaoXing).filter(YaoXing.xing=="温").all()
        self.assertEqual(len(suan),1)
        
        
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))

        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()

        browser.open(base + "/@@yaoxing_listings")
        
        self.assertTrue(u"温" in browser.contents)
        
    def testYaoWeiView(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open(base + "/@@yaowei_listings")
        self.assertTrue(u"甘" in browser.contents)
        suan = Session.query(YaoWei).filter(YaoWei.wei=="甘").all()
        self.assertEqual(len(suan),1)

    def testInputYaoXingForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_yaoxing" % base)        
        # Fill in the form 
#         browser.getControl(name=u"form.widgets.id").value = 1
        browser.getControl(name=u"form.widgets.xing").value = u"微寒"        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(YaoXing).filter(YaoXing.xing==u"微寒").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)        
#         self.assertTrue("row table table-striped table-bordered table-condensed listing" in browser.contents)

    def testInputYaoWeiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_yaowei" % base)        
        # Fill in the form 
#         browser.getControl(name=u"form.widgets.id").value = 1
        browser.getControl(name=u"form.widgets.wei").value = u"淡"        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(YaoWei).filter(YaoWei.wei==u"淡").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)   

    def testInputJingLuoForm(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_jingluo" % base)        
        # Fill in the form 
#         browser.getControl(name=u"form.widgets.id").value = 1
        browser.getControl(name=u"form.widgets.mingcheng").value = u"手太阳小肠经"        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(JingLuo).filter(JingLuo.mingcheng==u"手太阳小肠经").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testDeleteYaoWeiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        id = Session.query(YaoWei).filter(YaoWei.wei==u"甘").one().id
        # Open form
        browser.open("%s/@@delete_yaowei/%s" % (base,id))        
        # Fill in the form 
#         browser.getControl(name=u"form.widgets.id").value = 1
        browser.getControl(name=u"form.widgets.wei").value = u"甘"        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(YaoWei).filter(YaoWei.wei==u"甘").all()
        self.assertEqual(len(suan),0)
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

        
    def testInputYaoForm(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_yao" % base)
        yaowei_id = Session.query(YaoWei).filter(YaoWei.wei=="甘").first().id
        yaoxing_id = Session.query(YaoXing).filter(YaoXing.xing=="凉").first().id
        jingluo_id = Session.query(JingLuo).filter(JingLuo.mingcheng=="足少阳胆经").first().id
        jingluo_id2 = Session.query(JingLuo).filter(JingLuo.mingcheng=="足厥阴肝经").first().id
       
        # Fill in the form 
        browser.getControl(name=u"form.widgets.yaowei_id").value = str(yaowei_id)
        browser.getControl(name=u"form.widgets.yaoxing_id").value = str(yaoxing_id)
        browser.getControl(name=u"form.widgets.mingcheng").value = u"牛膝"
         
#         browser.getControl(name=u"form.widgets.guijing.to").value = [jingluo_id,jingluo_id2] 
        browser.getControl(name=u"form.widgets.zhuzhi").value = u"引气血下行"        
        # Submit
        browser.getControl(u"Submit").click()        
        suan = Session.query(Yao).filter(Yao.mingcheng==u"牛膝").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)        
 
    def testInputDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_dizhi" % base)        
        # Fill in the form 
        browser.getControl(name=u"form.widgets.guojia").value = u"中国"
        browser.getControl(name=u"form.widgets.sheng").value = u"湖南"
        browser.getControl(name=u"form.widgets.shi").value = u"长沙市"
        browser.getControl(name=u"form.widgets.jiedao").value = u"五一大道83号"                        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(DiZhi).filter(DiZhi.shi==u"长沙市").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)


    def testInputDanWeiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_danwei" % base)
        dizhi_id = Session.query(DiZhi).filter(DiZhi.shi==u"湘潭市").first().id      
        # Fill in the form        
#         browser.getControl(name=u"form.widgets.dizhi_id").value = str(dizhi_id)                
        # Fill in the form 
        browser.getControl(name=u"form.widgets.mingcheng").value = u"泽生堂"
        browser.getControl(name=u"form.widgets.dizhi:list").value =[str(dizhi_id)]                         
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(DanWei).join(DiZhi).filter(DiZhi.shi==u"湘潭市").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testInputYiShengForm(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_yisheng" % base)

        danwei_id = Session.query(DanWei).filter(DanWei.mingcheng=="任之堂").first().id      
        # Fill in the form        
        browser.getControl(name=u"form.widgets.danwei_id").value = str(danwei_id)               
        browser.getControl(name=u"form.widgets.xingming").value = "余dong"
        browser.getControl(name=u"form.widgets.xingbie:list").value = ['1']
        browser.getControl(name=u"form.widgets.shengri").value =  "2015-04-12"
        browser.getControl(name=u"form.widgets.dianhua").value = "13673265859"                        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(YiSheng).join(DanWei).filter(and_(DanWei.mingcheng=="任之堂",YiSheng.xingming=="余dong")).all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testInputBingRenForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_bingren" % base)
        dizhi_id = Session.query(DiZhi).filter(DiZhi.jiedao=="茅箭区施洋路83号").first().id      
        # Fill in the form        
        browser.getControl(name=u"form.widgets.dizhi_id").value = str(dizhi_id)               
        browser.getControl(name=u"form.widgets.xingming").value = "张dong"
        browser.getControl(name=u"form.widgets.xingbie:list").value = ['1']
        browser.getControl(name=u"form.widgets.shengri").value =  "2015-09-12"
        browser.getControl(name=u"form.widgets.dianhua").value = "13873265859"                        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(BingRen).join(DiZhi).filter(and_(DiZhi.jiedao=="茅箭区施洋路83号",BingRen.xingming=="张dong")).all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)
        
    def testInputChuFangForm(self):        
       
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_chufang" % base)

        browser.getControl(name=u"form.widgets.yaoes.buttons.add").click()
        
        yisheng_id = Session.query(YiSheng).filter(YiSheng.xingming=="余浩").first().id
        yao_id = Session.query(Yao).filter(Yao.mingcheng=="白芍").first().id      
        # Fill in the form        
#         browser.getControl(name=u"form.widgets.yisheng_id").value = str(yisheng_id)               
        browser.getControl(name=u"form.widgets.mingcheng").value = "麻黄汤"
        browser.getControl(name=u"form.widgets.yizhu").value = "热稀粥"
        browser.getControl(name=u"form.widgets.jiliang").value =  "5"
        browser.getControl(name=u"form.widgets.yisheng:list").value = [str(yisheng_id)]
        #fil subform
        browser.getControl(name=u"form.widgets.yaoes.0.widgets.yao_id:list").value = [str(yao_id)]
        browser.getControl(name=u"form.widgets.yaoes.0.widgets.yaoliang").value = '15'
        browser.getControl(name=u"form.widgets.yaoes.0.widgets.paozhi").value = 'pao zhi'
                                
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(ChuFang).join(YiSheng).filter(and_(YiSheng.xingming=="余浩",ChuFang.mingcheng=="麻黄汤")).all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)        