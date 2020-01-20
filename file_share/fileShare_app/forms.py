from django import forms
from .models import MyFile


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = MyFile
        fields = ['description','a_file'] 