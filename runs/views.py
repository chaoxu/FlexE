from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from runs.models import *
from runs.controller import *
from django.template import RequestContext
from threading import Thread
import pprint
import commands
from django.views.generic import ListView

class ResultListView(ListView):
    paginate_by = 20
    context_object_name = "result_list"
    template_name = "result_list.html"

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'rmsdED');
        return Out.objects.filter(jobid=self.args[0]).order_by(order_by)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ResultListView, self).get_context_data(**kwargs)
        # Add in the publisher
        entry = Entry.objects.get(jobid=self.args[0])
        context['submitter'] = entry.submitter;
        context['description'] = entry.description;
        context['protein'] = entry.name;
        return context

def index(request):
    return add(request)

def add(request):
    #Result success or fail
    if request.method == 'POST':
        entry = savejob(request)
        if (entry != None):
            t = Thread(target=process, args=(entry,))
            t.start()
            return render_to_response("submission_success.html")
        else:
            return render_to_response("addfail.html")
    else: #Create posting form
        form = EntryForm()
        csrfContext = RequestContext(request)
        return render_to_response("add.html", {'form':form}, csrfContext)


