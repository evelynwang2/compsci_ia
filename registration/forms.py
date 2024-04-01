from django.forms import ModelForm
from .models import Delegate, Delegation, Team, Registry

class RegisterIndForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['school'].widget.attrs.update({'class': 'form-select'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['fname'].widget.attrs.update({'class': 'form-control'})
        self.fields['lname'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-select'})
        self.fields['race'].widget.attrs.update({'class': 'form-select'})
        self.fields['grade'].widget.attrs.update({'class': 'form-select'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['addr'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-select'})
        self.fields['zip'].widget.attrs.update({'class': 'form-control'})
        self.fields['parentName'].widget.attrs.update({'class': 'form-control'})
        self.fields['parentEmail'].widget.attrs.update({'class': 'form-control'})
        self.fields['parentPhone'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Delegate
        fields = ['school','role','firstName','lastName'
                  ,'gender','race','grade','email'
                  ,'mobilePhone','streetAddr','city','state'
                  ,'zip','parentName','parentEmail']    
