from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash

from apps.dashboard.forms import (
    ChangePasswordForm,
    LoginForm,
    ProfileForm,
    RegistrationForm,
    TaskForm,
)

from apps.tasks.models import Task


User = get_user_model()


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


@login_required
def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect("login")
    
    return redirect("dashboard")


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


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create_user(
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"],  
            )
            
            login(request, user)
            
            messages.success(
                request,
                "Your account has been created.",
            )
            
            return redirect("dashboard")
    else:
        form = RegistrationForm()
        
    return render(
        request,
        "dashboard/register.html",
        {"form": form}
    )


@login_required
def profile(request):
    if request.method=="POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Profile updated successfully.",
            )
            
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
        
    return render(
        request,
        "dashboard/profile.html",
        {"form": form},
    )


@login_required
def change_password(request):
    if request.method=="POST":
        form = ChangePasswordForm(
            request.POST,
            user=request.user,
        )
        
        if form.is_valid():
            request.user.set_password(
                form.cleaned_data["new_password"]    
            )
            request.user.save()
            
            update_session_auth_hash(
                request,
                request.user,
            )
            
            messages.success(
                request,
                "Your password has been changed successfully.",
            )
            
            return redirect("profile")
    else:
        form = ChangePasswordForm(user=request.user)

    return render(
        request,
        "dashboard/change_password.html",
        {"form": form},
     )


@login_required
def complete_task(request, pk):
    task = get_object_or_404(
        Task,
        pk=pk,
        owner = request.user,
    )
    
    if request.method=="POST":
        task.status = Task.Status.COMPLETED,
        task.save(update_fields=["status", "updated_at"])
        
        messages.success(
            request,
            "Task marked as completed.",    
        )
        
        return redirect(
            request,
            "task-detail",
            pk=task.pk,           
        )
    
    return redirect(
        request,
        "task-detail",
        pk=task.pk,           
    )


@login_required
def task_list(request):
    tasks = Task.objects.filter(
        owner = request.user   
    ).order_by("-updated_at")
    
    return render(
        request,
        "dashboard/tasks.html",
        {"tasks": tasks},
    )









