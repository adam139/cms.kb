from z3c.formwidget.query.interfaces import IQuerySource
from zope.interface import Interface, implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import queryUtility
from cms.db.interfaces import IDbapi

from cms.db.browser.utility import getDanWeiId
from cms.db.orm import Yao_DanWei_Asso
from cms.db.orm import Yao


@implementer(IQuerySource)
class YaoSource(object):
    def __init__(self, context):
        self.context = context
        locator = queryUtility(IDbapi, name='yao')
        daiweiid = getDanWeiId()
        # all_a_except_b(self,a_cls,b_cls,b_a_fk,b_id,pk)
        values = locator.all_a_except_b(Yao,Yao_DanWei_Asso,"yao_id","danwei_id",daiweiid)
        self.vocab = SimpleVocabulary(
            [SimpleTerm(value=int(i.id), token=str(i.id), title=i.mingcheng) for i in values],
        )
        self.items = [(i.id,i.mingcheng,) for i in values]
        
    def __contains__(self, term):
        return self.vocab.__contains__(term)

    def __iter__(self):
        return self.vocab.__iter__()

    def __len__(self):
        return self.vocab.__len__()

    def getTerm(self, value):
        return self.vocab.getTerm(value)

    def getTermByToken(self, value):
        return self.vocab.getTermByToken(value)

    def search(self, query_string):
        q = query_string.lower()
        return [self.getTerm(kw[0]) for kw in self.items if q in kw[1].lower()]

    
@implementer(IContextSourceBinder)
class YaoSourceBinder(object):

    def __call__(self, context):
        return YaoSource(context)

