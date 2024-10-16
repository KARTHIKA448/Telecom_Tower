from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Login as the default route
    path('signup/', views.register, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('viewdashboard/<int:id>/', views.detailedview, name='viewdashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('edit/<int:id>/', views.edit_view, name='edit'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),  

]
