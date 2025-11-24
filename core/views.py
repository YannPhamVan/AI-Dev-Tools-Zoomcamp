from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Todo
from .forms import TodoForm

# Create your views here.

def home(request):
    return HttpResponse('Hello from core app!')

class TodoListView(ListView):
    model = Todo
    template_name = 'core/todo_list.html'
    context_object_name = 'todos'


class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'core/todo_form.html'
    success_url = reverse_lazy('core:list')


class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'core/todo_form.html'
    success_url = reverse_lazy('core:list')


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'core/todo_confirm_delete.html'
    success_url = reverse_lazy('core:list')


def toggle_completed(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('core:list')
