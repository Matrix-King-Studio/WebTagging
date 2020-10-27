from django.db import migrations
from django.conf import settings

from cvat.apps.engine.models import Job, ShapeType
from cvat.apps.engine.media_extractors import get_mime

from PIL import Image
from ast import literal_eval
import os


def make_image_meta_cache(db_task):
    with open(db_task.get_image_meta_cache_path(), 'w') as meta_file:
        cache = {
            'original_size': []
        }

        if db_task.mode == 'interpolation':
            image = Image.open(db_task.get_frame_path(0))
            cache['original_size'].append({
                'width': image.size[0],
                'height': image.size[1]
            })
            image.close()
        else:
            filenames = []
            for root, _, files in os.walk(db_task.get_upload_dirname()):
                fullnames = map(lambda f: os.path.join(root, f), files)
                images = filter(lambda x: get_mime(x) == 'image', fullnames)
                filenames.extend(images)
            filenames.sort()

            for image_path in filenames:
                image = Image.open(image_path)
                cache['original_size'].append({
                    'width': image.size[0],
                    'height': image.size[1]
                })
                image.close()

        meta_file.write(str(cache))


def get_image_meta_cache(db_task):
    try:
        with open(db_task.get_image_meta_cache_path()) as meta_cache_file:
            return literal_eval(meta_cache_file.read())
    except Exception:
        make_image_meta_cache(db_task)
        with open(db_task.get_image_meta_cache_path()) as meta_cache_file:
            return literal_eval(meta_cache_file.read())


def _flip_shape(shape, size):
    if shape.type == ShapeType.RECTANGLE:
        shape.points = [
            shape.points[2],  # xbr -> xtl
            shape.points[3],  # ybr -> ytl
            shape.points[0],  # xtl -> xbr
            shape.points[1]  # ytl -> ybr
        ]

    for x in range(0, len(shape.points), 2):
        y = x + 1
        shape.points[x] = size['width'] - shape.points[x]
        shape.points[y] = size['height'] - shape.points[y]


def frame_path(db_task, frame):
    task_dirname = os.path.join(settings.DATA_ROOT, str(db_task.id))
    d1 = str(int(frame) // 10000)
    d2 = str(int(frame) // 100)
    path = os.path.join(task_dirname, 'data', d1, d2, str(frame) + '.jpg')
    return path


def _get_image_meta_cache_path(self):
    task_dirname = os.path.join(settings.DATA_ROOT, str(self.id))
    return os.path.join(task_dirname, "image_meta.cache")


def forwards_func(apps, schema_editor):
    Task = apps.get_model('engine', 'Task')

    # class methods unavailable in the class which got via get_model()
    # nevertheless it is needed for us to use the function get_image_meta_cache()
    setattr(Task, 'get_image_meta_cache_path', _get_image_meta_cache_path)

    print('Getting flipped tasks...')
    db_flipped_tasks = Task.objects.prefetch_related(
        'image_set',
    ).filter(flipped=True).all()

    print('Conversion started...')
    for db_task in db_flipped_tasks:
        print('Processing task {}...'.format(db_task.id))
        db_image_by_frame = {}
        if db_task.mode == 'annotation':
            db_image_by_frame = {db_image.frame: {'width': db_image.width, 'height': db_image.height}
                                 for db_image in db_task.image_set.all()}
        else:
            im_meta_data = get_image_meta_cache(db_task)['original_size']
            db_image_by_frame = {
                0: {
                    'width': im_meta_data[0]['width'],
                    'height': im_meta_data[0]['height']
                }
            }

        def get_size(frame):
            if frame in db_image_by_frame:
                return db_image_by_frame[frame]
            else:
                return db_image_by_frame[0]

        db_jobs = Job.objects.select_related('segment').prefetch_related(
            'labeledshape_set',
            'labeledtrack_set',
            'labeledtrack_set__trackedshape_set').filter(segment__task_id=db_task.id).all()

        for db_job in db_jobs:
            db_shapes = db_job.labeledshape_set.all()
            db_tracks = db_job.labeledtrack_set.all()
            for db_shape in db_shapes:
                _flip_shape(db_shape, get_size(db_shape.frame))
                db_shape.save()

            for db_track in db_tracks:
                db_shapes = db_track.trackedshape_set.all()
                for db_shape in db_shapes:
                    _flip_shape(db_shape, get_size(db_shape.frame))
                    db_shape.save()

    for db_task in db_flipped_tasks:
        for frame in range(db_task.size):
            path = frame_path(db_task, frame)
            if os.path.islink(path):
                path = os.path.realpath(path)

            try:
                image = Image.open(path)
                image = image.transpose(Image.ROTATE_180)
                image.save(path)
            except IOError as ex:
                print('Error of handling the frame {}'.format(frame))
                print(ex)


class Migration(migrations.Migration):
    dependencies = [
        ('engine', '0019_frame_selection'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func
        ),

        migrations.RemoveField(
            model_name='task',
            name='flipped',
        ),
    ]
