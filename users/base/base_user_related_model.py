from django.db import models

from core.base.base_model import BaseModel
from users.models import UserModel


class UserOptionalBaseModel(BaseModel):
    user = models.ForeignKey(
        UserModel, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta(BaseModel.Meta):
        abstract = True


class UserRequiredBaseModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        abstract = True
