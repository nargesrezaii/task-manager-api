from django.urls import path

from apps.dashboard.views import (
    dashboard,
    login_view,
    logout_view,
    create_task,
    task_detail,
)


urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('tasks/create/', create_task, name="create-task"),
    path('tasks/<int:pk>/', task_detail, name="task-detail"),
]