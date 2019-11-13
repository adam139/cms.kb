from plone.app.registry.browser import controlpanel

from cms.db.interfaces import ISysSettings
from cms.db import _

try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget

class SettingsEditForm(controlpanel.RegistryEditForm):
    
    schema = ISysSettings
    label = _(u"system settings") 
    description = _(u"Please enter details of system")
    
    def updateFields(self):
        super(LogSettingsEditForm, self).updateFields()
        self.fields['timeout'].widgetFactory = TextLinesFieldWidget
        self.fields['max'].widgetFactory = TextLinesFieldWidget
        self.fields['percentage'].widgetFactory = TextLinesFieldWidget        
        self.fields['bsize'].widgetFactory = TextLinesFieldWidget

    
class SettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SettingsEditForm