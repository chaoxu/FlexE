import commands
import random
import tarfile
from django.conf import settings
from django.core.mail import send_mail
from runs.models import *

def sendmail(address, jobid):
    send_mail('Your calculation is ready', 
       'Your calculation is ready, <a href="'+settings.URL_ROOT+'result/'+str(jobid)+'">see it here</a>', 'powerful@example.com',
        [address], fail_silently=True)

def dostuff(pdb, ref, entry):
    os.chdir(settings.MEDIA_ROOT + str(entry.jobid) + '/')
    pdbs = preparefile('pdb', pdb)
    refs = preparefile('ref', ref)
    commands.getoutput("mkdir img")
    commands.getoutput("mkdir vmd")
    for pdb in pdbs:
        for ref in refs:
            rand = random.randint(1,2147483647)
            p = Out(id=rand, jobid=entry, pdb_filename=os.path.basename(pdb), ref_filename=os.path.basename(ref))
            p.save()
            out = commands.getoutput("python2 %s/FlexServ/analyze_ENM.py --pdb %s --ref %s" % (settings.PROJECT_ROOT, pdb, ref))
            out = out.split()[1:]
            try:
                print out
                p.rmsdED = float(out[0])
                p.Forw = float(out[1])
                p.Back = float(out[2])
                p.save()
            except:
                print "Unexpected Error when parsing the result"
            commands.getoutput("mv paper_fig.tga img/%s.tga" % p.id)
            commands.getoutput("mv state_paper.vmd vmd/%s.vmd" % p.id)
            commands.getoutput("mv paper_fig_ener.png img/%s.png" % p.id)
            #cleanup
            commands.getoutput("rm AAcolor_pdb.pdb AAcolor_ref.pdb color_pdb.pdb color_ref.pdb")

def preparefile(dirname, filename):
    a = []
    commands.getoutput("mkdir %s" % dirname)
    if os.path.splitext(filename)[1] == ".pdb":
        a.append(filename)
    elif os.path.splitext(filename)[1] == ".tar":
        tar = tarfile.open(filename)
        for tarinfo in tar:
            a.append(tarinfo.name)
        tar.extractall()
        tar.close()
    return split_multipdb(dirname, a);

def split_multipdb(dirname, files):
    a = []
    for f in files:
        of = open(f,'r')
        i = 0
        outf = None            
        for line in of:
            if 'MODEL' in line:
                outf = open('%s/%s%04d.pdb' % (dirname, os.path.splitext(f)[0], i),'w')
                a.append('%s/%s%04d.pdb' % (dirname, os.path.splitext(f)[0], i))
                continue
            if 'ENDMDL' in line:
                outf.close()
                i += 1
                continue
            if (outf != None):
                outf.write(line)
        if (i == 0):
            commands.getoutput("mv %s %s/%s" % (os.path.basename(f), dirname, os.path.basename(f)))    
            a.append("%s/%s" % (dirname, os.path.basename(f)))
    return a
       

def savejob(request):
    form = EntryForm(request.POST, request.FILES)
    rand = random.randint(1,2147483647)
    form.data.update({'jobid':str(rand)})
    if form.is_valid():
        entry = form.save()
        return entry
    return None

def process(job):
    #Get some program to keep open this file
    #pick most recent unfinished job
    #run process
    os.chdir(settings.MEDIA_ROOT)
    commands.getoutput("mkdir %s" % job.jobid)
    commands.getoutput("mv %s %s/%s" % (str(job.pdb), job.jobid, str(job.pdb)))
    commands.getoutput("mv %s %s/%s" % (str(job.ref), job.jobid, str(job.ref)))
    job.result = dostuff(str(job.pdb), str(job.ref), job)
    #send an email
    sendmail(job.email, job.jobid) 
    job.done = True
    #save job
    job.save()
    
