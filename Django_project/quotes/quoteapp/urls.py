from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('quote/', views.quote, name='quote'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    path('scrape-and-add/', views.scrape_and_add, name='scrape_and_add'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
]
