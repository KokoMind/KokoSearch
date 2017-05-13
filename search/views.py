from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import subprocess
from search.utils import valid_image_mimetype
import json

# from scipy import misc




# Create your views here.


def index(request):
    return render(request, 'index.html',
                  {
                      'github_repo': ""
                  })


def process_query(request):
    # id2word_file = "./results/results_wordids.txt.bz2"
    # corpus = "./results/results_tfidf.mm"
    # model = "./lda_model/lda.model"
    # rank = Ranker(_id2word_path=id2word_file, corpus_path=corpus, model_path=model)
    return HttpResponse("Search")


def process_image(request):
    if request.method == 'POST' and request.FILES['image']:
        img = request.FILES['image']

        if not valid_image_mimetype(img):
            return redirect(index)

        fs = FileSystemStorage()
        filename = fs.save(img.name, img)

        uploaded_file_url = fs.url(filename)

        cmd = ['gedit']
        subprocess.Popen(cmd).wait()

        fs.delete(filename)

        with open('ImageToTopic/vis/vis.json') as data_file:
            data = json.load(data_file)

        return HttpResponse("Search by image\n" + str(uploaded_file_url) + "\n" + str(data[0]['caption']))

    return redirect(index)


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
