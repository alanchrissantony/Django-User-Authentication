from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.login, name='signin'),
    path('signout', views.signout, name='signout'),
    path('', views.admin, name='admin'),
    path('root', views.root, name='root'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
]