from django.forms import ModelForm
from .models import Note, Category

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['category', 'title', 'text']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']