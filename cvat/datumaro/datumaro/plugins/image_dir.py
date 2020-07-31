
# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: MIT

from collections import OrderedDict
import os
import os.path as osp

from datumaro.components.extractor import DatasetItem, SourceExtractor, Importer
from datumaro.components.converter import Converter
from datumaro.util.image import save_image


class ImageDirImporter(Importer):
    EXTRACTOR_NAME = 'image_dir'

    def __call__(self, path, **extra_params):
        from datumaro.components.project import Project # cyclic import
        project = Project()

        if not osp.isdir(path):
            raise Exception("Can't find a directory at '%s'" % path)

        source_name = osp.basename(osp.normpath(path))
        project.add_source(source_name, {
            'url': source_name,
            'format': self.EXTRACTOR_NAME,
            'options': dict(extra_params),
        })

        return project


class ImageDirExtractor(SourceExtractor):
    _SUPPORTED_FORMATS = ['.png', '.jpg']

    def __init__(self, url):
        super().__init__()

        assert osp.isdir(url), url

        items = []
        for name in os.listdir(url):
            path = osp.join(url, name)
            if self._is_image(path):
                item_id = osp.splitext(name)[0]
                item = DatasetItem(id=item_id, image=path)
                items.append((item.id, item))

        items = sorted(items, key=lambda e: e[0])
        items = OrderedDict(items)
        self._items = items

    def __iter__(self):
        for item in self._items.values():
            yield item

    def __len__(self):
        return len(self._items)

    def get(self, item_id, subset=None, path=None):
        if path or subset:
            raise KeyError()
        return self._items[item_id]

    def _is_image(self, path):
        for ext in self._SUPPORTED_FORMATS:
            if osp.isfile(path) and path.endswith(ext):
                return True
        return False


class ImageDirConverter(Converter):
    def __call__(self, extractor, save_dir):
        os.makedirs(save_dir, exist_ok=True)

        for item in extractor:
            if item.has_image and item.image.has_data:
                filename = item.image.filename
                if filename:
                    filename = osp.splitext(filename)[0]
                else:
                    filename = item.id
                filename += '.jpg'
                save_image(osp.join(save_dir, filename), item.image.data)