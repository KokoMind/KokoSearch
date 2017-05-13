from django.shortcuts import render
from django.http import HttpResponse
# from scipy import misc


# Create your views here.


def index(request):
    return render(request, 'index.html',
                  {
                      'github_repo': ""
                  })


def process_query(request):
    return HttpResponse("Search")


def process_image(request):
    return HttpResponse("Search by image")


def results(request):
    num_res = 100
    req_time = 1.2
    query = "ElFr5a betr2os m3 dek roomy"

    class Obj:
        pass

    objs = []

    for i in range(100):
        ob = Obj()
        ob.link = "facebook.com"
        ob.text = "Bootdey is a gallery of free snippets resources templates and utilities for bootstrap css hmtl js framework. Codes for developers and web designers"
        objs.append(ob)

    return render(request, 'search_results.html',
                  {
                      'num_res': num_res,
                      'req_time': req_time,
                      'query': query,
                      'links': objs
                  })
