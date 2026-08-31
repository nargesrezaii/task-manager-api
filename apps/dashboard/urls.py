from django.urls import path

from apps.dashboard.views import (
    dashboard,
    login_view,
    logout_view,
    create_task,
    edit_task,
    delete_task,
    task_detail,
    register_view,
    profile,
    change_password,
)


urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('tasks/create/', create_task, name="create-task"),
    path('tasks/<int:pk>/', task_detail, name="task-detail"),
    path('tasks/<int:pk>/edit/', edit_task, name="edit-task"),
    path('tasks/<int:pk>/delete/', delete_task, name="delete-task"),
    path('register/', register_view, name="register"),
    path('profile/', profile, name="profile"),
     path('change-password/', change_password, name="change-password"),
]