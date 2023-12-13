
from django.db import models


class OtherProjectModel(models.Model):
    # Your fields go here

    class Meta:
        app_label = 'texeclientapp'
        db_table = 'orders'

