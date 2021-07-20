"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory

from napari.layers import Image, Shapes



def apply(image, points, axis):
    
    


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")



def widget_wrapper():
    from napari.qt.threading import thread_worker

    @thread_worker
    def run_project(image, points, axis, method):

        if method == 'CNN':
            ar2 = apply(image, points, channel)
        else:
            ar2 = np.max(image, axis=axis)
        return ar2

    @magicgui(call_button='run projection',
              layout='vertical',
              axis = dict(widget_type='SpinBox', label='axis', value=0),
              method = dict(widget_type='ComboBox', label ='method', choices=('rbf', 'maxproj'), value='rbf')
              )
    def widget(#label_logo,                                                                                                                                                  
            viewer: napari.viewer.Viewer,
            image_layer: Image,
            point_layer: Points,
            axis,
            method):

        def _new_layers(result):
            viewer.add_image(result[0], name=image_layer.name + '_orig', visible=False)
            viewer.add_image(result[1], name=image_layer.name + '_mask', visible=False)
            viewer.add_image(result[2], name=image_layer.name + '_projected', visible=False)

        def _new_image(result):
            _new_layers(result)
            viewer.layers[-1].visible = True
            image_layer.visible = True
            widget.call_button.enabled = True

        image = image_layer.data

        cp_worker = run_project(image, points, axis, method)
        cp_worker.returned.connect(_new_image)
        cp_worker.start()


    
    
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return widget_wrapper, {'name':'manual-stack-project'}
