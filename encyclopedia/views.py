from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint
from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def enterys(request, entery):
    entery_data = util.get_entry(entery)
    
    markdowner = Markdown()
    if entery_data :
        html =  markdowner.convert(entery_data)
        return render(
            request,
            "encyclopedia/entery.html",
            {
                "entery": html,
                "title": entery,
            },  )
    else:
        return render(
            request, "encyclopedia/error.html", {"error": "  ‘Oops, page not found!’."} )


def serarchs(request):
    if request.method == "POST":
        q = request.POST["q"]
        if q:
            topic_lest = util.list_entries()
            q.lower()
            list_iteam = [i for i in topic_lest if q.lower() in i.lower()]

            if len(list_iteam) == 0:
                return render(
                    request, "encyclopedia/error.html", {"error": " No such topic."}
                )

            elif len(list_iteam) == 1:
                return HttpResponseRedirect(
                    reverse("wiki", kwargs={"entery": list_iteam[0]})
                )
            else:
                return render(
                    request, "encyclopedia/index.html", {"entries": list_iteam}
                )
        else:
            return render(request, "encyclopedia/error.html", {"error": " No such topic."})
    else:
        return render(request, "encyclopedia/error.html", {"error": " No such topic."})


def new_pages(request):
    topic_lest = util.list_entries()
    if request.method == "POST":
        title = request.POST["title"]
        topic = request.POST["topic"]
        if title in topic_lest:
            return render(
                request,
                "encyclopedia/newpage.html",
                {"message": " This topic already add ."},
            )
        else:
            util.save_entry(title, topic)
            return render(
                request, "encyclopedia/newpage.html", {"message": "Add secusses"}
            )
    else:
        return render(
            request,
            "encyclopedia/newpage.html",
        )


def edit_pages(request, entery):
    edit_data = util.get_entry(entery)
    if request.method == "POST":
        title = request.POST["title"]
        topic = request.POST["topic"]
        util.save_entry(title, topic)
        redirect = reverse("wiki", kwargs={"entery": title})
        return HttpResponseRedirect(redirect)
    else:
        return render(  request, "encyclopedia/edit.html", {"title": entery, "entery": edit_data} )


def randomq(request):
    topic_lest = util.list_entries()
    value = randint(0, len(topic_lest) - 1)
    
    return HttpResponseRedirect(   reverse("wiki", kwargs={"entery": topic_lest[value]}) )
