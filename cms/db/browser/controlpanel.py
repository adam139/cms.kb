from plone.app.registry.browser import controlpanel
from cms.db.browser.interfaces import IAutomaticTypesSettings
from cms.db import _


class TypesSettingsEditForm(controlpanel.RegistryEditForm):
    
    schema = IAutomaticTypesSettings
    label = _(u"automatic create content types list") 
    description = _(u"automatic create content types list")
    
    def updateFields(self):
        super(TypesSettingsEditForm, self).updateFields()

    
class TypesSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TypesSettingsEditForm