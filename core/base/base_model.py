from bson import objectid
from django.db import models


def make_object_id():
    return str(objectid.ObjectId())


class BaseModel(models.Model):
    uid = models.CharField(default=make_object_id, db_index=True, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-uid"]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return self.uid
