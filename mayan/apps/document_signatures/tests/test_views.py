from __future__ import absolute_import, unicode_literals

from django.core.files import File

from django_gpg.models import Key
from documents.permissions import permission_document_view
from documents.tests.literals import TEST_DOCUMENT_PATH
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import (
    TEST_USER_USERNAME, TEST_USER_PASSWORD
)

from ..models import DetachedSignature
from ..permissions import (
    permission_document_version_signature_view,
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
)

from .literals import (
    TEST_SIGNED_DOCUMENT_PATH, TEST_SIGNATURE_FILE_PATH, TEST_KEY_FILE,
    TEST_KEY_ID, TEST_SIGNATURE_ID
)


class SignaturesViewTestCase(GenericDocumentViewTestCase):
    def test_signature_list_view_no_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get(
            'signatures:document_version_signature_list',
            args=(document.latest_version.pk,)
        )

        self.assertContains(response, 'Total: 0', status_code=200)

    def test_signature_list_view_with_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_document_version_signature_view.stored_permission
        )

        response = self.get(
            'signatures:document_version_signature_list',
            args=(document.latest_version.pk,)
        )

        self.assertContains(response, 'Total: 1', status_code=200)

    def test_signature_detail_view_no_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get(
            'signatures:document_version_signature_details',
            args=(signature.pk,)
        )

        self.assertEqual(response.status_code, 403)

    def test_signature_detail_view_with_permission(self):
        with open(TEST_KEY_FILE) as file_object:
            Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            signature = DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_document_version_signature_view.stored_permission
        )

        response = self.get(
            'signatures:document_version_signature_details',
            args=(signature.pk,)
        )

        self.assertContains(response, signature.signature_id, status_code=200)
