
from celery import shared_task
#mongo
import pymongo
import json
myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")


@shared_task
def add_info(*args,**kwargs):
    mydb=kwargs['db']
    mycol = kwargs["col"]
    mydb = myclient[mydb]
    mycol = mydb[mycol]
    info=json.loads(kwargs['info'])

    mycol.insert_one(info)


