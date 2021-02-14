import bpy
import math
# Set these to False if you don't want to key that property.
KEYFRAME_LOCATION = True
KEYFRAME_ROTATION = True
KEYFRAME_SCALE = True
KEYFRAME_VISIBILITY = True  # Viewport and render visibility.

def create_objects_for_particles(ps, obj):
    # Duplicate the given object for every particle and return the duplicates.
    # Use instances instead of full copies.
    obj_list = []
    mesh = obj.data
    for i, _ in enumerate(ps.particles):
        dupli = bpy.data.objects.new(
                    name="0.{:04d}".format(i),
                    object_data=mesh)
        bpy.context.scene.objects.link(dupli)
        obj_list.append(dupli)
    return obj_list

def match_and_keyframe_objects(ps, obj_list, start_frame, end_frame):
    # Match and keyframe the objects to the particles for every frame in the
    # given range.
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        for p, obj in zip(ps.particles, obj_list):
            match_object_to_particle(p, obj)
            keyframe_obj(obj)

def match_object_to_particle(p, obj):
    # Match the location, rotation, scale and visibility of the object to
    # the particle.
    loc = p.location
    rot = p.rotation
    size = p.size
    if p.alive_state == 'ALIVE':
        vis = True
    else:
        vis = False
    obj.location = loc
    # Set rotation mode to quaternion to match particle rotation.
    obj.rotation_mode = 'XYZ'
    obj.rotation_euler[0] = math.radians(90)
    obj.scale = (size, size, size)
    obj.hide = not(vis)
    obj.hide_render = not(vis)

def keyframe_obj(obj):
    # Keyframe location, rotation, scale and visibility if specified.
    if KEYFRAME_LOCATION:
        obj.keyframe_insert("location")
    if KEYFRAME_ROTATION:
        obj.keyframe_insert("rotation_quaternion")
    if KEYFRAME_SCALE:
        obj.keyframe_insert("scale")
    if KEYFRAME_VISIBILITY:
        obj.keyframe_insert("hide")
        obj.keyframe_insert("hide_render")

def main():
    # Assume only 2 objects are selected.
    # The active object should be the one with the particle system.
    ps_obj = bpy.context.object
    obj = [obj for obj in bpy.context.selected_objects if obj != ps_obj][0]
    ps = ps_obj.particle_systems[0]  # Assume only 1 particle system is present.
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    obj_list = create_objects_for_particles(ps, obj)
    match_and_keyframe_objects(ps, obj_list, start_frame, end_frame)

if __name__ == '__main__':
    main()