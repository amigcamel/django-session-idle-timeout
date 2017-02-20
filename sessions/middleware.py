"""A middleware used to log out users after a period of time."""
import datetime
from distutils.version import StrictVersion

import django
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings


if StrictVersion(django.get_version()) >= StrictVersion('1.10'):
    from django.utils.deprecation import MiddlewareMixin
else:
    MiddlewareMixin = object


class SessionIdleTimeout(MiddlewareMixin):
    """Middleware class to timeout a session after a specified time period."""

    def process_request(self, request):
        """Timeout is done only for authenticated logged in users."""
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()

            # Timeout if idle time period is exceeded.
            last_activity = request.session.get('last_activity')
            if (
                last_activity and
                (current_datetime - last_activity).seconds >
                settings.SESSION_IDLE_TIMEOUT
            ):
                logout(request)
                messages.add_message(
                    request, messages.ERROR, 'Your session has been timed out.'
                )
            # Set last activity time in current session.
            else:
                request.session['last_activity'] = current_datetime
        return None
