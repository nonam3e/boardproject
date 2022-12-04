from django.urls import  path
from board import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = "home"),
    path('changes/', views.changes, name = "changes"),
    path('login/',auth_views.LoginView.as_view(template_name = 'board/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'board/logout.html'), name='logout'), 
    path('add_to_stock/<int:pk>', views.add_to_stock, name='add_to_stock'),
    path('remove_from_stock/<int:pk>', views.remove_from_stock, name='remove_from_stock')
]