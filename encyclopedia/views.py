from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint
from . import util
from markdown2 import Markdown


def index(request):
    # index page will return a list of all entries title
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def enterys(request, entery):
    # get file from entries 
    entery_data = util.get_entry(entery)
  
    markdowner = Markdown()
    #  view not null file 
    if entery_data and entery:
        # transfer MD file to Html element
        html = markdowner.convert(entery_data)
        return render(  request, "encyclopedia/entery.html",     {  "entery": html,"title": entery, },  )
    #  if  null file 
    elif entery and   entery in  util.list_entries() :
         null =f"{entery} <p>This page is null you can add more details <p>"
         return render(  request, "encyclopedia/entery.html",     {  "entery": null,"title": entery, },  )
    else:
        #    redirect to error page if not find  any file 
        return render(      request, "encyclopedia/error.html", {"error": "  ‘Oops, page not found!’."}  )


def serarchs(request):
    if request.method == "POST":
        q = request.POST["q"]
        if q:
            # select all entries 
            topic_lest = util.list_entries()
            #  search in the list then find if any result like search entry and return a list from results
            list_iteam = [i for i in topic_lest if q.lower() in i.lower()]
            # if no result 
            if len(list_iteam) == 0:
                return render(        request, "encyclopedia/error.html", {"error": "No such topic."}     )
            # if one result same search entry
            elif len(list_iteam) == 1 and list_iteam[0].lower() == q.lower():
                return HttpResponseRedirect(       reverse("wiki", kwargs={"entery": list_iteam[0]})    )

            else:
                # if muny result
                return render( request, "encyclopedia/search.html", {"entries": list_iteam}  )
        else:
            # if null search from post
            return render(     request, "encyclopedia/error.html", {"error": " Your search was unsuccessful."}  )
    else:
        #  if null search from git 
        return render(request, "encyclopedia/error.html", {"error": " Your search was unsuccessful."})


def new_pages(request):
    # add new entery
    if request.method == "POST":
        title = request.POST["title"]
        topic = request.POST["topic"]
        #   confirm title and topic
        if not title or  not topic :
            return render(    request,  "encyclopedia/newpage.html", {"error": "Title and  Subject are required ."},  )

        # confirm this title not duplicate
        print(title.title())
        print( util.list_entries())
        print(  title.lower())
        if  title.title() in  util.list_entries():
            return render(     request,    "encyclopedia/newpage.html",    {"error": " This topic already add ."},    )
        else:
            title=title.title()
            util.save_entry(title, topic)
            message=f'{title} : Add secusses <a href="/wiki/{title}"> view</a>'
            return render(  request, "encyclopedia/newpage.html", {"message": message}   )
            

    else:
        return render(     request,     "encyclopedia/newpage.html",    )


def edit_pages(request, entery):
    # get topic from entry  topics 
    edit_data = util.get_entry(entery)
    
    if request.method == "POST":
        # confirm title and topic
        title = request.POST["title"]
        topic = request.POST["topic"]
        if not title or  not topic :
            return render( request,  "encyclopedia/edit.html", {"error": "Title and  Subject are required ." ,"title": entery, "entery": edit_data},  )
        #  Update file  
        util.save_entry(title, topic)
        # redirect to entery page 
        return HttpResponseRedirect(reverse("wiki", kwargs={"entery": title}))
    else:
        return render(   request, "encyclopedia/edit.html", {"title": entery, "entery": edit_data}  )

# random function will return one index  from of all entries
def randomq(request):
    topic_lest = util.list_entries()
    value = randint(0, len(topic_lest) - 1)
    return HttpResponseRedirect(reverse("wiki", kwargs={"entery": topic_lest[value]}))
