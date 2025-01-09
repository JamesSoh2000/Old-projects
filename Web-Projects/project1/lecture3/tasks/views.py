from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.



class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        tasks = request.session["tasks"]
        if form.is_valid():
            # From class NewTaskFrom, we get a property named 'task'.
            task = form.cleaned_data["task"]
            # request.session["tasks"] is a list like ['first', 'second', 'third'] and if you do += a list like below it will be ['first', 'second', 'third', task]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
            # return HttpResponseRedirect("/tasks")
        else:
            return render(request,"tasks/add.html", {
                "form":form
            })
    return render(request, "tasks/add.html", {
        "form":NewTaskForm()
    })
