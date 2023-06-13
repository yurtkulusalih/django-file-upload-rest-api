import os
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from core.renderer import PlainTextRenderer
from file.models import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import Client

from file.serializers import FileUploadSerializer, OneRandomLineSerializer

test_upload_file_path = settings.TEST_UPLOAD_FILE_PATH
test_populate_file_path = settings.TEST_POPULATE_FILE_PATH


class FileTests(APITestCase):
    json_renderer = JSONRenderer()
    xml_renderer = XMLRenderer()
    plain_text_renderer = PlainTextRenderer()

    longest_among_all_str = "I am the latest upload with the longest line and this line should be the first element of longest-line-enpoints"

    @classmethod
    def setUpTestData(cls) -> None:
        print(f"Populating db with existing files...")
        try:
            files = [cls._prepare_file_for_upload("test1.txt", upload=False), cls._prepare_file_for_upload(
                "test2.txt", upload=False), cls._prepare_file_for_upload("test3.txt", upload=False)]
            for file in files:
                cls._populate_db(file_obj=file)

            print(f"Operation successful!!")
        except Exception as e:
            raise e

    @staticmethod
    def _populate_db(file_obj: SimpleUploadedFile):
        serializer = FileUploadSerializer(data={"content": file_obj})
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @staticmethod
    def _prepare_file_for_upload(filename: str, content_type: str = 'text/plain', upload: bool = True) -> SimpleUploadedFile:
        file_path = test_upload_file_path if upload else test_populate_file_path

        wrapper_obj = open(os.path.join(file_path, filename), mode="rb")
        content = wrapper_obj.read()
        wrapper_obj.close()
        return SimpleUploadedFile(name=filename, content=content, content_type=content_type)

    def test_file_upload_success(self):
        file_obj = self._prepare_file_for_upload("test.txt")
        url = reverse('file-upload')
        response: Response = self.client.post(url, data={"content": file_obj})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # then delete the file
        latest_file_obj = File.objects.all().order_by('-created').first()
        latest_file_obj.content.delete()
        latest_file_obj.delete()

    def test_file_upload_not_txt(self):
        file_obj = self._prepare_file_for_upload('image.jpeg')
        url = reverse('file-upload')
        response: Response = self.client.post(url, data={"content": file_obj})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_file_upload_txt_but_content_different(self):
        file_obj = self._prepare_file_for_upload('image.txt')
        url = reverse('file-upload')
        response: Response = self.client.post(url, data={"content": file_obj})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_random_line(self):
        url = reverse('file-random-line')

        response_json: Response = self.client.get(
            url, HTTP_ACCEPT='application/json')

        response_xml: Response = self.client.get(
            url, HTTP_ACCEPT='application/xml')

        response_plain: Response = self.client.get(
            url, HTTP_ACCEPT='text/plain')

        # TODO: Normally, contents and content-types should also be compared but due to time constraints I skip that part.
        # Just compare the http status
        self.assertEqual(response_json.status_code, status.HTTP_200_OK)
        self.assertEqual(response_xml.status_code, status.HTTP_200_OK)
        self.assertEqual(response_plain.status_code, status.HTTP_200_OK)

    def test_random_line_invalid_header(self):
        url = reverse('file-random-line')

        response_invalid: Response = self.client.get(url)

        self.assertEqual(response_invalid.status_code,
                         status.HTTP_406_NOT_ACCEPTABLE)

    def test_random_line_backwards(self):
        url = reverse('file-random-line-backwards-list')
        # we upload 3 .txt files, therefore length of the expected result should be 3
        expected_len = 3
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_len)

    def test_hundred_longest_lines(self):
        # The total number of lines in test*.txt files ==> 118 lines in total, each file containing 36 lines
        url = reverse('file-longest-hundred-lines')
        expected_len = 100

        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data['longest_hundred_lines']
        self.assertTrue(isinstance(response_data, list))
        self.assertEqual(expected_len, len(response_data))
        self.assertEqual(self.longest_among_all_str, response_data[0])

    def test_twenty_longest_lines(self):
        # The total number of lines in the test3.txt more than 20 ==> 36 lines
        url = reverse('file-longest-twenty-lines')
        expected_len = 20

        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data['longest_twenty_lines']
        self.assertTrue(isinstance(response_data, list))
        self.assertEqual(expected_len, len(response_data))
        self.assertEqual(self.longest_among_all_str, response_data[0])

    @classmethod
    def tearDownClass(cls) -> None:
        file_objs = File.objects.all()
        for file in file_objs:
            # first, delete the file from disk
            file.content.delete()
            # then delete the db record
            file.delete()

        super().tearDownClass()
