from django.conf import settings
from django.http.response import JsonResponse

from phr.mpitoken.models import AuthToken


class MPIAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/v1/'):
            auth_token = request.META.get('HTTP_AUTHORIZATION', '')
            try:
                auth_token_type, auth_token_key = auth_token.split(' ')
                if auth_token_type == 'Bearer':
                    auth_token_app = AuthToken.objects.get(token=auth_token_key)
                    remote_addr = request.META.get('REMOTE_ADDR')
                    if settings.RESTRICT_API_BY_IP and remote_addr not in auth_token_app.allowed_ips.split(','):
                        return JsonResponse({'error': 'invalid_request',
                                             'error_description': 'The IP address is not allowed.'},
                                            status=403)
                else:
                    return JsonResponse(
                        {
                            'error': 'invalid_token_type',
                            'error_description': 'The access token type is invalid.'
                        },
                        status=401)
            except AuthToken.DoesNotExist:
                return JsonResponse({'error': 'invalid_token', 'error_description': 'The access token is invalid.'},
                                    status=401)
            except (IndexError, ValueError):
                return JsonResponse({'error': 'invalid_request',
                                     'error_description': 'Authorization header is invalid.'},
                                    status=400)
        response = self.get_response(request)

        return response
