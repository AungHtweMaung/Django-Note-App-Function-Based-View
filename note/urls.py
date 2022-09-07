from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('create/note', views.create_note, name="create_note"),
    path('create/category', views.create_category, name="create_category"),
    path('edit/note/<int:id>', views.edit_note, name="edit_note"),
    path('delete/note/<int:id>', views.delete_note,name="delete_note"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/note/<int:id>', views.note_detail, name="note_detail")
]
