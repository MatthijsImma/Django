from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.views import generic

import redis, json, urllib, urllib2

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def index(request):
    
    jokes = ''
       
    joke = {}
    fn = ''
    ln = ''
    url = 'http://api.icndb.com/jokes/random?firstName=John&lastName=Doe'

    if request.GET.get('FirstName'): 
        if request.GET.get('LastName'): 
            fn = request.GET['FirstName']
            ln = request.GET['LastName']
            url = 'http://api.icndb.com/jokes/random?firstName={}&lastName={}'.format(fn,ln)

    response = urllib2.urlopen(url)

    joke = json.load(response)
    if (joke['type'] != 'success'):
        joke = {}
        joke['joke'] = 'Joke not found'
        joke['categories'] ='operation failed'
    else:
        jokejson = joke['value']
        joke_id = jokejson['id']
        if (r.get(joke_id) is None):
            r.set(joke_id, json.dumps(joke['value']))
            joke = json.loads(r.get(joke_id))
        else:
            joke = json.loads(r.get(joke_id))

    return render(request,'jokes/index.html',{'jokes':joke['joke']})


