import logging as log
import numpy as np

from unittest import TestCase

from datumaro.components.extractor import (Extractor, DatasetItem,
    Mask, Polygon, PolyLine, Points, Bbox, Label,
    LabelCategories, MaskCategories, AnnotationType
)
import datumaro.util.mask_tools as mask_tools
import datumaro.plugins.transforms as transforms
from datumaro.util.test_utils import compare_datasets


class TransformsTest(TestCase):
    def test_reindex(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=10),
                    DatasetItem(id=10, subset='train'),
                    DatasetItem(id='a', subset='val'),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=5),
                    DatasetItem(id=6, subset='train'),
                    DatasetItem(id=7, subset='val'),
                ])

        actual = transforms.Reindex(SrcExtractor(), start=5)
        compare_datasets(self, DstExtractor(), actual)

    def test_mask_to_polygons(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                items = [
                    DatasetItem(id=1, image=np.zeros((5, 10, 3)),
                        annotations=[
                            Mask(np.array([
                                    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                                    [0, 0, 1, 1, 0, 1, 1, 1, 0, 0],
                                    [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                ]),
                            ),
                        ]
                    ),
                ]
                return iter(items)

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 10, 3)),
                        annotations=[
                            Polygon([3.0, 2.5, 1.0, 0.0, 3.5, 0.0, 3.0, 2.5]),
                            Polygon([5.0, 3.5, 4.5, 0.0, 8.0, 0.0, 5.0, 3.5]),
                        ]
                    ),
                ])

        actual = transforms.MasksToPolygons(SrcExtractor())
        compare_datasets(self, DstExtractor(), actual)

    def test_mask_to_polygons_small_polygons_message(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                items = [
                    DatasetItem(id=1, image=np.zeros((5, 10, 3)),
                        annotations=[
                            Mask(np.array([
                                    [0, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 0],
                                ]),
                            ),
                        ]
                    ),
                ]
                return iter(items)

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([ DatasetItem(id=1, image=np.zeros((5, 10, 3))), ])

        with self.assertLogs(level=log.DEBUG) as logs:
            actual = transforms.MasksToPolygons(SrcExtractor())

            compare_datasets(self, DstExtractor(), actual)
            self.assertRegex('\n'.join(logs.output), 'too small polygons')

    def test_polygons_to_masks(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 10, 3)),
                        annotations=[
                            Polygon([0, 0, 4, 0, 4, 4]),
                            Polygon([5, 0, 9, 0, 5, 5]),
                        ]
                    ),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 10, 3)),
                        annotations=[
                            Mask(np.array([
                                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                                    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                ]),
                            ),
                            Mask(np.array([
                                    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                ]),
                            ),
                        ]
                    ),
                ])

        actual = transforms.PolygonsToMasks(SrcExtractor())
        compare_datasets(self, DstExtractor(), actual)

    def test_crop_covered_segments(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            # The mask is partially covered by the polygon
                            Mask(np.array([
                                    [0, 0, 1, 1, 1],
                                    [0, 0, 1, 1, 1],
                                    [1, 1, 1, 1, 1],
                                    [1, 1, 1, 0, 0],
                                    [1, 1, 1, 0, 0]],
                                ),
                                z_order=0),
                            Polygon([1, 1, 4, 1, 4, 4, 1, 4],
                                z_order=1),
                        ]
                    ),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            Mask(np.array([
                                    [0, 0, 1, 1, 1],
                                    [0, 0, 0, 0, 1],
                                    [1, 0, 0, 0, 1],
                                    [1, 0, 0, 0, 0],
                                    [1, 1, 1, 0, 0]],
                                ),
                                z_order=0),
                            Polygon([1, 1, 4, 1, 4, 4, 1, 4],
                                z_order=1),
                        ]
                    ),
                ])

        actual = transforms.CropCoveredSegments(SrcExtractor())
        compare_datasets(self, DstExtractor(), actual)

    def test_merge_instance_segments(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            Mask(np.array([
                                    [0, 0, 1, 1, 1],
                                    [0, 0, 0, 0, 1],
                                    [1, 0, 0, 0, 1],
                                    [1, 0, 0, 0, 0],
                                    [1, 1, 1, 0, 0]],
                                ),
                                z_order=0, group=1),
                            Polygon([1, 1, 4, 1, 4, 4, 1, 4],
                                z_order=1, group=1),
                            Polygon([0, 0, 0, 2, 2, 2, 2, 0],
                                z_order=1),
                        ]
                    ),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            Mask(np.array([
                                    [0, 0, 1, 1, 1],
                                    [0, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 0],
                                    [1, 1, 1, 0, 0]],
                                ),
                                z_order=0, group=1),
                            Mask(np.array([
                                    [1, 1, 0, 0, 0],
                                    [1, 1, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0]],
                                ),
                                z_order=1),
                        ]
                    ),
                ])

        actual = transforms.MergeInstanceSegments(SrcExtractor(),
            include_polygons=True)
        compare_datasets(self, DstExtractor(), actual)

    def test_map_subsets(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, subset='a'),
                    DatasetItem(id=2, subset='b'),
                    DatasetItem(id=3, subset='c'),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, subset=''),
                    DatasetItem(id=2, subset='a'),
                    DatasetItem(id=3, subset='c'),
                ])

        actual = transforms.MapSubsets(SrcExtractor(),
            { 'a': '', 'b': 'a' })
        compare_datasets(self, DstExtractor(), actual)

    def test_shapes_to_boxes(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            Mask(np.array([
                                    [0, 0, 1, 1, 1],
                                    [0, 0, 0, 0, 1],
                                    [1, 0, 0, 0, 1],
                                    [1, 0, 0, 0, 0],
                                    [1, 1, 1, 0, 0]],
                                ), id=1),
                            Polygon([1, 1, 4, 1, 4, 4, 1, 4], id=2),
                            PolyLine([1, 1, 2, 1, 2, 2, 1, 2], id=3),
                            Points([2, 2, 4, 2, 4, 4, 2, 4], id=4),
                        ]
                    ),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            Bbox(0, 0, 4, 4, id=1),
                            Bbox(1, 1, 3, 3, id=2),
                            Bbox(1, 1, 1, 1, id=3),
                            Bbox(2, 2, 2, 2, id=4),
                        ]
                    ),
                ])

        actual = transforms.ShapesToBoxes(SrcExtractor())
        compare_datasets(self, DstExtractor(), actual)

    def test_id_from_image(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image='path.jpg'),
                    DatasetItem(id=2),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id='path', image='path.jpg'),
                    DatasetItem(id=2),
                ])

        actual = transforms.IdFromImageName(SrcExtractor())
        compare_datasets(self, DstExtractor(), actual)

    def test_boxes_to_masks(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            Bbox(0, 0, 3, 3, z_order=1),
                            Bbox(0, 0, 3, 1, z_order=2),
                            Bbox(0, 2, 3, 1, z_order=3),
                        ]
                    ),
                ])

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, image=np.zeros((5, 5, 3)),
                        annotations=[
                            Mask(np.array([
                                    [1, 1, 1, 0, 0],
                                    [1, 1, 1, 0, 0],
                                    [1, 1, 1, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0]],
                                ),
                                z_order=1),
                            Mask(np.array([
                                    [1, 1, 1, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0]],
                                ),
                                z_order=2),
                            Mask(np.array([
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [1, 1, 1, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0]],
                                ),
                                z_order=3),
                        ]
                    ),
                ])

        actual = transforms.BoxesToMasks(SrcExtractor())
        compare_datasets(self, DstExtractor(), actual)

    def test_random_split(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, subset="a"),
                    DatasetItem(id=2, subset="a"),
                    DatasetItem(id=3, subset="b"),
                    DatasetItem(id=4, subset="b"),
                    DatasetItem(id=5, subset="b"),
                    DatasetItem(id=6, subset=""),
                    DatasetItem(id=7, subset=""),
                ])

        actual = transforms.RandomSplit(SrcExtractor(), splits=[
            ('train', 4.0 / 7.0),
            ('test', 3.0 / 7.0),
        ])

        self.assertEqual(4, len(actual.get_subset('train')))
        self.assertEqual(3, len(actual.get_subset('test')))

    def test_random_split_gives_error_on_wrong_ratios(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([DatasetItem(id=1)])

        with self.assertRaises(Exception):
            transforms.RandomSplit(SrcExtractor(), splits=[
                ('train', 0.5),
                ('test', 0.7),
            ])

        with self.assertRaises(Exception):
            transforms.RandomSplit(SrcExtractor(), splits=[])

        with self.assertRaises(Exception):
            transforms.RandomSplit(SrcExtractor(), splits=[
                ('train', -0.5),
                ('test', 1.5),
            ])

    def test_remap_labels(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, annotations=[
                        # Should be remapped
                        Label(1),
                        Bbox(1, 2, 3, 4, label=2),
                        Mask(image=np.array([1]), label=3),

                        # Should be kept
                        Polygon([1, 1, 2, 2, 3, 4], label=4),
                        PolyLine([1, 3, 4, 2, 5, 6], label=None)
                    ]),
                ])

            def categories(self):
                label_cat = LabelCategories()
                label_cat.add('label0')
                label_cat.add('label1')
                label_cat.add('label2')
                label_cat.add('label3')
                label_cat.add('label4')

                mask_cat = MaskCategories(
                    colormap=mask_tools.generate_colormap(5))

                return {
                    AnnotationType.label: label_cat,
                    AnnotationType.mask: mask_cat,
                }

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([
                    DatasetItem(id=1, annotations=[
                        Label(1),
                        Bbox(1, 2, 3, 4, label=0),
                        Mask(image=np.array([1]), label=1),

                        Polygon([1, 1, 2, 2, 3, 4], label=2),
                        PolyLine([1, 3, 4, 2, 5, 6], label=None)
                    ]),
                ])

            def categories(self):
                label_cat = LabelCategories()
                label_cat.add('label0')
                label_cat.add('label9')
                label_cat.add('label4')

                mask_cat = MaskCategories(colormap={
                    k: v for k, v in mask_tools.generate_colormap(5).items()
                    if k in { 0, 1, 3, 4 }
                })

                return {
                    AnnotationType.label: label_cat,
                    AnnotationType.mask: mask_cat,
                }

        actual = transforms.RemapLabels(SrcExtractor(), mapping={
            'label1': 'label9',
            'label2': 'label0',
            'label3': 'label9',
        }, default='keep')

        compare_datasets(self, DstExtractor(), actual)

    def test_remap_labels_delete_unspecified(self):
        class SrcExtractor(Extractor):
            def __iter__(self):
                return iter([ DatasetItem(id=1, annotations=[ Label(0) ]) ])

            def categories(self):
                label_cat = LabelCategories()
                label_cat.add('label0')

                return { AnnotationType.label: label_cat }

        class DstExtractor(Extractor):
            def __iter__(self):
                return iter([ DatasetItem(id=1, annotations=[]) ])

            def categories(self):
                return { AnnotationType.label: LabelCategories() }

        actual = transforms.RemapLabels(SrcExtractor(),
            mapping={}, default='delete')

        compare_datasets(self, DstExtractor(), actual)
