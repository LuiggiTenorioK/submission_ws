# Dependencies
import logging

from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle

from submission.models import Group, get_anon_user_throttle

logger = logging.getLogger(__name__)

class IPRateThrottleBurst(AnonRateThrottle):
    scope = 'ipBurst'
    THROTTLE_RATES = {'ipBurst': '10/s'}

    ident = None

    def get_cache_key(self, request, view):
        if request.user is not None:
            return None  # Only throttle unauthenticated requests.

        anon_throttle = get_anon_user_throttle()

        self.num_requests, self.duration = self.parse_rate(anon_throttle.throttling_rate_burst)

        self.ident = self.get_ident(request)

        return self.cache_format % {
                'scope': self.scope,
                'ident': self.ident
        }

    def throttle_failure(self):
        logger.warning('Request was throttled', extra={'ip': self.ident})


class IPRateThrottleSustained(AnonRateThrottle):
    scope = 'ipSustained'
    THROTTLE_RATES = {'ipSustained': '100/d'}

    ident = None

    def get_cache_key(self, request, view):
        if request.user is not None:
            return None  # Only throttle unauthenticated requests.

        anon_throttle = get_anon_user_throttle()

        self.num_requests, self.duration = self.parse_rate(anon_throttle.throttling_rate_sustained)

        self.ident = self.get_ident(request)

        return self.cache_format % {
                'scope': self.scope,
                'ident': self.ident
        }

    def throttle_failure(self):
        logger.warning('Request was throttled', extra={'ip': self.ident})


class UserBasedThrottleBurst(SimpleRateThrottle):
    scope = 'userBurst'
    THROTTLE_RATES = {'userBurst': '5/s'}

    ident = None

    def get_cache_key(self, request, view):
        if request.user is not None and request.user.is_authenticated:
            self.num_requests, self.duration = self.parse_rate(request.user.throttling_rate_burst)
            pk = request.user.pk
            self.ident = request.user.username
        else:
            return None

        return self.cache_format % {
                'scope': self.scope,
                'ident': pk
        }

    def throttle_failure(self):
        logger.warning('Request was throttled', extra={'ip': self.ident})


class UserBasedThrottleSustained(SimpleRateThrottle):
    scope = 'userSustained'
    THROTTLE_RATES = {'userSustained': '1000/d'}

    ident = None

    def get_cache_key(self, request, view):
        if request.user is not None and request.user.is_authenticated:
            self.num_requests, self.duration = self.parse_rate(request.user.throttling_rate_sustained)
            pk = request.user.pk
            self.ident = request.user.username
        else:
            return None

        return self.cache_format % {
                'scope': self.scope,
                'ident': pk
        }

    def throttle_failure(self):
        logger.warning('Request was throttled', extra={'ip': self.ident})
