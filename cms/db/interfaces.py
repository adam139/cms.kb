#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema

from cms.db import _

 
         

class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

# db insterface
class IDbapi (Interface):
    """Db api """

    def get_rownumber():
        "fetch table's rownumber"

    def bulk_delete():
        "bulk delete"

    def fetch_oldest():
        "fetch the oldest recorder from db"
        
        
