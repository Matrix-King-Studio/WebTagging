# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: MIT

from copy import copy, deepcopy

import numpy as np
from scipy.optimize import linear_sum_assignment
from shapely import geometry

from cvat.apps.engine.models import ShapeType
from cvat.apps.engine.serializers import LabeledDataSerializer


class AnnotationIR:
    def __init__(self, data=None):
        self.reset()
        if data:
            self.tags = getattr(data, 'tags', []) or data['tags']
            self.shapes = getattr(data, 'shapes', []) or data['shapes']
            self.tracks = getattr(data, 'tracks', []) or data['tracks']

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_shape(self, shape):
        self.shapes.append(shape)

    def add_track(self, track):
        self.tracks.append(track)

    @property
    def data(self):
        return {
            'version': self.version,
            'tags': self.tags,
            'shapes': self.shapes,
            'tracks': self.tracks,
        }

    def __getitem__(self, key):
        return getattr(self, key)

    @data.setter
    def data(self, data):
        self.version = data['version']
        self.tags = data['tags']
        self.shapes = data['shapes']
        self.tracks = data['tracks']

    def serialize(self):
        serializer = LabeledDataSerializer(data=self.data)
        if serializer.is_valid(raise_exception=True):
            return serializer.data

    @staticmethod
    def _is_shape_inside(shape, start, stop):
        return start <= int(shape['frame']) <= stop

    @staticmethod
    def _is_track_inside(track, start, stop):
        def has_overlap(a, b):
            # a <= b
            return 0 <= min(b, stop) - max(a, start)

        prev_shape = None
        for shape in track['shapes']:
            if prev_shape and not prev_shape['outside'] and \
                has_overlap(prev_shape['frame'], shape['frame']):
                    return True
            prev_shape = shape

        if not prev_shape['outside'] and prev_shape['frame'] <= stop:
            return True

        return False

    @classmethod
    def _slice_track(cls, track_, start, stop):
        def filter_track_shapes(shapes):
            shapes = [s for s in shapes if cls._is_shape_inside(s, start, stop)]
            drop_count = 0
            for s in shapes:
                if s['outside']:
                    drop_count += 1
                else:
                    break
            # Need to leave the last shape if all shapes are outside
            if drop_count == len(shapes):
                drop_count -= 1

            return shapes[drop_count:]

        track = deepcopy(track_)
        segment_shapes = filter_track_shapes(track['shapes'])

        if len(segment_shapes) < len(track['shapes']):
            interpolated_shapes = TrackManager.get_interpolated_shapes(
                track, start, stop)
            scoped_shapes = filter_track_shapes(interpolated_shapes)

            if scoped_shapes:
                if not scoped_shapes[0]['keyframe']:
                    segment_shapes.insert(0, scoped_shapes[0])
                if not scoped_shapes[-1]['keyframe']:
                    segment_shapes.append(scoped_shapes[-1])

            # Should delete 'interpolation_shapes' and 'keyframe' keys because
            # Track and TrackedShape models don't expect these fields
            del track['interpolated_shapes']
            for shape in segment_shapes:
                del shape['keyframe']

        track['shapes'] = segment_shapes
        track['frame'] = track['shapes'][0]['frame']
        return track

    def slice(self, start, stop):
        #makes a data copy from specified frame interval
        splitted_data = AnnotationIR()
        splitted_data.tags = [deepcopy(t)
            for t in self.tags if self._is_shape_inside(t, start, stop)]
        splitted_data.shapes = [deepcopy(s)
            for s in self.shapes if self._is_shape_inside(s, start, stop)]
        splitted_data.tracks = [self._slice_track(t, start, stop)
            for t in self.tracks if self._is_track_inside(t, start, stop)]

        return splitted_data

    def reset(self):
        self.version = 0
        self.tags = []
        self.shapes = []
        self.tracks = []

class AnnotationManager:
    def __init__(self, data):
        self.data = data

    def merge(self, data, start_frame, overlap):
        tags = TagManager(self.data.tags)
        tags.merge(data.tags, start_frame, overlap)

        shapes = ShapeManager(self.data.shapes)
        shapes.merge(data.shapes, start_frame, overlap)

        tracks = TrackManager(self.data.tracks)
        tracks.merge(data.tracks, start_frame, overlap)

    def to_shapes(self, end_frame):
        shapes = self.data.shapes
        tracks = TrackManager(self.data.tracks)

        return shapes + tracks.to_shapes(end_frame)

    def to_tracks(self):
        tracks = self.data.tracks
        shapes = ShapeManager(self.data.shapes)

        return tracks + shapes.to_tracks()

class ObjectManager:
    def __init__(self, objects):
        self.objects = objects

    @staticmethod
    def _get_objects_by_frame(objects, start_frame):
        objects_by_frame = {}
        for obj in objects:
            if obj["frame"] >= start_frame:
                if obj["frame"] in objects_by_frame:
                    objects_by_frame[obj["frame"]].append(obj)
                else:
                    objects_by_frame[obj["frame"]] = [obj]

        return objects_by_frame

    @staticmethod
    def _get_cost_threshold():
        raise NotImplementedError()

    @staticmethod
    def _calc_objects_similarity(obj0, obj1, start_frame, overlap):
        raise NotImplementedError()

    @staticmethod
    def _unite_objects(obj0, obj1):
        raise NotImplementedError()

    @staticmethod
    def _modify_unmached_object(obj, end_frame):
        raise NotImplementedError()

    def merge(self, objects, start_frame, overlap):
        # 1. Split objects on two parts: new and which can be intersected
        # with existing objects.
        new_objects = [obj for obj in objects
            if obj["frame"] >= start_frame + overlap]
        int_objects = [obj for obj in objects
            if obj["frame"] < start_frame + overlap]
        assert len(new_objects) + len(int_objects) == len(objects)

        # 2. Convert to more convenient data structure (objects by frame)
        int_objects_by_frame = self._get_objects_by_frame(int_objects, start_frame)
        old_objects_by_frame = self._get_objects_by_frame(self.objects, start_frame)

        # 3. Add new objects as is. It should be done only after old_objects_by_frame
        # variable is initialized.
        self.objects.extend(new_objects)

        # Nothing to merge here. Just add all int_objects if any.
        if not old_objects_by_frame or not int_objects_by_frame:
            for frame in old_objects_by_frame:
                for old_obj in old_objects_by_frame[frame]:
                    self._modify_unmached_object(old_obj, start_frame + overlap)
            self.objects.extend(int_objects)
            return

        # 4. Build cost matrix for each frame and find correspondence using
        # Hungarian algorithm. In this case min_cost_thresh is stronger
        # because we compare only on one frame.
        min_cost_thresh = self._get_cost_threshold()
        for frame in int_objects_by_frame:
            if frame in old_objects_by_frame:
                int_objects = int_objects_by_frame[frame]
                old_objects = old_objects_by_frame[frame]
                cost_matrix = np.empty(shape=(len(int_objects), len(old_objects)),
                    dtype=float)
                # 5.1 Construct cost matrix for the frame.
                for i, int_obj in enumerate(int_objects):
                    for j, old_obj in enumerate(old_objects):
                        cost_matrix[i][j] = 1 - self._calc_objects_similarity(
                            int_obj, old_obj, start_frame, overlap)

                # 6. Find optimal solution using Hungarian algorithm.
                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                old_objects_indexes = list(range(0, len(old_objects)))
                int_objects_indexes = list(range(0, len(int_objects)))
                for i, j in zip(row_ind, col_ind):
                    # Reject the solution if the cost is too high. Remember
                    # inside int_objects_indexes objects which were handled.
                    if cost_matrix[i][j] <= min_cost_thresh:
                        old_objects[j] = self._unite_objects(int_objects[i], old_objects[j])
                        int_objects_indexes[i] = -1
                        old_objects_indexes[j] = -1

                # 7. Add all new objects which were not processed.
                for i in int_objects_indexes:
                    if i != -1:
                        self.objects.append(int_objects[i])

                # 8. Modify all old objects which were not processed
                # (e.g. generate a shape with outside=True at the end).
                for j in old_objects_indexes:
                    if j != -1:
                        self._modify_unmached_object(old_objects[j],
                            start_frame + overlap)
            else:
                # We don't have old objects on the frame. Let's add all new ones.
                self.objects.extend(int_objects_by_frame[frame])

class TagManager(ObjectManager):
    @staticmethod
    def _get_cost_threshold():
        return 0.25

    @staticmethod
    def _calc_objects_similarity(obj0, obj1, start_frame, overlap):
        # TODO: improve the trivial implementation, compare attributes
        return 1 if obj0["label_id"] == obj1["label_id"] else 0

    @staticmethod
    def _unite_objects(obj0, obj1):
        # TODO: improve the trivial implementation
        return obj0 if obj0["frame"] < obj1["frame"] else obj1

    @staticmethod
    def _modify_unmached_object(obj, end_frame):
        pass

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

class ShapeManager(ObjectManager):
    def to_tracks(self):
        tracks = []
        for shape in self.objects:
            shape0 = copy(shape)
            shape0["keyframe"] = True
            shape0["outside"] = False
            # TODO: Separate attributes on mutable and unmutable
            shape0["attributes"] = []
            shape0.pop("group", None)
            shape1 = copy(shape0)
            shape1["outside"] = True
            shape1["frame"] += 1

            track = {
                "label_id": shape["label_id"],
                "frame": shape["frame"],
                "group": shape.get("group", None),
                "attributes": shape["attributes"],
                "shapes": [shape0, shape1]
            }
            tracks.append(track)

        return tracks

    @staticmethod
    def _get_cost_threshold():
        return 0.25

    @staticmethod
    def _calc_objects_similarity(obj0, obj1, start_frame, overlap):
        def _calc_polygons_similarity(p0, p1):
            overlap_area = p0.intersection(p1).area
            return overlap_area / (p0.area + p1.area - overlap_area)

        has_same_type  = obj0["type"] == obj1["type"]
        has_same_label = obj0.get("label_id") == obj1.get("label_id")
        if has_same_type and has_same_label:
            if obj0["type"] == ShapeType.RECTANGLE:
                p0 = geometry.box(*obj0["points"])
                p1 = geometry.box(*obj1["points"])

                return _calc_polygons_similarity(p0, p1)
            elif obj0["type"] == ShapeType.POLYGON:
                p0 = geometry.Polygon(pairwise(obj0["points"]))
                p1 = geometry.Polygon(pairwise(obj0["points"]))

                return _calc_polygons_similarity(p0, p1)
            else:
                return 0 # FIXME: need some similarity for points and polylines
        return 0

    @staticmethod
    def _unite_objects(obj0, obj1):
        # TODO: improve the trivial implementation
        return obj0 if obj0["frame"] < obj1["frame"] else obj1

    @staticmethod
    def _modify_unmached_object(obj, end_frame):
        pass

class TrackManager(ObjectManager):
    def to_shapes(self, end_frame):
        shapes = []
        for idx, track in enumerate(self.objects):
            for shape in TrackManager.get_interpolated_shapes(track, 0, end_frame):
                shape["label_id"] = track["label_id"]
                shape["group"] = track["group"]
                shape["track_id"] = idx
                shape["attributes"] += track["attributes"]
                shapes.append(shape)
        return shapes

    @staticmethod
    def _get_objects_by_frame(objects, start_frame):
        # Just for unification. All tracks are assigned on the same frame
        objects_by_frame = {0: []}
        for obj in objects:
            shape = obj["shapes"][-1] # optimization for old tracks
            if shape["frame"] >= start_frame or not shape["outside"]:
                objects_by_frame[0].append(obj)

        if not objects_by_frame[0]:
            objects_by_frame = {}

        return objects_by_frame

    @staticmethod
    def _get_cost_threshold():
        return 0.5

    @staticmethod
    def _calc_objects_similarity(obj0, obj1, start_frame, overlap):
        if obj0["label_id"] == obj1["label_id"]:
            # Here start_frame is the start frame of next segment
            # and stop_frame is the stop frame of current segment
            # end_frame == stop_frame + 1
            end_frame = start_frame + overlap
            obj0_shapes = TrackManager.get_interpolated_shapes(obj0, start_frame, end_frame)
            obj1_shapes = TrackManager.get_interpolated_shapes(obj1, start_frame, end_frame)
            obj0_shapes_by_frame = {shape["frame"]:shape for shape in obj0_shapes}
            obj1_shapes_by_frame = {shape["frame"]:shape for shape in obj1_shapes}
            assert obj0_shapes_by_frame and obj1_shapes_by_frame

            count, error = 0, 0
            for frame in range(start_frame, end_frame):
                shape0 = obj0_shapes_by_frame.get(frame)
                shape1 = obj1_shapes_by_frame.get(frame)
                if shape0 and shape1:
                    if shape0["outside"] != shape1["outside"]:
                        error += 1
                    else:
                        error += 1 - ShapeManager._calc_objects_similarity(shape0, shape1, start_frame, overlap)
                    count += 1
                elif shape0 or shape1:
                    error += 1
                    count += 1

            return 1 - error / count
        else:
            return 0

    @staticmethod
    def _modify_unmached_object(obj, end_frame):
        shape = obj["shapes"][-1]
        if not shape["outside"]:
            shape = deepcopy(shape)
            shape["frame"] = end_frame
            shape["outside"] = True
            obj["shapes"].append(shape)
            # Need to update cached interpolated shapes
            # because key shapes were changed
            if obj.get("interpolated_shapes"):
                last_interpolated_shape = obj["interpolated_shapes"][-1]
                for frame in range(last_interpolated_shape["frame"] + 1, end_frame):
                    last_interpolated_shape = deepcopy(last_interpolated_shape)
                    last_interpolated_shape["frame"] = frame
                    obj["interpolated_shapes"].append(last_interpolated_shape)
                obj["interpolated_shapes"].append(shape)

    @staticmethod
    def normalize_shape(shape):
        points = list(shape["points"])
        if len(points) == 2:
            points.extend(points) # duplicate points for single point case
        points = np.asarray(points).reshape(-1, 2)
        broken_line = geometry.LineString(points)
        points = []
        for off in range(0, 100, 1):
            p = broken_line.interpolate(off / 100, True)
            points.append(p.x)
            points.append(p.y)

        shape = copy(shape)
        shape["points"] = points

        return shape

    @staticmethod
    def get_interpolated_shapes(track, start_frame, end_frame):
        def interpolate(shape0, shape1):
            shapes = []
            is_same_type = shape0["type"] == shape1["type"]
            is_polygon = shape0["type"] == ShapeType.POLYGON
            is_polyline = shape0["type"] == ShapeType.POLYLINE
            is_same_size = len(shape0["points"]) == len(shape1["points"])
            if not is_same_type or is_polygon or is_polyline or not is_same_size:
                shape0 = TrackManager.normalize_shape(shape0)
                shape1 = TrackManager.normalize_shape(shape1)

            distance = shape1["frame"] - shape0["frame"]
            step = np.subtract(shape1["points"], shape0["points"]) / distance
            for frame in range(shape0["frame"] + 1, shape1["frame"]):
                off = frame - shape0["frame"]
                if shape1["outside"]:
                    points = np.asarray(shape0["points"]).reshape(-1, 2)
                else:
                    points = (shape0["points"] + step * off).reshape(-1, 2)
                shape = deepcopy(shape0)
                if len(points) == 1:
                    shape["points"] = points.flatten()
                else:
                    broken_line = geometry.LineString(points).simplify(0.05, False)
                    shape["points"] = [x for p in broken_line.coords for x in p]

                shape["keyframe"] = False
                shape["frame"] = frame
                shapes.append(shape)
            return shapes

        if track.get("interpolated_shapes"):
            return track["interpolated_shapes"]

        # TODO: should be return an iterator?
        shapes = []
        curr_frame = track["shapes"][0]["frame"]
        prev_shape = {}
        for shape in track["shapes"]:
            if prev_shape:
                assert shape["frame"] > curr_frame
                for attr in prev_shape["attributes"]:
                    if attr["spec_id"] not in map(lambda el: el["spec_id"], shape["attributes"]):
                        shape["attributes"].append(deepcopy(attr))
                if not prev_shape["outside"]:
                    shapes.extend(interpolate(prev_shape, shape))

            shape["keyframe"] = True
            shapes.append(shape)
            curr_frame = shape["frame"]
            prev_shape = shape

        # TODO: Need to modify a client and a database (append "outside" shapes for polytracks)
        if not prev_shape["outside"] and (prev_shape["type"] == ShapeType.RECTANGLE
               or prev_shape["type"] == ShapeType.POINTS or prev_shape["type"] == ShapeType.CUBOID):
            shape = copy(prev_shape)
            shape["frame"] = end_frame
            shapes.extend(interpolate(prev_shape, shape))

        track["interpolated_shapes"] = shapes

        return shapes

    @staticmethod
    def _unite_objects(obj0, obj1):
        track = obj0 if obj0["frame"] < obj1["frame"] else obj1
        assert obj0["label_id"] == obj1["label_id"]
        shapes = {shape["frame"]:shape for shape in obj0["shapes"]}
        for shape in obj1["shapes"]:
            frame = shape["frame"]
            if frame in shapes:
                shapes[frame] = ShapeManager._unite_objects(shapes[frame], shape)
            else:
                shapes[frame] = shape

        track["frame"] = min(obj0["frame"], obj1["frame"])
        track["shapes"] = list(sorted(shapes.values(), key=lambda shape: shape["frame"]))
        track["interpolated_shapes"] = []

        return track
