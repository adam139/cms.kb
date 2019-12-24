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

from cms.db.contents.folder import IFolder
from cms.db.contents.ormfolder import IOrmfolder
from sqlalchemy import and_
from cms.db import  Session
from cms.db.tests.base import inputvalues,cleardb
from cms.db.tests.base import TABLES

for tb in TABLES:
    import_str = "from %(p)s import %(t)s" % dict(p='cms.db.orm',t=tb) 
    exec import_str


class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        inputvalues()
   
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('cms.db.folder', 'folder')
        portal['folder'].invokeFactory('cms.db.ormfolder', 'ormfolder')
        portal['folder'].invokeFactory('cms.db.yaofolder', 'yaofolder')
        portal['folder'].invokeFactory('cms.db.chufangfolder', 'chufangfolder')
        portal['folder'].invokeFactory('cms.db.bingrenfolder', 'bingrenfolder')
        portal['folder'].invokeFactory('cms.db.yishengfolder', 'yishengfolder')
        portal['folder'].invokeFactory('cms.db.danweifolder', 'danweifolder')               
        self.portal = portal

    def tearDown(self):
        cleardb()       
                
        
    def testfolderView(self):

        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        browser.open(portal['folder'].absolute_url())        
        self.assertTrue('class="pat-structure"' in browser.contents)
   
    def ormfolderView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
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
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open(base + "/@@yaoxing_listings")      
        self.assertTrue("温" in browser.contents)
        
    def testYaoWeiView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open(base + "/@@yaowei_listings")
        self.assertTrue("甘" in browser.contents)
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
        browser.getControl(name=u"form.widgets.xing").value = u"微寒"        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(YaoXing).filter(YaoXing.xing==u"微寒").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)        


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

        browser.getControl(name=u"form.widgets.mingcheng").value = u"手太阳小肠经"        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(JingLuo).filter(JingLuo.mingcheng==u"手太阳小肠经").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)
        
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
        browser.getControl(name=u"form.widgets.yaowei:list").value = [str(yaowei_id)]
        browser.getControl(name=u"form.widgets.yaoxing:list").value = [str(yaoxing_id)]
        browser.getControl(name=u"form.widgets.mingcheng").value = u"牛膝"         
#         browser.getControl(name=u"form.widgets.guijing.to").value = [str(jingluo_id)] 
        browser.getControl(name=u"form.widgets.zhuzhi").value = u"引气血下行"
        browser.getControl(name=u"form.widgets.yongliang").value = str(30)        
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

    def testInputGeRenDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_gerendizhi" % base)        
        # Fill in the form 
        browser.getControl(name=u"form.widgets.guojia").value = u"中国"
        browser.getControl(name=u"form.widgets.sheng").value = u"湖南"
        browser.getControl(name=u"form.widgets.shi").value = u"长沙市"
        browser.getControl(name=u"form.widgets.jiedao").value = u"五一大道83号"                        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(GeRenDiZhi).filter(GeRenDiZhi.shi==u"长沙市").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testInputDanWeiDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        # Open form
        browser.open("%s/@@input_danweidizhi" % base)        
        # Fill in the form 
        browser.getControl(name=u"form.widgets.guojia").value = u"中国"
        browser.getControl(name=u"form.widgets.sheng").value = u"湖南"
        browser.getControl(name=u"form.widgets.shi").value = u"长沙市"
        browser.getControl(name=u"form.widgets.jiedao").value = u"五一大道83号"
        browser.getControl(name=u"form.widgets.wangzhi").value = u"www.21cn.com"
        browser.getControl(name=u"form.widgets.gongzhonghao").value = u"zhongyi3"                        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.shi==u"长沙市").all()
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
        dizhi_id = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.shi==u"湘潭市").first().id      
        # Fill in the form 
        browser.getControl(name=u"form.widgets.mingcheng").value = u"泽生堂"
        browser.getControl(name=u"form.widgets.dizhi:list").value =[str(dizhi_id)]                         
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(DanWei).join(DanWeiDiZhi).filter(DanWeiDiZhi.shi==u"湘潭市").all()
        self.assertEqual(len(suan),2)
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
        browser.getControl(name=u"form.widgets.danwei:list").value = [str(danwei_id)]   
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
        dizhi_id = Session.query(GeRenDiZhi).filter(GeRenDiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组83号").first().id      
        # Fill in the form        
        browser.getControl(name=u"form.widgets.dizhi_id").value = str(dizhi_id)               
        browser.getControl(name=u"form.widgets.xingming").value = "张dong"
        browser.getControl(name=u"form.widgets.xingbie:list").value = ['1']
        browser.getControl(name=u"form.widgets.shengri").value =  "2015-09-12"
        browser.getControl(name=u"form.widgets.dianhua").value = "13873265859"                        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(BingRen).join(GeRenDiZhi).filter(and_(GeRenDiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组83号",BingRen.xingming=="张dong")).all()
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
        browser.getControl(name=u"form.widgets.bingrens.buttons.add").click()
        yisheng_id = Session.query(YiSheng).filter(YiSheng.xingming=="余浩").first().id
        bingren_id = Session.query(BingRen).filter(BingRen.xingming=="张三").first().id
        
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
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.bingren_id:list").value = [str(bingren_id)]
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.shijian").value = "2015-09-12 12:00"
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.maixiang").value = "两关郁,左寸小,右寸大"
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.shexiang").value = "舌苔淡青,有齿痕"
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.zhusu").value = "小腹冷痛,右肋痛,牙痛"
                                
        # Submit
        browser.getControl(u"Submit").click()        
        suan = Session.query(ChuFang).join(YiSheng).filter(and_(YiSheng.xingming=="余浩",ChuFang.mingcheng=="麻黄汤")).all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)
        
# edit forms
    def testUpdateYaoXingForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        yaoxing_id = Session.query(YaoXing).filter(YaoXing.xing==u"寒").first().id
        # Open form
        browser.open("%s/@@update_yaoxing/%s" % (base,yaoxing_id))        
        # Fill in the form 
#         browser.getControl(name=u"form.widgets.id").value = str(yaoxing_id)
        browser.getControl(name=u"form.widgets.xing").value = u"微寒"        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(YaoXing).filter(YaoXing.xing==u"微寒").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)
        
        
    def testUpdateYaoForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        yao_id = Session.query(Yao).filter(Yao.mingcheng==u"大枣").first().id
        yaowei_id = Session.query(YaoWei).filter(YaoWei.wei=="甘").first().id
        # Open form
        browser.open("%s/@@update_yao/%s" % (base,yao_id))


        browser.getControl(name=u"form.widgets.yaowei:list").value = [str(yaowei_id)]
        browser.getControl(name=u"form.widgets.zhuzhi").value = u"主脾胃"
        browser.getControl(name=u"form.widgets.yongliang").value = str(31)        
        browser.getControl(u"Submit").click()        
        suan = Session.query(Yao).filter(Yao.zhuzhi==u"主脾胃").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)
       
    def testUpdateChuFangForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        chufang_id = Session.query(ChuFang).filter(ChuFang.mingcheng=="桂枝汤").first().id
        yisheng_id = Session.query(YiSheng).filter(YiSheng.xingming=="余浩").first().id
        bingren_id = Session.query(BingRen).filter(BingRen.xingming=="张三").first().id
        
        yao_id = Session.query(Yao).filter(Yao.mingcheng=="麻黄").first().id
        yao_id2 = Session.query(Yao).filter(Yao.mingcheng=="桂枝").first().id       
        # Open form
        browser.open("%s/@@update_chufang/%s" % (base,chufang_id))
      
        # Fill in the form              
        browser.getControl(name=u"form.widgets.mingcheng").value = "麻黄汤"
        browser.getControl(name=u"form.widgets.yizhu").value = "主脾胃"
        browser.getControl(name=u"form.widgets.jiliang").value =  "3"
        browser.getControl(name=u"form.widgets.yisheng:list").value = [str(yisheng_id)]
        #fill subform
        browser.getControl(name=u"form.widgets.yaoes.0.widgets.yao_id:list").value = [str(yao_id)]
        browser.getControl(name=u"form.widgets.yaoes.0.widgets.yaoliang").value = '15'
        browser.getControl(name=u"form.widgets.yaoes.0.widgets.paozhi").value = 'pao zhi'
        browser.getControl(name=u"form.widgets.yaoes.1.widgets.yao_id:list").value = [str(yao_id2)]        
        browser.getControl(name=u"form.widgets.yaoes.1.widgets.yaoliang").value = '20'
        browser.getControl(name=u"form.widgets.yaoes.1.widgets.paozhi").value = '晒干'        
        
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.bingren_id:list").value = [str(bingren_id)]
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.shijian").value = "2018-09-12 12:00"
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.maixiang").value = "两关郁,左寸小,右寸大,右尺大"
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.shexiang").value = "舌苔淡白,有齿痕"
        browser.getControl(name=u"form.widgets.bingrens.0.widgets.zhusu").value = "小腹冷痛,右肋痛,牙痛,畏冷"        
        browser.getControl(u"Submit").click()        
        suan = Session.query(ChuFang).filter(ChuFang.yizhu==u"主脾胃").all()
        self.assertEqual(len(suan),1)
        suan = Session.query(ChuFang).join(ChuFang_BingRen_Asso).filter(ChuFang_BingRen_Asso.zhusu==u"小腹冷痛,右肋痛,牙痛,畏冷").all()
        self.assertEqual(len(suan),1)        
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testUpdateDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        dizhi_id = Session.query(DiZhi).filter(DiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组183号").first().id
        # Open form
        browser.open("%s/@@update_dizhi/%s" % (base,dizhi_id))
        browser.getControl(name=u"form.widgets.jiedao").value = "茅箭区施洋路85号"       
        browser.getControl(u"Submit").click()        
        suan = Session.query(DiZhi).filter(DiZhi.jiedao=="茅箭区施洋路85号").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testUpdateGeRenDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        dizhi_id = Session.query(GeRenDiZhi).filter(GeRenDiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组83号").first().id
        # Open form
        browser.open("%s/@@update_gerendizhi/%s" % (base,dizhi_id))
        browser.getControl(name=u"form.widgets.jiedao").value = "茅箭区施洋路85号"       
        browser.getControl(u"Submit").click()        
        suan = Session.query(GeRenDiZhi).filter(GeRenDiZhi.jiedao=="茅箭区施洋路85号").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testUpdateDanWeiDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        dizhi_id = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组38号").first().id
        # Open form
        browser.open("%s/@@update_danweidizhi/%s" % (base,dizhi_id))
        browser.getControl(name=u"form.widgets.jiedao").value = "茅箭区施洋路85号"
        browser.getControl(name=u"form.widgets.wangzhi").value = "www.21cn.com"
        browser.getControl(name=u"form.widgets.gongzhonghao").value = "zhongyi2"       
        browser.getControl(u"Submit").click()        
        suan = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.jiedao=="茅箭区施洋路85号").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)


    def testUpdateDanWeiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        danwei_id = Session.query(DanWei).filter(DanWei.mingcheng=="任之堂").first().id
        dizhi_id = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组38号").first().id
        # Open form
        browser.open("%s/@@update_danwei/%s" % (base,danwei_id))
        browser.getControl(name=u"form.widgets.dizhi:list").value = [str(dizhi_id)]
        browser.getControl(name=u"form.widgets.mingcheng").value = "润生堂"       
        browser.getControl(u"Submit").click()        
        suan = Session.query(DanWei).join(DanWeiDiZhi).filter(DanWeiDiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组38号").all()
        self.assertEqual(len(suan),2)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testUpdateYiShengForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        yisheng_id = Session.query(YiSheng).filter(YiSheng.xingming=="余浩").first().id
        danwei_id = Session.query(DanWei).filter(DanWei.mingcheng=="润生堂").first().id
        # Open form
        browser.open("%s/@@update_yisheng/%s" % (base,yisheng_id))
        browser.getControl(name=u"form.widgets.danwei:list").value = [str(danwei_id)]
        browser.getControl(name=u"form.widgets.shengri").value = "2013-09-12"       
        browser.getControl(u"Submit").click()        
        suan = Session.query(YiSheng).join(DanWei).filter(DanWei.mingcheng=="润生堂").all()
        self.assertEqual(len(suan),1)
        self.assertTrue(u"Thank you! Your data  will be update in back end DB." in browser.contents)

    def testUpdateBingRenForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        dizhi_id = Session.query(GeRenDiZhi).filter(DiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组83号").first().id
        bingren_id = Session.query(BingRen).filter(BingRen.xingming=="张三").first().id
        # Open form
        browser.open("%s/@@update_bingren/%s" % (base,bingren_id))
      
        # Fill in the form              
        browser.getControl(name=u"form.widgets.xingming").value = "李四"
        browser.getControl(name=u"form.widgets.dizhi:list").value = [str(dizhi_id)]
      
        browser.getControl(u"Submit").click()        
        suan = Session.query(BingRen).join(GeRenDiZhi).filter(GeRenDiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组83号").all()
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
        id = Session.query(YaoWei).filter(YaoWei.wei=="甘").one().id
        # Open form
        browser.open("%s/@@delete_yaowei/%s" % (base,id))        
        # Fill in the form 
        browser.getControl(name=u"form.widgets.wei").value = "甘"        
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(YaoWei).filter(YaoWei.wei=="甘").all()
        self.assertEqual(len(suan),0)
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

    def testDeleteYaoXingForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        id = Session.query(YaoXing).filter(YaoXing.xing=="温").one().id
        # Open form
        browser.open("%s/@@delete_yaoxing/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(YaoXing).filter(YaoXing.xing=="温").all()
        self.assertEqual(len(suan),0)
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

    def testDeleteJingLuoForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        id = Session.query(JingLuo).filter(JingLuo.mingcheng=="足阳明胃经").one().id
        # Open form
        browser.open("%s/@@delete_jingluo/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(JingLuo).filter(JingLuo.mingcheng=="足阳明胃经").all()
        self.assertEqual(len(suan),1)
        id = Session.query(JingLuo).filter(JingLuo.mingcheng=="足太阴脾经").one().id
        # Open form
        browser.open("%s/@@delete_jingluo/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(JingLuo).filter(JingLuo.mingcheng=="足太阴脾经").all()
        self.assertEqual(len(suan),0)        
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

    def testDeleteDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        id = Session.query(DiZhi).filter(DiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组183号").one().id
        # Open form
        browser.open("%s/@@delete_dizhi/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(DiZhi).filter(DiZhi.jiedao=="湘潭县云湖桥镇北岸村道林组183号").all()
        self.assertEqual(len(suan),0)      
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

    def testDeleteGeRenDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open("%s/@@input_gerendizhi" % base)        
        # Fill in the form 
        browser.getControl(name=u"form.widgets.guojia").value = u"中国"
        browser.getControl(name=u"form.widgets.sheng").value = u"湖南"
        browser.getControl(name=u"form.widgets.shi").value = u"长沙市"
        browser.getControl(name=u"form.widgets.jiedao").value = u"五一大道83号"
        browser.getControl(u"Submit").click()
        suan = Session.query(GeRenDiZhi).filter(GeRenDiZhi.jiedao=="五一大道83号").all()
        self.assertEqual(len(suan),1)                 
        id = Session.query(GeRenDiZhi).filter(GeRenDiZhi.jiedao=="五一大道83号").one().id
        # Open form
        browser.open("%s/@@delete_gerendizhi/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(GeRenDiZhi).filter(GeRenDiZhi.jiedao=="五一大道83号").all()
        self.assertEqual(len(suan),0)      
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

    def testDeleteDanWeiDiZhiForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open("%s/@@input_danweidizhi" % base)        
        # Fill in the form 
        browser.getControl(name=u"form.widgets.guojia").value = u"中国"
        browser.getControl(name=u"form.widgets.sheng").value = u"湖南"
        browser.getControl(name=u"form.widgets.shi").value = u"长沙市"
        browser.getControl(name=u"form.widgets.jiedao").value = u"五一大道83号"
        browser.getControl(name=u"form.widgets.wangzhi").value = u"www.21cn.com"
        browser.getControl(name=u"form.widgets.gongzhonghao").value = u"zhongyi3"
        browser.getControl(u"Submit").click()
        suan = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.jiedao=="五一大道83号").all()
        self.assertEqual(len(suan),1)                 
        id = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.jiedao=="五一大道83号").one().id
        # Open form
        browser.open("%s/@@delete_danweidizhi/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.jiedao=="五一大道83号").all()
        self.assertEqual(len(suan),0)      
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

    def testDeleteYaoForm(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        id = Session.query(Yao).filter(Yao.mingcheng=="白芍").one().id
        # Open form
        browser.open("%s/@@delete_yao/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(Yao).filter(Yao.mingcheng=="白芍").all()
        self.assertEqual(len(suan),1)
        id = Session.query(Yao).filter(Yao.mingcheng=="麻黄").one().id
        # Open form
        browser.open("%s/@@delete_yao/%s" % (base,id))             
        # Submit
        browser.getControl(u"Delete").click()
        suan = Session.query(Yao).filter(Yao.mingcheng=="麻黄").all()
        self.assertEqual(len(suan),0)        
        self.assertTrue(u"Your data  has been deleted." in browser.contents)

    def test_asso_proxyChuFang(self):

        chufang = Session.query(ChuFang).filter(ChuFang.mingcheng=="桂枝汤").first()
        self.assertEqual(len(chufang.yaoes),2)
        chufang_id = chufang.id
        jingluo = JingLuo("手太阳小肠经")
        yaoxing = YaoXing("平")
        yaowei = YaoWei("淡")
        yao1 = Yao("杏仁")
        yao1.yaowei = yaowei
        yao1.yaoxing = yaoxing
        yao1.guijing = [jingluo]
        yao_chufang = Yao_ChuFang_Asso(yao1,chufang,9,"炒")        
        Session.add_all([jingluo,yaoxing,yaowei,yao1,yao_chufang])
        Session.commit()
        self.assertEqual(len(chufang.yaoes),3)
        yao = Session.query(Yao).filter(Yao.mingcheng=="杏仁").first()
        chufang.yaoes = [yao]
        Session.add(chufang)
        Session.commit()
        self.assertEqual(len(chufang.yaoes),1)
        
  
        
                                 