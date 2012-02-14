from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from runs.views import *
from runs.models import Entry

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'runs.views.index'),
    url(r'^add$', 'runs.views.add'),
    #url(r'^process$', 'runs.views.process'),
    
    url(r'^queue/page(?P<page>[0-9]+)/$', 
        ListView.as_view(
           queryset=Entry.objects.order_by("-time"),
           model=Entry,
           paginate_by = 10,
           template_name='runs/templates/recentsubmission.html'),
        ),
    url(r'^result/(\d+)/$', 
        ResultListView.as_view()),
    url(r'^view/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Out,
            template_name='runs/templates/view.html'),
        ),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
