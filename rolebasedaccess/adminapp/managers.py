from django.db import models

class ActiveProductManager(models.Manager):
    def active(self):
        return list(self.filter(status=True).values())

    