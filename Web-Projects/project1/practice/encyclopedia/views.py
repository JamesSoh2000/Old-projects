from django.shortcuts import render, redirect
from markdown2 import markdown, Markdown
from . import util
from django import forms
import secrets
# secrets for picking random entry

class NewEntryForm(forms.Form):
    #  이 부분으로 아래 링크에서 widget사용법보셈. You might want a larger input element for the comment, and you might want the ‘name’ widget to have some special CSS class
    # https://docs.djangoproject.com/en/4.0/ref/forms/widgets/
    # 저 class는 bootstrap의 class들임 layout.html에 붙스트랩을 스타일앁으로 설정해놓아서 저렇게 가능
    task = forms.CharField(label="New Entry Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(label="Content Field", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entryPage = util.get_entry(title)
    if entryPage == None:
        entryPage = '## Page was not Found'
    # this markdown function takes the argument and turn it into HTML form ex. 위에 '## Page not found'를 샵을보고 <h2> Page was not found </h2>로 바꿔줌.
    entryPage = markdown(entryPage)
    return render(request, "encyclopedia/entry.html", {
        "content": entryPage, "title": title
    })

def search(request):
    q_value = request.GET.get('q').strip()
    if util.get_entry(q_value) != None:
        return redirect("entry", title=q_value)
    else:
        substringEntries = []
        for entry in util.list_entries():
            if q_value.upper() in entry.upper():
                substringEntries += [entry]

        return render(request, "encyclopedia/search.html", {
            "entries": substringEntries,
            "q_value": q_value
        })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["task"]
            content = form.cleaned_data["content"]
            # Check if the title is new(아직 존재하지않는 entry인지 확인) OR(아니면) form.cleaned_data["edit"] is True(아니면 우리가 지금 이페이지를 edit하고있는지).
            if util.get_entry(title) == None or form.cleaned_data["edit"] == True:
                util.save_entry(title, content)
                return redirect("entry", title=title)
            else:
                # Else, check the case that this title is already exist
                return render(request, "encyclopedia/add.html", {
                    "existing": True,
                    "form": form,
                    "title": title
                })
        else:
            return render(request, "encyclopedia/add.html", {
                "existing": False,
                "form": form
            })


    return render(request,"encyclopedia/add.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    entryPage = util.get_entry(title)


    if request.method == "POST":
        content = request.POST.get("content")
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': entryPage, 'title': title})

