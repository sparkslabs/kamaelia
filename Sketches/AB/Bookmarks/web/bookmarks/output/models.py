from django.db import models

# Create your models here.

# IMPORTANT: Use the schema provided and not this to generate the database. Default values and utf8 for the rawdata.text field don't work
    
class programmes(models.Model):
    pid = models.CharField(max_length=10,primary_key=True,db_column="pid")
    channel = models.CharField(max_length=20,db_column="channel")
    title = models.CharField(max_length=200,db_column="title")
    expectedstart = models.CharField(max_length=100,db_column="expectedstart")
    timediff = models.IntegerField(db_column="timediff",default=0)
    duration = models.IntegerField(db_column="duration",default=0)
    imported = models.BooleanField(db_column="imported",default=0)
    analysed = models.BooleanField(db_column="analysed",default=0)
    totaltweets = models.IntegerField(db_column="totaltweets",default=0)
    meantweets = models.FloatField(db_column="meantweets",default=0)
    mediantweets = models.IntegerField(db_column="mediantweets",default=0)
    modetweets = models.IntegerField(db_column="modetweets",default=0)
    stdevtweets = models.FloatField(db_column="stdevtweets",default=0)

    class Meta:
        db_table = 'programmes'

class analyseddata(models.Model):
    did = models.IntegerField(primary_key=True,db_column="did")
    pid = models.ForeignKey(programmes,db_column="pid")
    datetime = models.CharField(max_length=100,db_column="datetime")
    wordfreqexpected = models.CharField(max_length=500,db_column="wordfreqexpected")
    wordfrequnexpected = models.CharField(max_length=500,db_column="wordfrequnexpected")
    totaltweets = models.IntegerField(db_column="totaltweets",default=0)

    class Meta:
        db_table = 'analyseddata'

class keywords(models.Model):
    uid = models.IntegerField(primary_key=True,db_column="uid")
    pid = models.ForeignKey(programmes,db_column="pid")
    keyword = models.CharField(max_length=200,db_column="keyword")
    type = models.CharField(max_length=100,db_column="type")

    class Meta:
        db_table = 'keywords'

class rawdata(models.Model):
    tid = models.IntegerField(primary_key=True,db_column="tid")
    pid = models.ForeignKey(programmes,db_column="pid")
    datetime = models.CharField(max_length=100,db_column="datetime")
    text = models.CharField(max_length=200,db_column="text")
    user = models.CharField(max_length=200,db_column="user")
    analysed = models.BooleanField(db_column="analysed",default=0)

    class Meta:
        db_table = 'rawdata'