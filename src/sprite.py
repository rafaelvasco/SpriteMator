#--------------------------------------------------
# Name:             Sprite
# Purpose:          Represents a graphic entity composed of Animations which are composed of Frames which are composed
#                   of Surfaces (Layers), which are essentially images represented by QImage class.
#
# Author:           Rafael
# Date:             24/03/13
# License:          
#--------------------------------------------------
import pickle
import os

from PyQt5.QtGui import QPainter

import src.utils as utils
import src.drawing as drawing


class Sprite(object):
    def __init__(self):

        self._animations = []
        self._filePath = ""
        self._currentAnimation = None
        self._currentAnimationIndex = -1

    def current_animation(self):
        return self._currentAnimation

    def current_animation_index(self):
        return self._currentAnimationIndex

    def animations(self):

        return self._animations

    def animation_count(self):

        return len(self._animations)

    # ----- STATIC METHODS ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create(width, height):

        new_sprite = Sprite()
        new_sprite.add_animation()
        new_sprite.current_animation().add_empty_frame(width, height)

        return new_sprite

    @staticmethod
    def load_from_file(file):

        with open(file, 'rb') as spriteFile:
            new_sprite = pickle.load(spriteFile)

        if new_sprite is not None:

            if new_sprite.file_path() != file:
                print('Sprite was moved.. setting new path: ', file)
                new_sprite.set_file_path(file)

            return new_sprite

        raise Exception('[SpriteManager] : Error loading sprite file')

    @staticmethod
    def save(sprite, save_path):

        sprite.set_file_path(save_path)

        with open(save_path, 'wb+') as outFile:
            pickle.dump(sprite, outFile)

    @staticmethod
    def import_from_image_files(image_files):

        new_sprite = Sprite()
        new_sprite.add_animation()

        for imageFile in image_files:
            image = utils.load_image(imageFile)
            new_sprite.current_animation().add_frame(image)

        return new_sprite

    @staticmethod
    def import_from_spritesheet(image):
        pass

    @staticmethod
    def export(sprite, directory):

        created_folder_successfuly = True

        directories = {}

        for animation in sprite.animations():

            directory = utils.make_dir(directory, animation.name())

            if directory is not None:

                directories[animation] = directory

            else:

                created_folder_successfuly = False
                directories.clear()
                break

        if created_folder_successfuly:

            for animation, animationDirectory in directories.items():

                for index, frame in enumerate(animation.frames()):

                    flattened_frame_image = frame.flatten()

                    file_path = os.path.join(animationDirectory, ('frame{0}.png'.format(index)))

                    try:

                        flattened_frame_image.save(file_path, "PNG")

                    except Exception as e:

                        raise e

    @staticmethod
    def export_to_spritesheet(sprite, directory):

        pass

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def file_path(self):
        return self._filePath

    def set_file_path(self, path):
        self._filePath = path

    def set_animation(self, index):

        index = utils.clamp(index, 0, len(self._animations) - 1)

        self._currentAnimationIndex = index
        self._currentAnimation = self._animations[index]

    def animation_at(self, index):
        index = utils.clamp(index, 0, len(self._animations) - 1)
        return self._animations[index]

    def add_animation(self):

        name = 'Animation ' + str(len(self._animations) + 1)
        new_animation = Animation(name)

        if self._currentAnimation is not None:
            new_animation.add_empty_frame(self._currentAnimation.frame_width(), self._currentAnimation.frame_height())

        self._animations.append(new_animation)

        self._currentAnimation = new_animation
        self._currentAnimationIndex += 1

    def remove_current_animation(self):

        del self._animations[self._currentAnimationIndex]

        if self._currentAnimationIndex == len(self._animations) - 1:
            self._currentAnimationIndex -= 1

        self._currentAnimation = self._animations[self._currentAnimationIndex]


class Animation(object):
    def __init__(self, name):

        self._frames = []
        self._currentFrame = None
        self._currentFrameIndex = -1
        self._name = name
        self._frameWidth = 0
        self._frameHeight = 0

    def name(self):
        return self._name

    def set_name(self, text):

        self._name = text

    def frames(self):
        return self._frames

    def frame_width(self):
        return self._frameWidth

    def frame_height(self):
        return self._frameHeight

    def frame_count(self):

        return len(self._frames) if self._frames is not None else 0

    def current_frame(self):
        return self._currentFrame

    def current_frame_index(self):
        return self._currentFrameIndex

    def is_on_last_frame(self):
        return self._currentFrameIndex == len(self._frames) - 1

    def is_on_first_frame(self):
        return self._currentFrameIndex == 0

    def last_frame(self):
        return self._frames[-1]

    def frame_at(self, index):

        index = utils.clamp(index, 0, len(self._frames) - 1)
        return self._frames[index]

    def add_frame(self, image, at=None):

        if self._currentFrameIndex == -1:

            self._frameWidth = image.width()
            self._frameHeight = image.height()

        else:

            if self._frameWidth < image.width() or self._frameHeight < image.height():

                self.resize(image.width(), image.height())

            elif self._frameWidth > image.width() or self._frameHeight > image.height():

                frame_image = utils.create_image(self._frameWidth, self._frameHeight)

                drawing.paste_image(image, frame_image)

                image = frame_image

        new_frame = Frame(self, image)

        if at is None:
            self._frames.append(new_frame)
        else:
            self._frames.insert(at, new_frame)

        self.set_frame(len(self._frames) - 1)

    def add_empty_frame(self, width, height, at=None):

        frame_image = utils.create_image(width, height)
        self.add_frame(frame_image, at)

    def remove_frame(self, index=None):

        if index is None:
            index = self._currentFrameIndex
        else:
            index = utils.clamp(index, 0, len(self._frames) - 1)

        new_index = index

        if self._currentFrameIndex == index:

            if self.is_on_last_frame():
                new_index -= 1

        del self._frames[index]

        if len(self._frames) > 0:

            self.set_frame(new_index)

        else:

            self.set_frame(None)

    def copy_frame(self, index=None):

        if index is None:
            index = self._currentFrameIndex
        else:
            index = utils.clamp(index, 0, len(self._frames) - 1)

        clone = self._frames[index].clone()

        if index < len(self._frames) - 1:

            self._frames.insert(self._currentFrameIndex, clone)

        else:

            self._frames.append(clone)

        self.set_frame(index + 1)

    def set_frame(self, index):

        if index is None:

            self._currentFrame = None
            self._currentFrameIndex = -1
        else:

            index = utils.clamp(index, 0, len(self._frames) - 1)

            self._currentFrame = self._frames[index]
            self._currentFrameIndex = index

    def go_to_next_frame(self):

        self.set_frame(self._currentFrameIndex + 1)

    def go_to_previous_frame(self):

        self.set_frame(self._currentFrameIndex - 1)

    def resize(self, width, height):

        for frame in self._frames:
            frame.resize(width, height)

        self._frameWidth = width
        self._frameHeight = height


class Frame(object):
    def __init__(self, animation, image=None):

        self._surfaces = []
        self._currentSurface = None
        self._currentSurfaceIndex = -1
        self._animation = animation

        if image is not None:
            self.add_surface(image)

    def surfaces(self):
        return self._surfaces

    def surface_count(self):
        return len(self._surfaces)

    def surface_at(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)
        return self._surfaces[index]

    def set_surface(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)

        self._currentSurfaceIndex = index
        self._currentSurface = self._surfaces[index]

    def add_empty_surface(self, width, height, at=None):

        surface_image = utils.create_image(width, height)
        self.add_surface(surface_image, at)

    def add_surface(self, image, at=None):

        sid = len(self._surfaces)

        new_surface = Surface(image, 'Layer ' + str(sid))
        new_surface._id = sid

        if new_surface.width() > self._animation.frame_width() or new_surface.height() > self._animation.frame_height():
            self._animation.resize(new_surface.width(), new_surface.height())

        if at is None:
            self._surfaces.append(new_surface)
        else:
            self._surfaces.append(new_surface)

        self._currentSurface = new_surface
        self._currentSurfaceIndex += 1

    def remove_surface(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)

        del self._surfaces[index]

        if self._currentSurfaceIndex == index:

            if self._currentSurfaceIndex > 0:
                self._currentSurfaceIndex -= 1

            self._currentSurface = self._surfaces[self._currentSurfaceIndex]

    def move_surface(self, from_index, to_index):

        self._surfaces.insert(to_index, self._surfaces.pop(from_index))

        index = 0
        for surface in self._surfaces:
            if surface.id() == self._currentSurface.id():
                self._currentSurfaceIndex = index
                break

            index += 1

        self._currentSurface = self._surfaces[self._currentSurfaceIndex]

    def current_surface(self):
        return self._currentSurface

    def current_surface_index(self):
        return self._currentSurfaceIndex

    def flatten(self):

        if len(self._surfaces) == 1:
            return self._surfaces[0].image()

        flattened_image = utils.create_image(self._animation.frame_width(), self._animation.frame_height())

        painter = QPainter()
        painter.begin(flattened_image)

        for surface in self._surfaces:
            painter.drawImage(0, 0, surface.image())

        painter.end()

        return flattened_image

    def resize(self, width, height):

        for surface in self._surfaces:
            surface.resize(width, height)

    def scale_to_size(self, width, height):

        for surface in self._surfaces:
            old_width = surface.width()
            old_height = surface.height()

            surface.scale(width / old_width, height / old_height)

    def scale_to_factor(self, factor):

        for surface in self._surfaces:
            surface.scale(factor, factor)

    def clone(self):

        clone = Frame(self._animation)

        for surface in self._surfaces:
            clone.add_surface(surface.image().copy())

        return clone


class Surface(object):
    def __init__(self, image, name):
        self._image = image
        self._name = name
        self._bytes = None
        self._id = 0

    def width(self):
        return self._image.width() if self._image is not None else 0

    def height(self):
        return self._image.height() if self._image is not None else 0

    def image(self):
        return self._image

    def name(self):
        return self._name

    def id(self):
        return self._id

    def resize(self, width, height):
        new_image = utils.create_image(width, height)

        painter = QPainter(new_image)

        painter.drawImage(0, 0, self._image)

        self._image = new_image

    def scale(self, scale_x, scale_y):
        cur_width = self.width()
        cur_height = self.height()

        new_width = cur_width * scale_x
        new_height = cur_height * scale_y

        self._image = self._image.scaled(new_width, new_height)

    def __getstate__(self):
        if self._bytes is None or self._bytes.isEmpty():
            self._bytes = utils.image_to_bytearray(self._image)

        state = self.__dict__.copy()

        del state['_image']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._image = utils.byte_array_to_image(self._bytes)
        self._bytes.clear()

