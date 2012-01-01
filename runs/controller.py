import commands
import random
from django.conf import settings
from django.core.mail import send_mail
from runs.models import *

def sendmail(address, jobid):
    send_mail('Your calculation is ready', 
       'Your calculation is ready, <a href="'+settings.URL_ROOT+str(jobid)+'">see it here</a>', 'powerful@example.com',
        [address], fail_silently=True)

def dostuff(filename1, filename2, jobid):
    directory = settings.MEDIA_ROOT
    pdb = directory+filename1
    ref = directory+filename2
    out = commands.getoutput("python2 %s/FlexServ/analyze_ENM.py --pdb %s --ref %s" % (settings.PROJECT_ROOT, pdb, ref))
    out = str(out.split()[1:])
    commands.getoutput("mv paper_fig.tga static/files/%s.tga" % jobid)
    commands.getoutput("mv state_paper.vmd static/files/%s.vmd" % jobid)
    commands.getoutput("mv paper_fig_ener.png static/files/%s.png" % jobid)
    #cleanup
    commands.getoutput("rm AAcolor_pdb.pdb AAcolor_ref.pdb color_pdb.pdb color_ref.pdb")
    return out

def savejob(request):
    form = EntryForm(request.POST, request.FILES)
    rand = random.randint(1,2147483647)
    form.data.update({'jobid':str(rand)})
    if form.is_valid():
        form.save()
    return form
