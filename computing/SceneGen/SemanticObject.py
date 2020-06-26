import numpy as np
import mathutils
import itertools
from shapely.geometry.polygon import Polygon

#Constants:
ROOM_SCALE = 0.2 # percentage of room dimensions an object has to be to be characterized as close to edge or another object
RAY_SIZE  = 100


def getObjMinMax(obj):
    obj_min_x = min([obj.center[0] - obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0], obj.center[0] - obj.radius[0] * obj.axis1[0] + obj.radius[1] * obj.axis2[0], obj.center[0] + obj.radius[0] * obj.axis1[0] + obj.radius[1]* obj.axis2[0],obj.center[0] + obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0]])
    obj_max_x = max([obj.center[0] - obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0], obj.center[0] - obj.radius[0] * obj.axis1[0] + obj.radius[1]* obj.axis2[0], obj.center[0] + obj.radius[0] * obj.axis1[0] + obj.radius[1]* obj.axis2[0],obj.center[0] + obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0]])
    obj_min_y = min([obj.center[1] - obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1], obj.center[1] - obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1], obj.center[1] + obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1],obj.center[1] + obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1]])
    obj_max_y = max([obj.center[1] - obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1], obj.center[1] - obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1], obj.center[1] + obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1],obj.center[1] + obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1]])
    return obj_min_x, obj_max_x, obj_min_y, obj_max_y

def getRoomInfo(objects):
    objectMinMaxes = [getObjMinMax(obj) for obj in objects]
    min_x = min([o[0] for o in objectMinMaxes])
    max_x = max([o[1] for o in objectMinMaxes])
    min_y = min([o[2] for o in objectMinMaxes])
    max_y = max([o[3] for o in objectMinMaxes])
    room_size = np.sqrt((max_x - min_x) **2 + (max_y - min_y) **2)

    return min_x, max_x, min_y, max_y, room_size

#return minimum x,y distance between 2 rectangles
def min_distance2D(first_obj, second_obj):
    center_1 = np.array(first_obj.center[:2])
    axis1 = np.array(first_obj.axis1[:2]) * first_obj.radius[0]
    axis2 = np.array(first_obj.axis2[:2]) * first_obj.radius[1]

    mm1 = (center_1 - axis1 - axis2)
    pm1 = (center_1 + axis1 - axis2)
    pp1 = (center_1 + axis1 + axis2)
    mp1 = (center_1 - axis1 + axis2)
    corners_first = [mm1, pm1, pp1, mp1]

    center_2 = np.array(second_obj.center[:2])
    axis1 = np.array(second_obj.axis1[:2]) * second_obj.radius[0]
    axis2 = np.array(second_obj.axis2[:2]) * second_obj.radius[1]

    mm2 = (center_2 - axis1 - axis2 )
    pm2 = (center_2 + axis1 - axis2)
    pp2 = (center_2 + axis1 + axis2)
    mp2 = (center_2 - axis1 + axis2)
    corners_second = [mm2, pm2, pp2, mp2]
    return Polygon(corners_second).distance(Polygon(corners_first))

def getObjCorners2D(obj):
    c1 = np.array(obj.center[:2]) +  (+1 * obj.radius[0] * np.array(obj.axis1[:2]) + obj.radius[1] * np.array(obj.axis2[:2]))
    c2 = np.array(obj.center[:2]) +  (+1 * obj.radius[0] * np.array(obj.axis1[:2]) - obj.radius[1] * np.array(obj.axis2[:2]))
    c3 = np.array(obj.center[:2]) +  (-1 * obj.radius[0] * np.array(obj.axis1[:2]) - obj.radius[1] * np.array(obj.axis2[:2]))
    c4 = np.array(obj.center[:2]) +  (-1 * obj.radius[0] * np.array(obj.axis1[:2]) + obj.radius[1] * np.array(obj.axis2[:2]))
    return c1, c2, c3, c4

def getObjMinMax(obj):
    obj_min_x = min([obj.center[0] - obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0], obj.center[0] - obj.radius[0] * obj.axis1[0] + obj.radius[1] * obj.axis2[0], obj.center[0] + obj.radius[0] * obj.axis1[0] + obj.radius[1]* obj.axis2[0],obj.center[0] + obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0]])
    obj_max_x = max([obj.center[0] - obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0], obj.center[0] - obj.radius[0] * obj.axis1[0] + obj.radius[1]* obj.axis2[0], obj.center[0] + obj.radius[0] * obj.axis1[0] + obj.radius[1]* obj.axis2[0],obj.center[0] + obj.radius[0] * obj.axis1[0] - obj.radius[1]* obj.axis2[0]])
    obj_min_y = min([obj.center[1] - obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1], obj.center[1] - obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1], obj.center[1] + obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1],obj.center[1] + obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1]])
    obj_max_y = max([obj.center[1] - obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1], obj.center[1] - obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1], obj.center[1] + obj.radius[0] * obj.axis1[1] + obj.radius[1]* obj.axis2[1],obj.center[1] + obj.radius[0] * obj.axis1[1] - obj.radius[1]* obj.axis2[1]])
    return obj_min_x, obj_max_x, obj_min_y, obj_max_y

def semanticObjectToString(object):
    return '%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%d'%(object.label, object.center[0],object.center[1],object.center[2],object.axis1[0],object.axis1[1],object.axis1[2],object.axis2[0],object.axis2[1],object.axis2[2], object.radius[0], object.radius[1],object.radius[2],object.symmetric)

def containsCenter(first_obj, second_obj):
    center_1 = np.array(first_obj.center[:2])
    axis1 = np.array(first_obj.axis1[:2]) * first_obj.radius[0]
    axis2 = np.array(first_obj.axis2[:2]) * first_obj.radius[1]

    mm1 = (center_1 - axis1 - axis2)
    pm1 = (center_1 + axis1 - axis2)
    pp1 = (center_1 + axis1 + axis2)
    mp1 = (center_1 - axis1 + axis2)
    corners_first = [mm1, pm1, pp1, mp1]

    center_2 = np.array(second_obj.center[:2])
    axis1 = np.array(second_obj.axis1[:2]) * second_obj.radius[0] *0.001
    axis2 = np.array(second_obj.axis2[:2]) * second_obj.radius[1] * 0.001

    mm2 = (center_2 - axis1 - axis2 )
    pm2 = (center_2 + axis1 - axis2)
    pp2 = (center_2 + axis1 + axis2)
    mp2 = (center_2 - axis1 + axis2)
    corners_second = [mm2, pm2, pp2, mp2]
    return Polygon(corners_second).within(Polygon(corners_first))

def insideRoom(first_obj, room_info):
    min_x, max_x, min_y, max_y, _ = room_info
    room = [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]]

    center_1 = np.array(first_obj.center[:2])
    axis1 = np.array(first_obj.axis1[:2]) * first_obj.radius[0]
    axis2 = np.array(first_obj.axis2[:2]) * first_obj.radius[1]

    mm1 = (center_1 - axis1 - axis2)
    pm1 = (center_1 + axis1 - axis2)
    pp1 = (center_1 + axis1 + axis2)
    mp1 = (center_1 - axis1 + axis2)
    corners_first = [mm1, pm1, pp1, mp1]
    return Polygon(corners_first).within(Polygon(room))

def canPut(existing_object, new_object, can_overlap, use_radius = True):
    if existing_object.label in can_overlap.get(new_object.label, can_overlap['other']):
        return True
    if use_radius:
        dist = min_distance2D(existing_object, new_object)
        return dist > 0
    else:
        return not containsCenter(existing_object,new_object)

class SemanticObject():
    def __init__(self, label, center, radius, axis1, axis2, symmetry):
        self.label = label
        self.center = center
        self.radius = radius
        self.axis1 = axis1
        self.axis2 = axis2
        self.is_corner = False
        self.is_middle = False
        self.is_edge = False
        self.is_surrounded_by = {}
        self.distances_by_labels = {}
        self.avg_object_distances = {}
        self.symmetric = symmetry
        self.isFacingObject = {}
        self.nextToObjects = {}
        self.towardsCenter = False
        self.similarDirection = 0
        self.oppositeDirection = 0
        self.otherDirection = 0


    def updateRoomPosition(self, room_info):
        min_x, max_x, min_y, max_y, self.roomSize = room_info
        x_dist = max_x - min_x
        y_dist = max_y - min_y
        obj_min_x, obj_max_x, obj_min_y, obj_max_y = getObjMinMax(self)
        orig = mathutils.Vector([self.center[0], self.center[1]])

        room_corners = [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)]

        axis = np.array(self.axis1[:2])
        ray = orig + RAY_SIZE * mathutils.Vector(axis)
        if ((self.center[0] - min_x) < x_dist * 0.5 and (self.center[1] - min_y) < y_dist * 0.5): #if on bottom left side of the room:
            if mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[1], room_corners[2]) or mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[2], room_corners[3]):
                self.towardsCenter = True
        elif ((self.center[0] - min_x) > x_dist * 0.5 and (self.center[1] - min_y) < y_dist * 0.5): #if on bottom right side of the room:
            if mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[0], room_corners[1]) or mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[1], room_corners[2]):
                self.towardsCenter = True
        elif ((self.center[0] - min_x) > x_dist * 0.5 and (self.center[1] - min_y) > y_dist * 0.5): #if on top right side of the room:
            if mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[0], room_corners[1]) or mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[3], room_corners[0]):
                self.towardsCenter = True
        else: #top left
            if mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[2], room_corners[3]) or mathutils.geometry.intersect_line_line_2d(orig, ray, room_corners[3], room_corners[0]):
                self.towardsCenter = True


        is_lr_side = (obj_min_x - min_x) < x_dist * ROOM_SCALE or (max_x - obj_max_x) < x_dist * ROOM_SCALE
        is_tb_side = (obj_min_y - min_y) < y_dist * ROOM_SCALE or (max_y - obj_max_y) < y_dist * ROOM_SCALE

        if (is_lr_side and is_tb_side):
            self.is_corner = True
        elif (is_lr_side or is_tb_side):
            self.is_edge = True
        else:
            self.is_middle = True

    def updateProximities(self, room_info):
        min_x, max_x, min_y, max_y, self.roomSize = room_info
        x_dist = max_x - min_x
        y_dist = max_y - min_y
        close = np.linalg.norm(self.radius[:2])
        for key, vals in self.distances_by_labels.items():
            self.is_surrounded_by[key] = len([1  for val in vals if val < close])
            self.avg_object_distances[key] = np.mean(vals)

    def update_relationship(self, second_obj):

        rots = []
        for i in range (5):
            theta = np.radians(-15 + 7.5 * i)
            c, s = np.cos(theta), np.sin(theta)
            rots.append(np.array(((c,-s), (s, c))))

        distance = min_distance2D(self, second_obj)
        self.distances_by_labels[second_obj.label] = self.distances_by_labels.get(second_obj.label, []) + [distance]
        close = np.linalg.norm(self.radius[:2])
        #first obj facings if asymmetric!
        if self.symmetric == 2 and distance < close:
            orig = mathutils.Vector(self.center[:2])
            other_center =  mathutils.Vector(second_obj.center[:2])
            v1, v2, v3, v4 = getObjCorners2D(second_obj)
            segments = [(v1, v2), (v2, v3), (v3, v4), (v4, v1)]

            axis = np.array(self.axis1[:2])
            rays = [orig + RAY_SIZE *mathutils.Vector(np.matmul(R, axis)) for R in rots]
            intersections =  False
            for ray in rays:
                for segment in segments:
                    intersection = mathutils.geometry.intersect_line_line_2d(orig, ray, segment[0], segment[1])
                    if intersection is not None and np.linalg.norm(intersection - other_center) < np.linalg.norm(orig - other_center):
                        intersections = True
                        break
                if intersections:
                    break
            if (intersections):
                self.isFacingObject[second_obj.label] = self.isFacingObject.get(second_obj.label, 0) + 1

            axes = [np.array(self.axis2[:2]), -1 * np.array(self.axis2[:2])]
            intersections =  False
            for axis in axes:
                rays = [orig + RAY_SIZE *mathutils.Vector(np.matmul(R, axis)) for R in rots]
                for ray in rays:
                    for segment in segments:
                        intersection = mathutils.geometry.intersect_line_line_2d(orig, ray, segment[0], segment[1])
                        if intersection is not None and np.linalg.norm(intersection - other_center) < np.linalg.norm(orig - other_center):
                            intersections = True
                            break
                    if intersections:
                        break
                if intersections:
                    break
            if (intersections):
                self.nextToObjects[second_obj.label] = self.nextToObjects.get(second_obj.label, 0) + 1

            if  second_obj.symmetric == 2:
                first_angle = np.arctan2(self.axis1[1], self.axis1[0])
                second_angle = np.arctan2(second_obj.axis1[1], second_obj.axis1[0])
                difference = min((first_angle - second_angle)% (np.pi * 2), (second_angle - first_angle)% (np.pi * 2))
                if (difference < np.pi / 4):
                    self.similarDirection += 1
                elif (difference > 3 * np.pi/4):
                    self.oppositeDirection +=1
                else:
                    self.otherDirection += 1

    def getPositionFeatures(self, dist_repeat_objects, surround_repeat_objects, use_room_position, min_distance_missing = 100):
        avg_distances = [(self.avg_object_distances.get(label,  min_distance_missing)) for label in dist_repeat_objects]
        is_surround = [self.is_surrounded_by.get(label, 0) for label in surround_repeat_objects]
        position = [0 if self.is_middle else 1 if self.is_edge else 2] if use_room_position else []
        y = np.array(avg_distances + is_surround + position)
        return y

    def getOrientationFeatures(self, facing_repeat_objects, next_to_repeat_objects, use_center, use_similarity, use_room_position):
        if self.symmetric == 2:
            is_facing = [self.isFacingObject.get(label, 0) for label in facing_repeat_objects]
            is_next_to = [self.nextToObjects.get(label, 0) for label in next_to_repeat_objects]
            center = [1 if self.towardsCenter else 0] if use_center else []
            if use_similarity:
                if all_directions > 0:
                    similarity = [self.similarDirection, self.oppositeDirection]
                else:
                    similarity =  [0, 0]
            else:
                similarity =  []
            position = [0 if self.is_middle else 1 if self.is_edge else 2] if use_room_position else []
            return np.array(is_facing + is_next_to + center + similarity + position)

    def isAwayFromWall(self, room_info):
        min_x, max_x, min_y, max_y, self.roomSize = room_info
        dist_to_min_x = self.center[0] - self.axis1[0] * self.radius[0] - self.axis2[0] * self.radius[1] - min_x
        dist_to_max_x = max_x - (self.center[0] + self.axis1[0] * self.radius[0] + self.axis2[0] * self.radius[1])
        dist_to_min_y = self.center[1] - self.axis1[1] * self.radius[0] - self.axis2[1] * self.radius[1] - min_y
        dist_to_max_y = max_y - (self.center[1] + self.axis1[1] * self.radius[0] + self.axis2[1] * self.radius[1])
        all_distances = [dist_to_min_x, dist_to_max_x, dist_to_min_y, dist_to_max_y]
        e = 0.1
        if dist_to_min_x == min(all_distances) and np.linalg.norm(self.axis1 - np.array([1,0,0])) < e:
            return True
        if dist_to_max_x == min(all_distances) and np.linalg.norm(self.axis1 - np.array([-1, 0,0])) < e:
            return True
        if dist_to_min_y == min(all_distances) and np.linalg.norm(self.axis1 - np.array([0, 1,0])) < e:
            return True
        if dist_to_max_y == min(all_distances) and np.linalg.norm(self.axis1 - np.array([0, -1, 0])) < e:
            return True
