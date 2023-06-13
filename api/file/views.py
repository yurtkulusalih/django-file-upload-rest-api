from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer

from file.models import File
from file.serializers import FileUploadSerializer, OneRandomLineSerializer, OneRandomLineBackwardSerializer, LongestHundredLinesSerializer, LongestTwentyLinesSerializer
from core.renderer import PlainTextRenderer


class FileViewSet(viewsets.GenericViewSet):
    queryset = File.objects.all().order_by("-created")
    parser_classes = [MultiPartParser, FormParser]
    renderer_classes = [JSONRenderer]
    pagination_class = None

    @action(methods=['post'], detail=False, url_name='upload', serializer_class=FileUploadSerializer)
    def upload(self, request, *args, **kwargs):
        serializer: FileUploadSerializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path='random-line', url_name='random-line', serializer_class=OneRandomLineSerializer,
            renderer_classes=[JSONRenderer, XMLRenderer, PlainTextRenderer])
    def get_random_line(self, request, *args, **kwargs):
        valid_accept_headers = ['application/xml',
                                'application/json', 'text/plain']
        accept_header = request.headers.get('Accept', 'invalid')

        if accept_header not in valid_accept_headers:
            return Response({'detail': f'Please provide one of these accept headers: {valid_accept_headers}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        queryset = self.get_queryset()
        # Get the latest uploaded file
        instance = queryset.first()
        serializer = self.get_serializer(
            instance=instance, accept_header=accept_header)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='random-line-backwards', url_name='random-line-backwards-list',
            serializer_class=OneRandomLineBackwardSerializer)
    def get_random_line_backwards_list(self, request, *args, **kwargs):
        # No pagination for now
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='longest-hundred-lines', url_name='longest-hundred-lines',
            serializer_class=LongestHundredLinesSerializer)
    def get_longest_hundred_lines(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='longest-twenty-lines', url_name='longest-twenty-lines',
            serializer_class=LongestTwentyLinesSerializer)
    def get_longest_twenty_lines(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Get the latest uploaded file
        instance = queryset.first()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
