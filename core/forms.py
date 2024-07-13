from django import forms
from django.utils.text import slugify  # Import qilish

from .models import Category,Maqola


class AddPageForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label='Boshqa katigoriya',label='Katigoriya')

    class Meta:
        model = Maqola
        fields = ['title', 'content', 'cat']  # 'filelds' o'rniga 'fields'
        widgets = {
            'title': forms.TextInput(
                attrs={"class": "form-input", 
                       'style': 'width: 600px;  font-size: 16px;'}
                ),
            'content': forms.Textarea(attrs={'cols': 69, 'rows': 10})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title and not cleaned_data.get('slug'):
            cleaned_data['slug'] = slugify(title)
        return cleaned_data
    

class UpdateForm(forms.ModelForm):
    IS_PUBLISHED_CHOICES = [
        (True, 'Ruxsat Berish'),
        (False, 'Rad qilish')
    ]

    is_published = forms.ChoiceField(
        choices=IS_PUBLISHED_CHOICES,
        widget=forms.RadioSelect
    )
    class Meta:
        model = Maqola
        fields = ['title', 'content', 'is_published',"message"]  # Barcha ustunlarni ko'rsatish
        widgets = {
            'is_published': forms.RadioSelect(),
            'rejection': forms.RadioSelect(),
            'message ':forms.Textarea(attrs={'cols': 40, 'rows': 30})
        }

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['readonly'] = True
        self.fields['content'].widget.attrs['readonly'] = True
        self.fields['title'].widget.attrs['style'] = 'width: 600px; font-size: 16px;'
        self.fields['content'].widget.attrs['style'] = 'width: 600px; height: 400px; font-size: 16px;'
    