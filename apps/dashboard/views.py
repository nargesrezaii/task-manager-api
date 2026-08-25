import stat
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from apps.tasks.models import Task


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        
        return render(
            request,
            "dashboard/login.html",
            {"error": "Invalid email or password."},
        )
    
    return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)

    return redirect("login")


@login_required
def dashboard(request):
    tasks = Task.objects.filter(
        owner = request.user    
    ).order_by("-created_at")
    
    context = {
        "tasks": tasks[:5],
        "total_tasks": tasks.count(),
        "todo": tasks.filter(
            status=Task.Status.TODO
        ).count(),
        "in_progress": tasks.filter(
            status = Task.Status.IN_PROGRESS    
        ).count(),
        "completed": tasks.filter(
            status=Task.Status.COMPLETED,
        ).count()
    }
    
    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )


@login_required
def create_task(request):
    if request.method=="POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")

        Task.objects.create(
            owner = request.user,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
        )
        return redirect("dashboard")
    
    context = {
        "statuses": Task.Status.choices,
        "priorities": Task.Priority.choices,
    }
    
    return render(
        request,
        "dashboard/create_task.html",
        context,
    )

