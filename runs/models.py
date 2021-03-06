from django.db import models
from django.forms import ModelForm
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename

# Create your models here.
class Entry(models.Model):
    submitter = models.CharField("Name", max_length=200, blank=False)
    email = models.EmailField("Email", blank=False) #max length 75
    pdb = models.FileField("pdb", upload_to=get_file_path, blank=False)
    ref = models.FileField("ref", upload_to=get_file_path, blank=False)
    name = models.CharField("Protein Name", max_length=200, blank=True)
    description = models.CharField("Description", max_length=200, blank=True)
    jobid = models.PositiveIntegerField(primary_key=True)
    time  = models.DateTimeField("Time", auto_now_add=True)
    done = models.BooleanField(editable=False,default=False)
    public = models.BooleanField(editable=True,default=True)

class Out(models.Model):
    jobid = models.ForeignKey(Entry)
    pdb_filename = models.CharField(max_length=255,editable=False,blank=True)
    ref_filename = models.CharField(max_length=255,editable=False,blank=True)
    rmsdED = models.FloatField(default=-1)
    Forw = models.FloatField(default=-1)
    Back = models.FloatField(default=-1)
class EntryForm(ModelForm):
    class Meta:
        model = Entry
