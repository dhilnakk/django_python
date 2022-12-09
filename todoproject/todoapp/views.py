from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from todoapp.models import Task
from .forms import TodoForm
# Create your views here.
class TodoListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task1'

class TodoDetailedView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'
class TodoUpdateView(UpdateView):
    model = Task
    template_name = 'edit.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={ pk:self.object.id})
class TodoDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy("todoapp:cbvhome")

def todo(request):
    task1 = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task')
        priority=request.POST.get('priority')
        date = request.POST.get('date')
        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request, 'home.html',{'task1':task1})
def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method == 'POST' :
        task.delete()
        return redirect('/')
    return render(request,'delete.html')
def update(request,id):
    task=Task.objects.get(id=id)
    frm = TodoForm(request.POST or None,instance=task)
    if frm.is_valid():
        frm.save()
        return redirect('/')
    return render(request,'edit.html',{'frm':frm,'task':task})

