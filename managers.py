from django.db import models

class StatusManager(models.Manager):
    def get_query_set(self):
        return super(StatusManager, self).get_query_set().filter(status=self.model.OPEN_STATUS)