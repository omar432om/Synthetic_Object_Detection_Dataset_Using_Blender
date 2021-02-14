import bpy, os
from math import sin, cos, pi
import numpy as np
import json
import sys
import copy


dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import boundingbox
import importlib
importlib.reload(boundingbox)


""" Please define the following information:"""
location = r'C:\Users\omar4\Desktop\testing' #your desired output location
width = 608 #the rendering width you chose in Blender
height = 608#the rendering height you chose in Blender
particles = 1500#the number of particles you have created
frames_num = 30#Number of frames you want to render
"""********************************************************************************"""

def render(scene, camera_object, mesh_objects, camera_steps,stones_id, file_prefix="render" ):
    
    
    labels = []
    images = []
    for i in range(0, camera_steps + 1):
        for j in range(0, camera_steps + 1):
            # Rendering
            # https://blender.stackexchange.com/questions/1101/blender-rendering-automation-build-script
            filename = '{}-{}y-{}p.png'.format(str(file_prefix), str(i), str(j))
            bpy.context.scene.render.filepath = os.path.join(location, filename)
            bpy.ops.render.render(write_still=True)
            
             
            scene = bpy.data.scenes['Scene']
            image_entry = {"id": file_prefix,
            "license": 1,
            "file_name": filename,
            "height": height,
            "width": width,
            "date_captured": "2020-07-12T19:39:33+00:00" }
            
            label_entry = {"id": [],
                            "image_id": file_prefix,
                            "category_id": 1,
                            "bbox" : [], 
                            "area": [] ,
                            "segmentation": [],
                            "iscrowd": 0 
                         }
            print(file_prefix)
            
            """ Get the bounding box coordinates for each mesh """
            for object in mesh_objects:
                
                bounding_box = boundingbox.camera_view_bounds_2d(scene, camera_object, object)
                if bounding_box and object.visible_get():
                    x1 = int(bounding_box[0][0]*width)
                    x2 = int(bounding_box[1][0]*width)
                    y1 = int(bounding_box[0][1]*height)
                    y2 = int(bounding_box[1][1]*height)
                    Bwidth= x2 - x1
                    Bheight = y2 - y1
                    area = Bwidth*Bheight
                    label_entry['bbox'] = [
                         x1,
                         height-y2,
                         Bwidth,
                         Bheight,
                        ]
                    label_entry['id'] = stones_id
                    label_entry['area'] = area
                    stones_id =  stones_id + 1
                    labels.append(copy.deepcopy(label_entry))
                    
            images.append(image_entry)
            print(labels)
            
            
    return labels , images , stones_id


def batch_render(scene, camera_object, mesh_objects):
    import scene_setup
    camera_steps = 0
    scene_setup_steps = frames_num
    annotations_prev = {}
    cache_prev = {}
    with open(location + r'\labels.json', 'r+') as f:
        annotations_prev = json.load(f)
    with open(location +r'\cache.json', 'r+') as h:
        cache_prev = json.load(h)
    labels = annotations_prev["annotations"]
    images = annotations_prev["images"]
    stones_id = cache_prev["stones_id"]
    file_prefix = 0;
    for i in range(0, scene_setup_steps):
        frame_num = cache_prev["file_prefix"] +i +1 
        file_prefix = cache_prev["file_prefix"] +i +1
        scene_setup.simulate(scene, mesh_objects, frame_num)
        scene_labels ,  scene_images , stones_id = render(scene, camera_object, mesh_objects, camera_steps, stones_id,file_prefix= file_prefix )
        labels += scene_labels # Merge lists
        images += scene_images 
    info = {
        "year": "2020",
        "version": "1",
        "description": "",
        "contributor": "",
        "url": "",
        "date_created": "2020-07-12T19:39:33+00:00"
           }
    licenses = [
        {
            "id": 1,
            "url": "",
            "name": "Unknown"
        }
             ]
    categories = [
        {
            "id": 0,
            "name": "stone",
            "supercategory": "none"
        },
        {
            "id": 1,
            "name": "stone",
            "supercategory": "stone"
        }
                ]    
    annotations = {"info" : info , "licenses" : licenses , "categories" : categories , "images"  : images , "annotations" : labels }
    with open(location +r'\labels.json', 'w+') as f:
        json.dump(annotations, f, sort_keys=True, indent=4, separators=(',', ': '))
    cache = { "stones_id" : stones_id , "file_prefix" : file_prefix }
    with open(location + r'\cache.json', 'w+') as h:
        json.dump(cache, h, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    scene = bpy.data.scenes['Scene']
    camera_object = bpy.data.objects['Camera']
    mesh_names = ['{0:.4f}'.format(0.0001*x) for x in range(0,particles -1)]
    mesh_objects = [bpy.data.objects[name] for name in mesh_names]
    batch_render(scene, camera_object, mesh_objects)
