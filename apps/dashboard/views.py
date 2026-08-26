from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.dashboard.forms import LoginForm, TaskForm
from apps.tasks.models import Task


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method=="POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            user = authenticate(
                request,
                email=email,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect("dashboard")
            
            form.add_error(
                None,
                "Invalid email or password.",
            )
    else:
        form = LoginForm()

    return render(
        request,
        "dashboard/login.html",
        {"form": form},
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
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(
                request,
                "Task created successfully.",
            )
            return redirect("dashboard")
    
    else:
        form = TaskForm()
    
    return render(
        request,
        "dashboard/create_task.html",
        {"form": form},
    )


@login_required
def task_detail(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        owner=request.user,
    )

    return render(
        request,
        "dashboard/task_detail.html",  
        {"task": task}
    )


@login_required
def edit_task(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        owner = request.user,
    )
    
    if request.method=="POST":
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            form.save()
            
            messages.success(
                request,
                "Task updated successfully.",
            )
            
            return redirect(
                "task-detail",
                pk=task.pk
            )
    else:
        form = TaskForm(instance=task)
        
    return render(
        request,
        "dashboard/edit_task.html",
        {"form": form,"task": task},
    )
            

@login_required
def delete_task(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        owner = request.user,
    )
    
    if request.method=="POST":
        task.delete()

        messages.success(
            request,
            "Task deleted successfully.",
        )
        
        return redirect("dashboard")
    
    return render(
        request,
        "dashboard/delete_task.html",
        {"task": task},
    )