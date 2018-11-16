import ipaddress

from django.core.exceptions import ValidationError


def validate_ip(value):
    for ip in value.split(','):
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValidationError(
                "{} no es una IP válida".format(ip)
            )
