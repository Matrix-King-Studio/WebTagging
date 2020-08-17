from rest_framework import serializers


class DatasetFormatSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64, source='DISPLAY_NAME')
    ext = serializers.CharField(max_length=64, source='EXT')
    version = serializers.CharField(max_length=64, source='VERSION')


class DatasetFormatsSerializer(serializers.Serializer):
    importers = DatasetFormatSerializer(many=True)
    exporters = DatasetFormatSerializer(many=True)
