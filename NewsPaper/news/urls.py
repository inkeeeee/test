from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList


urlpatterns = [
   path('', PostsList.as_view()),
]