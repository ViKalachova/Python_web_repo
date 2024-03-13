from django.forms import ModelForm, CharField, TextInput, ModelChoiceField, ModelMultipleChoiceField, SelectMultiple
from .models import Tag, Quote, Author


class AuthorForm(ModelForm):
    fullname = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    born_date = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    born_location = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=5, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class TagForm(ModelForm):
    tag_name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['tag_name']

class QuoteForm(ModelForm):
    artist = ModelChoiceField(queryset=Author.objects.all())
    quote = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=SelectMultiple, required=False)

    class Meta:
        model = Quote
        fields = ['artist', 'quote', 'tags']