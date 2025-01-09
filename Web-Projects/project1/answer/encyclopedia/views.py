from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
from random import randint

# Django 시작할때 해야될거
# python manage.py makemigrations
# python manage.py migrate
# 그리고 아래 두줄을 메인이 되주는 settings.py 맨 아래에 복붙시켜줄것
# CORS_ORIGIN_WHITELIST = ['https://justlikethat17-code50-103625235-5gp5gv7qwf4wrw-8000.githubpreview.dev']
# CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    # wiki/HTML 같이 존재하는 entryPage가 아니라 wiki/xddd 이렇게 존재하지 않는것을 대상으로 하면 'Page not Found' 라는 화면을 보여줘야함
    content = util.get_entry(title.strip())
    if content == None:
        content = "## Page was not found"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content, 'title': title})


def search(request):
    # GET.get 사용법 https://stackoverflow.com/questions/44598962/what-does-request-get-get-mean
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})


def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_title)


def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/add.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html", {"message": "Title already exist. Try another.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/add.html")


def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})
