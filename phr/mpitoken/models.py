import uuid

from django.db import models

from phr.mpitoken.validators import validate_ip


class AuthToken(models.Model):
    app_identifier = models.CharField(max_length=50)
    app_name = models.CharField(max_length=250)
    token = models.CharField(max_length=32, editable=False)
    allowed_ips = models.TextField(validators=[validate_ip], help_text='Lista de IPs permitidas, separadas por comas.')

    def __str__(self):
        return "{} - {}".format(self.app_identifier, self.token)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        self.allowed_ips = self.allowed_ips.replace(' ', '').replace('\n', '').replace('\r', '')
        return super().save(*args, **kwargs)
