#-*- coding: UTF-8 -*-
from plone.directives import form


# Interface class; used to define content-type schema.

class IFolder(form.Schema):
    """
    Chinese.medical.science base folder
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/topicfolder.xml to define the content type
    # and add directives here as necessary.

