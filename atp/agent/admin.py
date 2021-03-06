from django.contrib import admin
from agent.models import *
from agent.forms import *
from django import forms
from ajax_upload.widgets import AjaxClearableFileInput
from suit.widgets import SuitDateWidget
from fsm_admin.mixins import FSMTransitionMixin

# Register your models here.

##
# Agent Id Card
##
class AgentIdCardInlineForm(forms.ModelForm):
    class Meta:
        model = AgentIdCard
        widgets = {
                'id_card_front': AjaxClearableFileInput(),
                'id_card_back': AjaxClearableFileInput(),
                'id_card_validity_start_date': SuitDateWidget,
                'id_card_validity_end_date': SuitDateWidget,
                }


class AgentIdCardInline(admin.StackedInline):
    model = AgentIdCard
    max_num = 1
    extra = 0
    suit_classes = 'suit-tab suit-tab-id_card'
    form = AgentIdCardInlineForm

    def has_delete_permission(self, request, obj=None):
            return False


##
# Agent Pro Card
##
class AgentProCardInlineForm(forms.ModelForm):
    class Meta:
        model = AgentProCard
        widgets = {
                'pro_card_front': AjaxClearableFileInput(),
                }


class AgentProCardInline(admin.StackedInline):
    model = AgentProCard
    max_num = 1
    extra = 0
    suit_classes = 'suit-tab suit-tab-pro_card'
    form = AgentProCardInlineForm

    def has_delete_permission(self, request, obj=None):
            return False


##
# Agent Certification 
##
class AgentCertificationInlineForm(forms.ModelForm):
    class Meta:
        model = AgentCertification
        widgets = {
                'picture': AjaxClearableFileInput(),
                }


class CertificationsInline(admin.StackedInline):
    model = AgentCertification
    suit_classes = 'suit-tab suit-tab-certifications'
    max_num = 3
    extra = 1


##
# Agent Address
##
class AgentAddressInline(admin.StackedInline):
    model = AgentAddress
    max_num = 1
    extra = 0
    suit_classes = 'suit-tab suit-tab-address'

    def has_delete_permission(self, request, obj=None):
            return False


class AgentAdminForm(forms.ModelForm):
    class Meta:
        model = Agent
        widgets = {
                'picture': AjaxClearableFileInput(),
                }


##
# Agent Qualification 
##
class AgentQualificationInline(admin.StackedInline):
    model = AgentQualification
    suit_classes = 'suit-tab suit-tab-qualifications'
    max_num = 5
    extra = 1

    def has_delete_permission(self, request, obj=None):
            return False

##
# Agent Various 
##
class AgentVariousInlineForm(forms.ModelForm):
    class Meta:
        model = AgentVarious


class AgentVariousInline(admin.StackedInline):
    model = AgentVarious
    max_num =3 
    extra = 3
    suit_classes = 'suit-tab suit-tab-various'
    form = AgentVariousInlineForm

##
# Agent
##
class AgentAdmin(FSMTransitionMixin, admin.ModelAdmin):
    inlines = (CertificationsInline, AgentIdCardInline, AgentAddressInline, AgentProCardInline, AgentQualificationInline, AgentVariousInline)
    form = AgentAdminForm
    list_filter = ('birthdate', 'birthplace', 'qualifications', 'certifications', 'last_modified',)
    filter_vertical = ()

    fieldsets = [
        ('Etat Civil', {
            'classes': ('suit-tab', 'suit-tab-etat_civil'),
            'fields': ['firstname', 'lastname', 'genre', 'nationality', 'birthdate', 'birthplace', 'picture']
            }),
        ]
    suit_form_tabs = (('etat_civil', 'Etat civil'), ('various', 'VARIOUS'), ('id_card', 'Papiers identite'), ('address', 'Coordonnees'), ('pro_card', 'Carte Pro'), ('qualifications', 'Qualifications'), ('certifications', 'Certifications'))

    class Media:
        css = {
            'all': ('ajax_upload/css/ajax-upload-widget.css',)
            }
        js = [
            'ajax_upload/js/ajax-upload-widget.js',
            'ajax_upload/js/jquery.iframe-transport.js',
            'js/project.js',
        ]


class QualificationAdmin(admin.ModelAdmin):
    pass


class CertificationAdmin(admin.ModelAdmin):
    pass


class StatesAdmin(admin.ModelAdmin):
    pass


class AreaDepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Agent,AgentAdmin)
admin.site.register(Certification,CertificationAdmin)
admin.site.register(Qualification,QualificationAdmin)
admin.site.register(States,StatesAdmin)
admin.site.register(AreaDepartment,AreaDepartmentAdmin)
# admin.site.register(Certification,CertificationAdmin)
