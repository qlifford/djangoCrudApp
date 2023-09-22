from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from . import models
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin




from .models import Task


class CustomLoginView(LoginView):
    template_name = 'todos/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterUserView(FormView):
        template_name = 'todos/register.html'
        form_class = UserCreationForm
        redirect_authenticated_user = True
        success_url = reverse_lazy('tasks')

        def form_valid(self, form):
            user = form.save()
            if user is not None:
                login(self.request, user)
            return super(RegisterUserView, self).form_valid(form)
        
        def get(self, *args, **kwargs):
            if self.request.user.is_authenticated:
                return redirect('tasks')
            return super(RegisterUserView, self).get(*args, **kwargs)



class TaskListView(LoginRequiredMixin, ListView):
    model = models.Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)


        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith = search_input)
        
        context['search_input'] = search_input

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'todos/task_detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    fields = ['title', 'details']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Task
    fields = ['title', 'details']
    success_url = reverse_lazy('tasks')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Task
    fields = '__all__'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
