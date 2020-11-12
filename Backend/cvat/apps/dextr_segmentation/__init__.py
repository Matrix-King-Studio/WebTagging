from cvat.settings.base import JS_3RDPARTY

JS_3RDPARTY['engine'] = JS_3RDPARTY.get('engine', []) + ['dextr_segmentation/js/enginePlugin.js']
