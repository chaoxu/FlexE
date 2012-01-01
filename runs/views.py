from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from runs.models import *
from runs.controller import *
from django.template import RequestContext
import pprint

def index(request):
    return add(request)

def add(request):
    #Result success or fail
    if request.method == 'POST':
        form = savejob(request)
        if form.is_valid():
            return render_to_response("added.html")
        else:
            return render_to_response("addfail.html")
    else: #Create posting form
        form = EntryForm()
        csrfContext = RequestContext(request)
        return render_to_response("add.html", {'form':form}, csrfContext)

def process(request):
    #Get some program to keep open this file
    #pick most recent unfinished job
    jobs = Entry.objects.filter(done=False).order_by( 'time' )[:1]
    if (len(jobs) > 0):
        job = jobs[0]
        #run process
        job.result = dostuff(str(job.pdb), str(job.ref), str(job.jobid))
        #send an email
        sendmail(job.email, job.jobid) 
        job.done = True
        #save job
        job.save()
    return HttpResponse("Done")
