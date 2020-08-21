# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: MIT

from tempfile import TemporaryDirectory

from pyunpack import Archive

import datumaro.components.extractor as datumaro
from cvat.apps.dataset_manager.bindings import (CvatTaskDataExtractor,
    match_frame)
from cvat.apps.dataset_manager.util import make_zip_archive
from datumaro.components.project import Dataset

from .registry import dm_env, exporter, importer


@exporter(name='MOT', ext='ZIP', version='1.1')
def _export(dst_file, task_data, save_images=False):
    extractor = CvatTaskDataExtractor(task_data, include_images=save_images)
    envt = dm_env.transforms
    extractor = extractor.transform(envt.get('id_from_image_name'))
    extractor = Dataset.from_extractors(extractor) # apply lazy transforms
    with TemporaryDirectory() as temp_dir:
        converter = dm_env.make_converter('mot_seq_gt',
            save_images=save_images)
        converter(extractor, save_dir=temp_dir)

        make_zip_archive(temp_dir, dst_file)

@importer(name='MOT', ext='ZIP', version='1.1')
def _import(src_file, task_data):
    with TemporaryDirectory() as tmp_dir:
        Archive(src_file.name).extractall(tmp_dir)

        dataset = dm_env.make_importer('mot_seq')(tmp_dir).make_dataset()

        tracks = {}
        label_cat = dataset.categories()[datumaro.AnnotationType.label]

        for item in dataset:
            item = item.wrap(id=int(item.id) - 1) # NOTE: MOT frames start from 1
            frame_id = match_frame(item, task_data)

            for ann in item.annotations:
                if ann.type != datumaro.AnnotationType.bbox:
                    continue

                track_id = ann.attributes.get('track_id')
                if track_id is None:
                    continue

                shape = task_data.TrackedShape(
                    type='rectangle',
                    points=ann.points,
                    occluded=ann.attributes.get('occluded') == True,
                    outside=False,
                    keyframe=False,
                    z_order=ann.z_order,
                    frame=frame_id,
                    attributes=[],
                )

                # build trajectories as lists of shapes in track dict
                if track_id not in tracks:
                    tracks[track_id] = task_data.Track(
                        label_cat.items[ann.label].name, 0, [])
                tracks[track_id].shapes.append(shape)

        for track in tracks.values():
            # MOT annotations do not require frames to be ordered
            track.shapes.sort(key=lambda t: t.frame)
            # Set outside=True for the last shape in a track to finish the track
            track.shapes[-1] = track.shapes[-1]._replace(outside=True)
            task_data.add_track(track)
