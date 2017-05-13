from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import subprocess
from search.utils import valid_image_mimetype
import json
from Ranker.ranker import Ranker
import time


def index(request):
    return render(request, 'index.html',
                  {
                      'github_repo': ""
                  })


def process_query(request):
    if request.method == 'POST' and request.POST['query']:
        start = time.time()
        print('searching')
        id2word_file = "Ranker/results/results_wordids.txt.bz2"
        corpus = "Ranker/results/results_tfidf.mm"
        model = "Ranker/lda_model/lda.model"
        rank = Ranker(_id2word_path=id2word_file, corpus_path=corpus, model_path=model)
        obj = rank.search(request.POST['query'])
        num_res = len(obj)
        req_time = (time.time() - start)
        print('search finished')
        return render(request, 'search_results.html',
                      {
                          'num_res': num_res,
                          'req_time': req_time,
                          'query': request.POST['query'],
                          'links': obj
                      })
    return redirect(index)


def process_image(request):
    if request.method == 'POST' and request.FILES['image']:
        img = request.FILES['image']

        if not valid_image_mimetype(img):
            return redirect(index)

        fs = FileSystemStorage()
        filename = fs.save(img.name, img)

        uploaded_file_url = fs.url(filename)

        print('starting image captioning')

        cmd = ['th ~/KokoSearch/kneuraltalk2-master/eval.lua -model model_id1-501-1448236541.t7_cpu.t7 -image_folder ~/KokoSearch/imgs -num_images 10 -gpuid -1']
        subprocess.Popen(cmd).wait()

        print('finished image captioning')

        fs.delete(filename)

        with open('ImageToTopic/vis/vis.json') as data_file:
            data = json.load(data_file)

        query = str(data[0]['caption'])
        start = time.time()
        print('searching with image')
        id2word_file = "Ranker/results/results_wordids.txt.bz2"
        corpus = "Ranker/results/results_tfidf.mm"
        model = "Ranker/lda_model/lda.model"
        rank = Ranker(_id2word_path=id2word_file, corpus_path=corpus, model_path=model)
        obj = rank.search(query)
        num_res = len(obj)
        req_time = (time.time() - start)
        print('search finished with image')
        return render(request, 'search_results.html',
                      {
                          'num_res': num_res,
                          'req_time': req_time,
                          'query': query,
                          'links': obj
                      })

    return redirect(index)
