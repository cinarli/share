

# Create your tasks here


from celery import shared_task,Celery
#mongo
import pymongo
import json
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")


from .models import MyFile
@shared_task
def my_first_task(*args,**kwargs):
    FormId=kwargs['FormId']
    try:
        Form=MyFile.objects.get(id=FormId)
        Form.delete()
    except:
        return False