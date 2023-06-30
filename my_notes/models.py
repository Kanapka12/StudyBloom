from django.db import models
from django.db.models import ForeignKey
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class Section(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self):
        return self.name


    class MPTTMeta:
        order_insertion_by = ['name']



class Note(MPTTModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    parent = TreeForeignKey(Section, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
