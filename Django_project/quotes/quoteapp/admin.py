from django.contrib import admin
from .models import Tag, Quote, Author

# Register your models here.
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Quote)
