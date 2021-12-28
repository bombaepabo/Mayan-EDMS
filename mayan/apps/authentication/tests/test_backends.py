from furl import furl

from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlunquote_plus

from mayan.apps.smart_settings.classes import SettingNamespace
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..classes import AuthenticationBackend

from .literals import TEST_EMAIL_AUTHENTICATION_BACKEND
from .mixins import LoginViewTestMixin


class AuthenticationBackendTestCase(LoginViewTestMixin, GenericViewTestCase):
    authenticated_url = reverse(viewname='common:home')
    authentication_url = urlunquote_plus(
        furl(
            path=reverse(settings.LOGIN_URL), args={
                'next': authenticated_url
            }
        ).tostr()
    )
    auto_login_user = False
    create_test_case_superuser = True

    def setUp(self):
        super().setUp()
        SettingNamespace.invalidate_cache_all()

    @override_settings(AUTHENTICATION_BACKEND=TEST_EMAIL_AUTHENTICATION_BACKEND)
    def test_email_authentication_backend(self):
        backend = AuthenticationBackend.get_instance()

        logged_in = backend.login(
            email=self._test_case_superuser.email,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertTrue(logged_in)

        self._clear_events()

        response = self._request_authenticated_view()
        # We didn't get redirected to the login URL.
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_username_authentication_backend(self):
        backend = AuthenticationBackend.get_instance()

        logged_in = backend.login(
            username=self._test_case_superuser.username,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertTrue(logged_in)

        self._clear_events()

        response = self._request_authenticated_view()
        # We didn't get redirected to the login URL.
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)