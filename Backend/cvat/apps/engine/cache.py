import os
from io import BytesIO

from diskcache import Cache
from django.conf import settings

from cvat.apps.engine.prepare import PrepareInfo
from cvat.apps.engine.models import DataChoice, StorageChoice
from cvat.apps.engine.media_extractors import ZipChunkWriter, ZipCompressedChunkWriter
from cvat.apps.engine.media_extractors import Mpeg4ChunkWriter, Mpeg4CompressedChunkWriter


class CacheInteraction:
    def __init__(self):
        self._cache = Cache(settings.CACHE_ROOT)

    def __del__(self):
        self._cache.close()

    def get_buff_mime(self, chunk_number, quality, db_data):
        chunk, tag = self._cache.get('{}_{}_{}'.format(db_data.id, chunk_number, quality), tag=True)

        if not chunk:
            chunk, tag = self.prepare_chunk_buff(db_data, quality, chunk_number)
            self.save_chunk(db_data.id, chunk_number, quality, chunk, tag)
        return chunk, tag

    def prepare_chunk_buff(self, db_data, quality, chunk_number):
        from cvat.apps.engine.frame_provider import FrameProvider  # TODO: remove circular dependency
        writer_classes = {
            FrameProvider.Quality.COMPRESSED: Mpeg4CompressedChunkWriter if db_data.compressed_chunk_type == DataChoice.VIDEO else ZipCompressedChunkWriter,
            FrameProvider.Quality.ORIGINAL: Mpeg4ChunkWriter if db_data.original_chunk_type == DataChoice.VIDEO else ZipChunkWriter,
        }

        image_quality = 100 if writer_classes[quality] in [Mpeg4ChunkWriter, ZipChunkWriter] else db_data.image_quality
        mime_type = 'video/mp4' if writer_classes[quality] in [Mpeg4ChunkWriter,
                                                               Mpeg4CompressedChunkWriter] else 'application/zip'

        writer = writer_classes[quality](image_quality)

        images = []
        buff = BytesIO()
        upload_dir = {
            StorageChoice.LOCAL: db_data.get_upload_dirname(),
            StorageChoice.SHARE: settings.SHARE_ROOT
        }[db_data.storage]
        if os.path.exists(db_data.get_meta_path()):
            source_path = os.path.join(upload_dir, db_data.video.path)
            meta = PrepareInfo(source_path=source_path, meta_path=db_data.get_meta_path())
            for frame in meta.decode_needed_frames(chunk_number, db_data):
                images.append(frame)
            writer.save_as_chunk([(image, source_path, None) for image in images], buff)
        else:
            with open(db_data.get_dummy_chunk_path(chunk_number), 'r') as dummy_file:
                images = [os.path.join(upload_dir, line.strip()) for line in dummy_file]
            writer.save_as_chunk([(image, image, None) for image in images], buff)

        buff.seek(0)
        return buff, mime_type

    def save_chunk(self, db_data_id, chunk_number, quality, buff, mime_type):
        self._cache.set('{}_{}_{}'.format(db_data_id, chunk_number, quality), buff, tag=mime_type)
