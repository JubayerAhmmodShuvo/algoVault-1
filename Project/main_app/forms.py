from django import forms
from .models import Tutorial
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Tutorial
        fields = '__all__'
        exclude = ['isApproved', 'author']