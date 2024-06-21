from rest_framework.throttling import SimpleRateThrottle

class BurstRateThrottle(SimpleRateThrottle):
    scope = 'burst'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
            
        else:
            ident = self.get_ident(request)
            print(ident,'sssssss')

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }