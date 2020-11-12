import cvat.apps.engine.models
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from cvat.apps.dataset_manager.task import _merge_table_rows


# some modified functions to transer annotation
def _bulk_create(db_model, db_alias, objects, flt_param):
    if objects:
        if flt_param:
            if 'postgresql' in settings.DATABASES["default"]["ENGINE"]:
                return db_model.objects.using(db_alias).bulk_create(objects)
            else:
                ids = list(db_model.objects.using(db_alias).filter(**flt_param).values_list('id', flat=True))
                db_model.objects.using(db_alias).bulk_create(objects)

                return list(db_model.objects.using(db_alias).exclude(id__in=ids).filter(**flt_param))
        else:
            return db_model.objects.using(db_alias).bulk_create(objects)


def get_old_db_shapes(shape_type, db_job):
    def _get_shape_set(db_job, shape_type):
        if shape_type == 'polygons':
            return db_job.labeledpolygon_set
        elif shape_type == 'polylines':
            return db_job.labeledpolyline_set
        elif shape_type == 'boxes':
            return db_job.labeledbox_set
        elif shape_type == 'points':
            return db_job.labeledpoints_set

    def get_values(shape_type):
        if shape_type == 'polygons':
            return [
                ('id', 'frame', 'points', 'label_id', 'group_id', 'occluded', 'z_order', 'client_id',
                 'labeledpolygonattributeval__value', 'labeledpolygonattributeval__spec_id',
                 'labeledpolygonattributeval__id'), {
                    'attributes': [
                        'labeledpolygonattributeval__value',
                        'labeledpolygonattributeval__spec_id',
                        'labeledpolygonattributeval__id'
                    ]
                }, 'labeledpolygonattributeval_set'
            ]
        elif shape_type == 'polylines':
            return [
                ('id', 'frame', 'points', 'label_id', 'group_id', 'occluded', 'z_order', 'client_id',
                 'labeledpolylineattributeval__value', 'labeledpolylineattributeval__spec_id',
                 'labeledpolylineattributeval__id'), {
                    'attributes': [
                        'labeledpolylineattributeval__value',
                        'labeledpolylineattributeval__spec_id',
                        'labeledpolylineattributeval__id'
                    ]
                }, 'labeledpolylineattributeval_set'
            ]
        elif shape_type == 'boxes':
            return [
                ('id', 'frame', 'xtl', 'ytl', 'xbr', 'ybr', 'label_id', 'group_id', 'occluded', 'z_order', 'client_id',
                 'labeledboxattributeval__value', 'labeledboxattributeval__spec_id',
                 'labeledboxattributeval__id'), {
                    'attributes': [
                        'labeledboxattributeval__value',
                        'labeledboxattributeval__spec_id',
                        'labeledboxattributeval__id'
                    ]
                }, 'labeledboxattributeval_set'
            ]
        elif shape_type == 'points':
            return [
                ('id', 'frame', 'points', 'label_id', 'group_id', 'occluded', 'z_order', 'client_id',
                 'labeledpointsattributeval__value', 'labeledpointsattributeval__spec_id',
                 'labeledpointsattributeval__id'), {
                    'attributes': [
                        'labeledpointsattributeval__value',
                        'labeledpointsattributeval__spec_id',
                        'labeledpointsattributeval__id'
                    ]
                }, 'labeledpointsattributeval_set'
            ]

    (values, merge_keys, prefetch) = get_values(shape_type)
    db_shapes = list(_get_shape_set(db_job, shape_type).prefetch_related(prefetch).values(*values).order_by('frame'))
    return _merge_table_rows(db_shapes, merge_keys, 'id')


def get_old_db_paths(db_job):
    db_paths = db_job.objectpath_set
    for shape in ['trackedpoints_set', 'trackedbox_set', 'trackedpolyline_set', 'trackedpolygon_set']:
        db_paths.prefetch_related(shape)
    for shape_attr in ['trackedpoints_set__trackedpointsattributeval_set', 'trackedbox_set__trackedboxattributeval_set',
                       'trackedpolygon_set__trackedpolygonattributeval_set',
                       'trackedpolyline_set__trackedpolylineattributeval_set']:
        db_paths.prefetch_related(shape_attr)
    db_paths.prefetch_related('objectpathattributeval_set')
    db_paths = list(db_paths.values('id', 'frame', 'group_id', 'shapes', 'client_id', 'objectpathattributeval__spec_id',
                                    'objectpathattributeval__id', 'objectpathattributeval__value',
                                    'trackedbox', 'trackedpolygon', 'trackedpolyline', 'trackedpoints',
                                    'trackedbox__id', 'label_id', 'trackedbox__xtl', 'trackedbox__ytl',
                                    'trackedbox__xbr', 'trackedbox__ybr', 'trackedbox__frame', 'trackedbox__occluded',
                                    'trackedbox__z_order', 'trackedbox__outside',
                                    'trackedbox__trackedboxattributeval__spec_id',
                                    'trackedbox__trackedboxattributeval__value',
                                    'trackedbox__trackedboxattributeval__id',
                                    'trackedpolygon__id', 'trackedpolygon__points', 'trackedpolygon__frame',
                                    'trackedpolygon__occluded',
                                    'trackedpolygon__z_order', 'trackedpolygon__outside',
                                    'trackedpolygon__trackedpolygonattributeval__spec_id',
                                    'trackedpolygon__trackedpolygonattributeval__value',
                                    'trackedpolygon__trackedpolygonattributeval__id',
                                    'trackedpolyline__id', 'trackedpolyline__points', 'trackedpolyline__frame',
                                    'trackedpolyline__occluded',
                                    'trackedpolyline__z_order', 'trackedpolyline__outside',
                                    'trackedpolyline__trackedpolylineattributeval__spec_id',
                                    'trackedpolyline__trackedpolylineattributeval__value',
                                    'trackedpolyline__trackedpolylineattributeval__id',
                                    'trackedpoints__id', 'trackedpoints__points', 'trackedpoints__frame',
                                    'trackedpoints__occluded',
                                    'trackedpoints__z_order', 'trackedpoints__outside',
                                    'trackedpoints__trackedpointsattributeval__spec_id',
                                    'trackedpoints__trackedpointsattributeval__value',
                                    'trackedpoints__trackedpointsattributeval__id')
                    .order_by('id', 'trackedbox__frame', 'trackedpolygon__frame', 'trackedpolyline__frame',
                              'trackedpoints__frame'))

    db_box_paths = list(filter(lambda path: path['shapes'] == 'boxes', db_paths))
    db_polygon_paths = list(filter(lambda path: path['shapes'] == 'polygons', db_paths))
    db_polyline_paths = list(filter(lambda path: path['shapes'] == 'polylines', db_paths))
    db_points_paths = list(filter(lambda path: path['shapes'] == 'points', db_paths))

    object_path_attr_merge_key = [
        'objectpathattributeval__value',
        'objectpathattributeval__spec_id',
        'objectpathattributeval__id'
    ]

    db_box_paths = _merge_table_rows(db_box_paths, {
        'attributes': object_path_attr_merge_key,
        'shapes': [
            'trackedbox__id', 'trackedbox__xtl', 'trackedbox__ytl',
            'trackedbox__xbr', 'trackedbox__ybr', 'trackedbox__frame',
            'trackedbox__occluded', 'trackedbox__z_order', 'trackedbox__outside',
            'trackedbox__trackedboxattributeval__value',
            'trackedbox__trackedboxattributeval__spec_id',
            'trackedbox__trackedboxattributeval__id'
        ],
    }, 'id')

    db_polygon_paths = _merge_table_rows(db_polygon_paths, {
        'attributes': object_path_attr_merge_key,
        'shapes': [
            'trackedpolygon__id', 'trackedpolygon__points', 'trackedpolygon__frame',
            'trackedpolygon__occluded', 'trackedpolygon__z_order', 'trackedpolygon__outside',
            'trackedpolygon__trackedpolygonattributeval__value',
            'trackedpolygon__trackedpolygonattributeval__spec_id',
            'trackedpolygon__trackedpolygonattributeval__id'
        ]
    }, 'id')

    db_polyline_paths = _merge_table_rows(db_polyline_paths, {
        'attributes': object_path_attr_merge_key,
        'shapes': [
            'trackedpolyline__id', 'trackedpolyline__points', 'trackedpolyline__frame',
            'trackedpolyline__occluded', 'trackedpolyline__z_order', 'trackedpolyline__outside',
            'trackedpolyline__trackedpolylineattributeval__value',
            'trackedpolyline__trackedpolylineattributeval__spec_id',
            'trackedpolyline__trackedpolylineattributeval__id'
        ],
    }, 'id')

    db_points_paths = _merge_table_rows(db_points_paths, {
        'attributes': object_path_attr_merge_key,
        'shapes': [
            'trackedpoints__id', 'trackedpoints__points', 'trackedpoints__frame',
            'trackedpoints__occluded', 'trackedpoints__z_order', 'trackedpoints__outside',
            'trackedpoints__trackedpointsattributeval__value',
            'trackedpoints__trackedpointsattributeval__spec_id',
            'trackedpoints__trackedpointsattributeval__id'
        ]
    }, 'id')

    for db_box_path in db_box_paths:
        db_box_path.attributes = list(set(db_box_path.attributes))
        db_box_path.type = 'box_path'
        db_box_path.shapes = _merge_table_rows(db_box_path.shapes, {
            'attributes': [
                'trackedboxattributeval__value',
                'trackedboxattributeval__spec_id',
                'trackedboxattributeval__id'
            ]
        }, 'id')

    for db_polygon_path in db_polygon_paths:
        db_polygon_path.attributes = list(set(db_polygon_path.attributes))
        db_polygon_path.type = 'poligon_path'
        db_polygon_path.shapes = _merge_table_rows(db_polygon_path.shapes, {
            'attributes': [
                'trackedpolygonattributeval__value',
                'trackedpolygonattributeval__spec_id',
                'trackedpolygonattributeval__id'
            ]
        }, 'id')

    for db_polyline_path in db_polyline_paths:
        db_polyline_path.attributes = list(set(db_polyline_path.attributes))
        db_polyline_path.type = 'polyline_path'
        db_polyline_path.shapes = _merge_table_rows(db_polyline_path.shapes, {
            'attributes': [
                'trackedpolylineattributeval__value',
                'trackedpolylineattributeval__spec_id',
                'trackedpolylineattributeval__id'
            ]
        }, 'id')

    for db_points_path in db_points_paths:
        db_points_path.attributes = list(set(db_points_path.attributes))
        db_points_path.type = 'points_path'
        db_points_path.shapes = _merge_table_rows(db_points_path.shapes, {
            'attributes': [
                'trackedpointsattributeval__value',
                'trackedpointsattributeval__spec_id',
                'trackedpointsattributeval__id'
            ]
        }, 'id')
    return db_box_paths + db_polygon_paths + db_polyline_paths + db_points_paths


def process_shapes(db_job, apps, db_labels, db_attributes, db_alias):
    LabeledShape = apps.get_model('engine', 'LabeledShape')
    LabeledShapeAttributeVal = apps.get_model('engine', 'LabeledShapeAttributeVal')
    new_db_shapes = []
    new_db_attrvals = []
    for shape_type in ['boxes', 'points', 'polygons', 'polylines']:
        for shape in get_old_db_shapes(shape_type, db_job):
            new_db_shape = LabeledShape()
            new_db_shape.job = db_job
            new_db_shape.label = db_labels[shape.label_id]
            new_db_shape.group = shape.group_id

            if shape_type == 'boxes':
                new_db_shape.type = cvat.apps.engine.models.ShapeType.RECTANGLE
                new_db_shape.points = [shape.xtl, shape.ytl, shape.xbr, shape.ybr]
            else:
                new_db_shape.points = shape.points.replace(',', ' ').split()
                if shape_type == 'points':
                    new_db_shape.type = cvat.apps.engine.models.ShapeType.POINTS
                elif shape_type == 'polygons':
                    new_db_shape.type = cvat.apps.engine.models.ShapeType.POLYGON
                elif shape_type == 'polylines':
                    new_db_shape.type = cvat.apps.engine.models.ShapeType.POLYLINE

            new_db_shape.frame = shape.frame
            new_db_shape.occluded = shape.occluded
            new_db_shape.z_order = shape.z_order

            for attr in shape.attributes:
                db_attrval = LabeledShapeAttributeVal()
                db_attrval.shape_id = len(new_db_shapes)
                db_attrval.spec = db_attributes[attr.spec_id]
                db_attrval.value = attr.value
                new_db_attrvals.append(db_attrval)

            new_db_shapes.append(new_db_shape)

    new_db_shapes = _bulk_create(LabeledShape, db_alias, new_db_shapes, {"job_id": db_job.id})
    for db_attrval in new_db_attrvals:
        db_attrval.shape_id = new_db_shapes[db_attrval.shape_id].id

    _bulk_create(LabeledShapeAttributeVal, db_alias, new_db_attrvals, {})


def process_paths(db_job, apps, db_labels, db_attributes, db_alias):
    TrackedShape = apps.get_model('engine', 'TrackedShape')
    LabeledTrack = apps.get_model('engine', 'LabeledTrack')
    LabeledTrackAttributeVal = apps.get_model('engine', 'LabeledTrackAttributeVal')
    TrackedShapeAttributeVal = apps.get_model('engine', 'TrackedShapeAttributeVal')
    tracks = get_old_db_paths(db_job)

    new_db_tracks = []
    new_db_track_attrvals = []
    new_db_shapes = []
    new_db_shape_attrvals = []

    for track in tracks:
        db_track = LabeledTrack()
        db_track.job = db_job
        db_track.label = db_labels[track.label_id]
        db_track.frame = track.frame
        db_track.group = track.group_id

        for attr in track.attributes:
            db_attrspec = db_attributes[attr.spec_id]
            db_attrval = LabeledTrackAttributeVal()
            db_attrval.track_id = len(new_db_tracks)
            db_attrval.spec = db_attrspec
            db_attrval.value = attr.value
            new_db_track_attrvals.append(db_attrval)

        for shape in track.shapes:
            db_shape = TrackedShape()
            db_shape.track_id = len(new_db_tracks)
            db_shape.frame = shape.frame
            db_shape.occluded = shape.occluded
            db_shape.z_order = shape.z_order
            db_shape.outside = shape.outside
            if track.type == 'box_path':
                db_shape.type = cvat.apps.engine.models.ShapeType.RECTANGLE
                db_shape.points = [shape.xtl, shape.ytl, shape.xbr, shape.ybr]
            else:
                db_shape.points = shape.points.replace(',', ' ').split()
                if track.type == 'points_path':
                    db_shape.type = cvat.apps.engine.models.ShapeType.POINTS
                elif track.type == 'polygon_path':
                    db_shape.type = cvat.apps.engine.models.ShapeType.POLYGON
                elif track.type == 'polyline_path':
                    db_shape.type = cvat.apps.engine.models.ShapeType.POLYLINE

            for attr in shape.attributes:
                db_attrspec = db_attributes[attr.spec_id]
                db_attrval = TrackedShapeAttributeVal()
                db_attrval.shape_id = len(new_db_shapes)
                db_attrval.spec = db_attrspec
                db_attrval.value = attr.value
                new_db_shape_attrvals.append(db_attrval)

            new_db_shapes.append(db_shape)
        new_db_tracks.append(db_track)

    new_db_tracks = _bulk_create(LabeledTrack, db_alias, new_db_tracks, {"job_id": db_job.id})

    for db_attrval in new_db_track_attrvals:
        db_attrval.track_id = new_db_tracks[db_attrval.track_id].id
    _bulk_create(LabeledTrackAttributeVal, db_alias, new_db_track_attrvals, {})

    for db_shape in new_db_shapes:
        db_shape.track_id = new_db_tracks[db_shape.track_id].id

    new_db_shapes = _bulk_create(TrackedShape, db_alias, new_db_shapes, {"track__job_id": db_job.id})

    for db_attrval in new_db_shape_attrvals:
        db_attrval.shape_id = new_db_shapes[db_attrval.shape_id].id

    _bulk_create(TrackedShapeAttributeVal, db_alias, new_db_shape_attrvals, {})


def copy_annotations_forward(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Task = apps.get_model('engine', 'Task')
    AttributeSpec = apps.get_model('engine', 'AttributeSpec')

    for task in Task.objects.all():
        print("run anno migration for the task {}".format(task.id))
        db_labels = {db_label.id: db_label for db_label in task.label_set.all()}
        db_attributes = {db_attr.id: db_attr for db_attr in AttributeSpec.objects.filter(label__task__id=task.id)}
        for segment in task.segment_set.prefetch_related('job_set').all():
            db_job = segment.job_set.first()
            print("run anno migration for the job {}".format(db_job.id))
            process_shapes(db_job, apps, db_labels, db_attributes, db_alias)
            process_paths(db_job, apps, db_labels, db_attributes, db_alias)


def _save_old_shapes_to_db(apps, db_shapes, db_attributes, db_alias, db_job):
    def _get_shape_class(shape_type):
        if shape_type == 'polygons':
            return apps.get_model('engine', 'LabeledPolygon')
        elif shape_type == 'polylines':
            return apps.get_model('engine', 'LabeledPolyline')
        elif shape_type == 'boxes':
            return apps.get_model('engine', 'LabeledBox')
        elif shape_type == 'points':
            return apps.get_model('engine', 'LabeledPoints')

    def _get_shape_attr_class(shape_type):
        if shape_type == 'polygons':
            return apps.get_model('engine', 'LabeledPolygonAttributeVal')
        elif shape_type == 'polylines':
            return apps.get_model('engine', 'LabeledPolylineAttributeVal')
        elif shape_type == 'boxes':
            return apps.get_model('engine', 'LabeledBoxAttributeVal')
        elif shape_type == 'points':
            return apps.get_model('engine', 'LabeledPointsAttributeVal')

    shapes = [
        list(filter(lambda s: s.type == cvat.apps.engine.models.ShapeType.RECTANGLE, db_shapes)),
        list(filter(lambda s: s.type == cvat.apps.engine.models.ShapeType.POLYLINE, db_shapes)),
        list(filter(lambda s: s.type == cvat.apps.engine.models.ShapeType.POLYGON, db_shapes)),
        list(filter(lambda s: s.type == cvat.apps.engine.models.ShapeType.POINTS, db_shapes)),
    ]
    for i, shape_type in enumerate(['boxes', 'polylines', 'polygons', 'points']):
        new_db_shapes = []
        new_db_attrvals = []
        for shape in shapes[i]:
            db_shape = _get_shape_class(shape_type)()
            db_shape.job = shape.job
            db_shape.label = shape.label
            db_shape.group_id = shape.group
            if shape.type == cvat.apps.engine.models.ShapeType.RECTANGLE:
                db_shape.xtl = shape.points[0]
                db_shape.ytl = shape.points[1]
                db_shape.xbr = shape.points[2]
                db_shape.ybr = shape.points[3]
            else:
                point_iterator = iter(shape.points)
                db_shape.points = ' '.join(['{},{}'.format(point, next(point_iterator)) for point in point_iterator])
            db_shape.frame = shape.frame
            db_shape.occluded = shape.occluded
            db_shape.z_order = shape.z_order

            for attr in list(shape.labeledshapeattributeval_set.all()):
                db_attrval = _get_shape_attr_class(shape_type)()
                if shape.type == cvat.apps.engine.models.ShapeType.POLYGON:
                    db_attrval.polygon_id = len(new_db_shapes)
                elif shape.type == cvat.apps.engine.models.ShapeType.POLYLINE:
                    db_attrval.polyline_id = len(new_db_shapes)
                elif shape.type == cvat.apps.engine.models.ShapeType.RECTANGLE:
                    db_attrval.box_id = len(new_db_shapes)
                else:
                    db_attrval.points_id = len(new_db_shapes)

                db_attrval.spec = db_attributes[attr.spec_id]
                db_attrval.value = attr.value
                new_db_attrvals.append(db_attrval)

            new_db_shapes.append(db_shape)

        new_db_shapes = _bulk_create(_get_shape_class(shape_type), db_alias, new_db_shapes, {"job_id": db_job.id})

        for db_attrval in new_db_attrvals:
            if shape_type == 'polygons':
                db_attrval.polygon_id = new_db_shapes[db_attrval.polygon_id].id
            elif shape_type == 'polylines':
                db_attrval.polyline_id = new_db_shapes[db_attrval.polyline_id].id
            elif shape_type == 'boxes':
                db_attrval.box_id = new_db_shapes[db_attrval.box_id].id
            else:
                db_attrval.points_id = new_db_shapes[db_attrval.points_id].id

        _bulk_create(_get_shape_attr_class(shape_type), db_alias, new_db_attrvals, {})


def _save_old_tracks_to_db(apps, db_shapes, db_attributes, db_alias, db_job):
    def _get_shape_class(shape_type):
        if shape_type == 'polygon_paths':
            return apps.get_model('engine', 'TrackedPolygon')
        elif shape_type == 'polyline_paths':
            return apps.get_model('engine', 'TrackedPolyline')
        elif shape_type == 'box_paths':
            return apps.get_model('engine', 'TrackedBox')
        elif shape_type == 'points_paths':
            return apps.get_model('engine', 'TrackedPoints')

    def _get_shape_attr_class(shape_type):
        if shape_type == 'polygon_paths':
            return apps.get_model('engine', 'TrackedPolygonAttributeVal')
        elif shape_type == 'polyline_paths':
            return apps.get_model('engine', 'TrackedPolylineAttributeVal')
        elif shape_type == 'box_paths':
            return apps.get_model('engine', 'TrackedBoxAttributeVal')
        elif shape_type == 'points_paths':
            return apps.get_model('engine', 'TrackedPointsAttributeVal')

    tracks = [
        list(filter(lambda t: t.trackedshape_set.first().type == cvat.apps.engine.models.ShapeType.RECTANGLE,
                    db_shapes)),
        list(
            filter(lambda t: t.trackedshape_set.first().type == cvat.apps.engine.models.ShapeType.POLYLINE, db_shapes)),
        list(filter(lambda t: t.trackedshape_set.first().type == cvat.apps.engine.models.ShapeType.POLYGON, db_shapes)),
        list(filter(lambda t: t.trackedshape_set.first().type == cvat.apps.engine.models.ShapeType.POINTS, db_shapes)),
    ]

    ObjectPath = apps.get_model('engine', 'ObjectPath')
    ObjectPathAttributeVal = apps.get_model('engine', 'ObjectPathAttributeVal')

    for i, shape_type in enumerate(['box_paths', 'polyline_paths', 'polygon_paths', 'points_paths', ]):
        new_db_paths = []
        new_db_path_attrvals = []
        new_db_shapes = []
        new_db_shape_attrvals = []

        for path in tracks[i]:
            db_path = ObjectPath()
            db_path.job = db_job
            db_path.label = path.label
            db_path.frame = path.frame
            db_path.group_id = path.group
            # db_path.client_id = path.client_id
            if shape_type == 'polygon_paths':
                db_path.shapes = 'polygons'
            elif shape_type == 'polyline_paths':
                db_path.shapes = 'polylines'
            elif shape_type == 'box_paths':
                db_path.shapes = 'boxes'
            elif shape_type == 'points_paths':
                db_path.shapes = 'points'

            for attr in list(path.labeledtrackattributeval_set.all()):
                db_attrspec = db_attributes[attr.spec_id]
                db_attrval = ObjectPathAttributeVal()
                db_attrval.track_id = len(new_db_paths)
                db_attrval.spec = db_attrspec
                db_attrval.value = attr.value
                new_db_path_attrvals.append(db_attrval)

            for shape in list(path.trackedshape_set.all()):
                db_shape = _get_shape_class(shape_type)()
                db_shape.track_id = len(new_db_paths)
                if shape_type == 'box_paths':
                    db_shape.xtl = shape.points[0]
                    db_shape.ytl = shape.points[1]
                    db_shape.xbr = shape.points[2]
                    db_shape.ybr = shape.points[3]
                else:
                    point_iterator = iter(shape.points)
                    db_shape.points = ' '.join(
                        ['{},{}'.format(point, next(point_iterator)) for point in point_iterator])

                db_shape.frame = shape.frame
                db_shape.occluded = shape.occluded
                db_shape.z_order = shape.z_order
                db_shape.outside = shape.outside

                for attr in list(shape.trackedshapeattributeval_set.all()):
                    db_attrspec = db_attributes[attr.spec_id]
                    db_attrval = _get_shape_attr_class(shape_type)()
                    if shape_type == 'polygon_paths':
                        db_attrval.polygon_id = len(new_db_shapes)
                    elif shape_type == 'polyline_paths':
                        db_attrval.polyline_id = len(new_db_shapes)
                    elif shape_type == 'box_paths':
                        db_attrval.box_id = len(new_db_shapes)
                    elif shape_type == 'points_paths':
                        db_attrval.points_id = len(new_db_shapes)
                    db_attrval.spec = db_attrspec
                    db_attrval.value = attr.value
                    new_db_shape_attrvals.append(db_attrval)

                new_db_shapes.append(db_shape)
            new_db_paths.append(db_path)

        new_db_paths = _bulk_create(ObjectPath, db_alias, new_db_paths, {"job_id": db_job.id})

        for db_attrval in new_db_path_attrvals:
            db_attrval.track_id = new_db_paths[db_attrval.track_id].id
        _bulk_create(ObjectPathAttributeVal, db_alias, new_db_path_attrvals, {})

        for db_shape in new_db_shapes:
            db_shape.track_id = new_db_paths[db_shape.track_id].id

        db_shapes = _bulk_create(_get_shape_class(shape_type), db_alias, new_db_shapes, {"track__job_id": db_job.id})

        for db_attrval in new_db_shape_attrvals:
            if shape_type == 'polygon_paths':
                db_attrval.polygon_id = db_shapes[db_attrval.polygon_id].id
            elif shape_type == 'polyline_paths':
                db_attrval.polyline_id = db_shapes[db_attrval.polyline_id].id
            elif shape_type == 'box_paths':
                db_attrval.box_id = db_shapes[db_attrval.box_id].id
            elif shape_type == 'points_paths':
                db_attrval.points_id = db_shapes[db_attrval.points_id].id

        _bulk_create(_get_shape_attr_class(shape_type), db_alias, new_db_shape_attrvals, {})


def copy_annotations_backward(apps, schema_editor):
    Task = apps.get_model('engine', 'Task')
    AttributeSpec = apps.get_model('engine', 'AttributeSpec')
    db_alias = schema_editor.connection.alias

    for task in Task.objects.all():
        db_attributes = {db_attr.id: db_attr for db_attr in AttributeSpec.objects.filter(label__task__id=task.id)}
        for segment in task.segment_set.prefetch_related('job_set').all():
            db_job = segment.job_set.first()

            db_shapes = list(db_job.labeledshape_set
                             .prefetch_related("label")
                             .prefetch_related("labeledshapeattributeval_set"))
            _save_old_shapes_to_db(apps, db_shapes, db_attributes, db_alias, db_job)

            db_tracks = list(db_job.labeledtrack_set
                             .select_related("label")
                             .prefetch_related("labeledtrackattributeval_set")
                             .prefetch_related("trackedshape_set__trackedshapeattributeval_set"))
            _save_old_tracks_to_db(apps, db_tracks, db_attributes, db_alias, db_job)


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0016_attribute_spec_20190217'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabeledImageAttributeVal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', cvat.apps.engine.models.SafeCharField(max_length=64)),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.AttributeSpec')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='LabeledShapeAttributeVal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', cvat.apps.engine.models.SafeCharField(max_length=64)),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.AttributeSpec')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='LabeledTrackAttributeVal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', cvat.apps.engine.models.SafeCharField(max_length=64)),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.AttributeSpec')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TrackedShape',
            fields=[
                ('type', models.CharField(
                    choices=[('rectangle', 'RECTANGLE'), ('polygon', 'POLYGON'), ('polyline', 'POLYLINE'),
                             ('points', 'POINTS')], max_length=16)),
                ('occluded', models.BooleanField(default=False)),
                ('z_order', models.IntegerField(default=0)),
                ('points', cvat.apps.engine.models.FloatArrayField()),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('frame', models.PositiveIntegerField()),
                ('outside', models.BooleanField(default=False)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TrackedShapeAttributeVal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', cvat.apps.engine.models.SafeCharField(max_length=64)),
                ('shape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.TrackedShape')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.AttributeSpec')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='LabeledImage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('frame', models.PositiveIntegerField()),
                ('group', models.PositiveIntegerField(null=True)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='LabeledShape',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('frame', models.PositiveIntegerField()),
                ('group', models.PositiveIntegerField(null=True)),
                ('type', models.CharField(
                    choices=[('rectangle', 'RECTANGLE'), ('polygon', 'POLYGON'), ('polyline', 'POLYLINE'),
                             ('points', 'POINTS')], max_length=16)),
                ('occluded', models.BooleanField(default=False)),
                ('z_order', models.IntegerField(default=0)),
                ('points', cvat.apps.engine.models.FloatArrayField()),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='LabeledTrack',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('frame', models.PositiveIntegerField()),
                ('group', models.PositiveIntegerField(null=True)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='labeledimage',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Job'),
        ),
        migrations.AddField(
            model_name='labeledtrack',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Job'),
        ),
        migrations.AddField(
            model_name='labeledshape',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Job'),
        ),
        migrations.AddField(
            model_name='labeledimage',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Label'),
        ),
        migrations.AddField(
            model_name='labeledshape',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Label'),
        ),
        migrations.AddField(
            model_name='labeledtrack',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Label'),
        ),
        migrations.AddField(
            model_name='trackedshape',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.LabeledTrack'),
        ),
        migrations.AddField(
            model_name='labeledtrackattributeval',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.LabeledTrack'),
        ),
        migrations.AddField(
            model_name='labeledshapeattributeval',
            name='shape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.LabeledShape'),
        ),
        migrations.AddField(
            model_name='labeledimageattributeval',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.LabeledImage'),
        ),
        migrations.RunPython(
            code=copy_annotations_forward,
            reverse_code=copy_annotations_backward,
        ),
        migrations.RemoveField(
            model_name='labeledbox',
            name='job',
        ),
        migrations.RemoveField(
            model_name='labeledbox',
            name='label',
        ),
        migrations.RemoveField(
            model_name='labeledboxattributeval',
            name='box',
        ),
        migrations.RemoveField(
            model_name='labeledboxattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='labeledpoints',
            name='job',
        ),
        migrations.RemoveField(
            model_name='labeledpoints',
            name='label',
        ),
        migrations.RemoveField(
            model_name='labeledpointsattributeval',
            name='points',
        ),
        migrations.RemoveField(
            model_name='labeledpointsattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='labeledpolygon',
            name='job',
        ),
        migrations.RemoveField(
            model_name='job',
            name='max_shape_id',
        ),
        migrations.RemoveField(
            model_name='labeledpolygon',
            name='label',
        ),
        migrations.RemoveField(
            model_name='labeledpolygonattributeval',
            name='polygon',
        ),
        migrations.RemoveField(
            model_name='labeledpolygonattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='labeledpolyline',
            name='job',
        ),
        migrations.RemoveField(
            model_name='labeledpolyline',
            name='label',
        ),
        migrations.RemoveField(
            model_name='labeledpolylineattributeval',
            name='polyline',
        ),
        migrations.RemoveField(
            model_name='labeledpolylineattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='objectpath',
            name='job',
        ),
        migrations.RemoveField(
            model_name='objectpath',
            name='label',
        ),
        migrations.RemoveField(
            model_name='objectpathattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='objectpathattributeval',
            name='track',
        ),
        migrations.RemoveField(
            model_name='trackedbox',
            name='track',
        ),
        migrations.RemoveField(
            model_name='trackedboxattributeval',
            name='box',
        ),
        migrations.RemoveField(
            model_name='trackedboxattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='trackedpoints',
            name='track',
        ),
        migrations.RemoveField(
            model_name='trackedpointsattributeval',
            name='points',
        ),
        migrations.RemoveField(
            model_name='trackedpointsattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='trackedpolygon',
            name='track',
        ),
        migrations.RemoveField(
            model_name='trackedpolygonattributeval',
            name='polygon',
        ),
        migrations.RemoveField(
            model_name='trackedpolygonattributeval',
            name='spec',
        ),
        migrations.RemoveField(
            model_name='trackedpolyline',
            name='track',
        ),
        migrations.RemoveField(
            model_name='trackedpolylineattributeval',
            name='polyline',
        ),
        migrations.RemoveField(
            model_name='trackedpolylineattributeval',
            name='spec',
        ),
        migrations.DeleteModel(
            name='LabeledBox',
        ),
        migrations.DeleteModel(
            name='LabeledBoxAttributeVal',
        ),
        migrations.DeleteModel(
            name='LabeledPoints',
        ),
        migrations.DeleteModel(
            name='LabeledPointsAttributeVal',
        ),
        migrations.DeleteModel(
            name='LabeledPolygon',
        ),
        migrations.DeleteModel(
            name='LabeledPolygonAttributeVal',
        ),
        migrations.DeleteModel(
            name='LabeledPolyline',
        ),
        migrations.DeleteModel(
            name='LabeledPolylineAttributeVal',
        ),
        migrations.DeleteModel(
            name='ObjectPath',
        ),
        migrations.DeleteModel(
            name='ObjectPathAttributeVal',
        ),
        migrations.DeleteModel(
            name='TrackedBox',
        ),
        migrations.DeleteModel(
            name='TrackedBoxAttributeVal',
        ),
        migrations.DeleteModel(
            name='TrackedPoints',
        ),
        migrations.DeleteModel(
            name='TrackedPointsAttributeVal',
        ),
        migrations.DeleteModel(
            name='TrackedPolygon',
        ),
        migrations.DeleteModel(
            name='TrackedPolygonAttributeVal',
        ),
        migrations.DeleteModel(
            name='TrackedPolyline',
        ),
        migrations.DeleteModel(
            name='TrackedPolylineAttributeVal',
        ),
    ]
