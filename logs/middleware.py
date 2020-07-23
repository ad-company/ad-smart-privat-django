from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class SettingsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            host = request.META['HTTP_HOST']
            if host == '0.0.0.0':
                print(host, 'HOST')
                settings.DEBUG = True
            # else:
        except AttributeError:
            pass

# class SettingsMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def process_request(self, request):
#         try:
#             host = request.META['HTTP_HOST']
#             if host == '0.0.0.0':
#                 print(host, 'HOST')
#                 settings.DEBUG = False
#             # else:
#         except AttributeError:
#             pass
