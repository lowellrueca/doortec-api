from tortoise import fields
from tortoise.models import Model


class AbstractBaseModel(Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class AbstractBaseProductModel(AbstractBaseModel):
    series = fields.CharField(max_length=64)
    price = fields.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        abstract = True


class Door(AbstractBaseProductModel):
    class Meta:
        table = "door"


__models__ = [Door]
