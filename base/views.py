from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import UserRegistrationForm, TodoForm
from .models import TodoItem


@login_required
def home(request):
    if request.method == 'POST':
        todo_name = request.POST.get("new-todo")
        TodoItem.objects.create(name=todo_name, user=request.user)
        return redirect("home")

    todos = TodoItem.objects.filter(user=request.user, is_completed=False).order_by("-id")

    # pagination 4 items per page
    paginator = Paginator(todos, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"todos": todos, "page_obj": page_obj}

    return render(request, "base/crud.html", context)


def register(request):
    """
    User Registration form

    Args:
        request (POST): New user registered
    """
    UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "base/register.html", context)


def logout_user(request):
    logout(request)
    return redirect("login")


def update_todo(request, pk):
    # NOTE: below get_object_or_404() returns a data if exists else status 404 not found
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.name = request.POST.get(f"todo_{pk}")
    todo.save()
    # return redirect("home")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def complete_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.is_completed = True
    todo.save()
    # return redirect("home")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.delete()
    # return redirect("home")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
