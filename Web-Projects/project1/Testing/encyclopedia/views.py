from django.shortcuts import render, redirect
from markdown2 import markdown, Markdown
from . import util
from django import forms
import secrets

class NewEntryForm(forms.Form):
    title = forms.CharField(label="New entry title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        content = "## Page was not Found"
    content = markdown(content)
    return render(request, 'encyclopedia/entry.html', {
        "title": title,
        "content": content
    })

def search(request):
    q_value = request.GET.get('q')

    if util.get_entry(q_value) != None:
        return redirect("entry", title=q_value)

    substringEntry = []
    entries = util.list_entries()
    for entry in entries:
        if q_value.upper() in entry.upper():
            substringEntry += [entry]

    return render(request, 'encyclopedia/search.html', {
        'title': q_value,
        'entries': substringEntry
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            # Give error message if they don't fill any of these fields.
            if title == "" or content == "":
                return render(request, 'encyclopedia/create.html', {
                    'message': "Please fill these given fields!",
                    'form': NewEntryForm()
                })
            # Check if the entry already exists.
            if util.get_entry(title) != None:
                return render(request, 'encyclopedia/create.html', {
                    'message': "This Entry already Exists!",
                    'form': NewEntryForm(request.POST)
                })
            # Else, save the entry and redirect to the entry page I just created.
            util.save_entry(title, content)
            return redirect('entry', title=title)

    return render(request, 'encyclopedia/create.html', {
        'form': NewEntryForm()
    })

def edit(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, 'encyclopedia/Error.html', {
            'message': "404 Error: Page not Found!"
        })

    if request.method == "POST":
        Newcontent = request.POST.get('content')
        if Newcontent == "":
            return render(request, 'encyclopedia/edit.html', {
                'message': "Please fill this given field!",
                'title': title
            })
        util.save_entry(title, Newcontent)
        return redirect('entry', title=title)

    return render(request, 'encyclopedia/edit.html', {
        "content": content,
        'title': title
    })
