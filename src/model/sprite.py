# --------------------------------------------------------------------------------------------------
# Name:             Sprite
# Purpose:          Represents a graphic entity composed of Animations which are composed of Frames
#                   which are composed of Surfaces (Layers) that can be edited by the Canvas
#
# Author:           Rafael
# Date:             24/03/13
# License:          
#--------------------------------------------------------------------------------------------------
import pickle
import os

from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QPainter

import src.helpers.utils as utils
import src.helpers.cropper as cropper
import src.model.appdata as appdata
from src.helpers.packer import RectanglePacker


class Sprite(object):
    def __init__(self, width, height):

        self._width = width
        self._height = height
        self._animations = []
        self._filePath = ""
        self._currentAnimationIndex = -1

    @property
    def file_path(self):
        return self._filePath

    @file_path.setter
    def file_path(self, value):
        self._filePath = value

    @property
    def active_surface(self):
        return self.current_animation.current_frame.current_surface.image

    @property
    def active_surface_pixel_data(self):

        return self.current_animation.current_frame.current_surface.pixel_data

    @property
    def current_animation(self):

        if self._currentAnimationIndex == -1:
            return None

        return self._animations[self._currentAnimationIndex]

    @property
    def current_animation_index(self):
        return self._currentAnimationIndex

    @property
    def animations(self):
        return self._animations

    @property
    def animation_count(self):
        return len(self._animations)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def size(self):
        return QSize(self._width, self._height)

    # =========================================================================

    def animation_at(self, index):

        index = utils.clamp(index, 0, len(self._animations) - 1)
        return self._animations[index]

    def resize(self, width, height):

        self._width = width
        self._height = height

        for animation in self._animations:

            for frame in animation.frames:
                frame.resize(width, height)

    def scale(self, scale_width, scale_height=None):

        self._width = int(round(self._width * scale_width))
        self._height = int(round(self._height * scale_height))

        if scale_height is None:
            scale_height = scale_width

        for animation in self._animations:

            for frame in animation.frames():
                frame.scale(scale_width, scale_height)

    def paste_image(self, image):

        self.current_animation.current_frame.paste_image(image)

    # ----- STATIC METHODS ------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    @staticmethod
    def create(width, height):

        new_sprite = Sprite(width, height)
        new_sprite.add_animation()
        new_sprite.current_animation.add_empty_frame()
        return new_sprite

    @staticmethod
    def load_from_file(file):

        with open(file, 'rb') as spriteFile:
            new_sprite = pickle.load(spriteFile)

        if new_sprite is not None:

            if new_sprite.file_path != file:
                new_sprite.file_path = file

            return new_sprite

        raise Exception('[SpriteManager] : Error loading sprite file')

    @staticmethod
    def save(sprite, save_path):

        sprite.file_path = save_path

        with open(save_path, 'wb+') as outFile:
            pickle.dump(sprite, outFile)

    @staticmethod
    def import_from_image_files(image_files):

        biggest_width = 0
        biggest_height = 0

        image_list = []

        for imageFile in image_files:
            image = utils.load_image(imageFile)
            image_list.append(image)

            if image.width() > biggest_width:
                biggest_width = image.width()
            if image.height() > biggest_height:
                biggest_height = image.height()

        new_sprite = Sprite(biggest_width, biggest_height)
        new_sprite.add_animation()

        for image in image_list:
            new_sprite.current_animation.add_frame(image)

        return new_sprite

    @staticmethod
    def import_from_spritesheet(image):
        pass

    @staticmethod
    def export(sprite, directory):

        created_folder_successfuly = True

        directories = {}

        for animation in sprite.animations:

            directory = utils.make_directory(directory, animation.name)

            if directory is not None:

                directories[animation] = directory

            else:

                created_folder_successfuly = False
                directories.clear()
                break

        if created_folder_successfuly:

            for animation, animationDirectory in directories.items():

                for index, frame in enumerate(animation.frames):

                    flattened_frame_image = frame.flatten()

                    flattened_frame_image = cropper.crop(flattened_frame_image)

                    file_path = os.path.join(animationDirectory, ('frame{0}.png'.format(index)))

                    try:

                        flattened_frame_image.save(file_path, "PNG")

                    except Exception as e:

                        raise e

    @staticmethod
    def export_to_spritesheet(sprite, directory):

        packer = RectanglePacker(appdata.max_texture_size, appdata.max_texture_size)

        animation = sprite.animations[0]

        frames = animation.frames

        cropped_images = []

        spritesheet_regions = []

        for frame in frames:
            flattened_frame_image = frame.flatten()

            cropped_frame_image = cropper.crop(flattened_frame_image)

            cropped_images.append(cropped_frame_image)

        images_remaining = len(cropped_images)

        while images_remaining > 0:

            for image in cropped_images:

                image_width = image.width()
                image_height = image.height()

                point = packer.pack(image_width, image_height)

                if point is None:
                    raise Exception("Can't fit all sprite frames. Max image size is 4096x4096.")

                images_remaining -= 1

                spritesheet_regions.append((image, point))

        spritesheet = utils.create_image(packer.actual_packing_area_width(),
                                         packer.actual_packing_area_height())
        painter = QPainter()

        painter.begin(spritesheet)

        for sprRegion in spritesheet_regions:
            spr_image = sprRegion[0]
            target_point = QPoint(sprRegion[1].x, sprRegion[1].y)

            painter.drawImage(target_point, spr_image)

        painter.end()

        file_path = os.path.join(directory, ('{0}Sheet.png'.format(animation.name)))

        try:

            spritesheet.save(file_path, "PNG")

        except Exception as e:

            raise e

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    def set_animation(self, index):

        index = utils.clamp(index, 0, len(self._animations) - 1)

        self._currentAnimationIndex = index

    def add_animation(self):

        name = 'Animation ' + str(len(self._animations) + 1)
        new_animation = Animation(name, self)

        self._animations.append(new_animation)

        self._currentAnimationIndex = len(self._animations) - 1

    def remove_current_animation(self):

        previous_length = len(self._animations)

        del self._animations[self._currentAnimationIndex]

        if len(self._animations) > 0 and self._currentAnimationIndex == previous_length - 1:
            self._currentAnimationIndex -= 1

        elif len(self._animations) == 0:

            self.add_animation()


class Animation(object):
    def __init__(self, name, sprite):

        self._frames = []
        self._current_frameIndex = -1
        self._name = name
        self._frameWidth = 0
        self._frameHeight = 0
        self._sprite = sprite

    @property
    def sprite(self):
        return self._sprite

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def frame_width(self):
        return self._frameWidth

    @property
    def frame_height(self):
        return self._frameHeight

    @property
    def frames(self):
        return self._frames

    @property
    def frame_count(self):
        return len(self._frames)

    @property
    def current_frame(self):

        if self._current_frameIndex == -1:
            return None

        return self._frames[self._current_frameIndex]

    @property
    def current_frame_index(self):
        return self._current_frameIndex

    @property
    def is_on_last_frame(self):
        return self._current_frameIndex == len(self._frames) - 1

    @property
    def is_on_first_frame(self):
        return self._current_frameIndex == 0

    @property
    def last_frame(self):
        return self._frames[-1]

    def frame_at(self, index):

        index = utils.clamp(index, 0, len(self._frames) - 1)
        return self._frames[index]

    def add_frame(self, image, at=None):

        if self._current_frameIndex == -1:

            self._frameWidth = image.width()
            self._frameHeight = image.height()

        else:

            if self._frameWidth < image.width() or self._frameHeight < image.height():
                self._sprite.resize(image.width(), image.height())

        new_frame = Frame(self, image)

        if at is None:
            self._frames.append(new_frame)
        else:
            self._frames.insert(at, new_frame)

        self.set_frame(len(self._frames) - 1)

    def add_empty_frame(self, at=None):

        frame_image = utils.create_image(self._sprite.width, self._sprite.height)
        self.add_frame(frame_image, at)

    def remove_frame(self, index=None):

        if index is None:
            index = self._current_frameIndex
        else:
            index = utils.clamp(index, 0, len(self._frames) - 1)

        new_index = index

        if self._current_frameIndex == index:

            if self.is_on_last_frame:
                new_index -= 1

        del self._frames[index]

        if len(self._frames) > 0:

            self.set_frame(new_index)

        else:

            self.set_frame(None)

    def copy_frame(self, index=None):

        if index is None:
            index = self._current_frameIndex
        else:
            index = utils.clamp(index, 0, len(self._frames) - 1)

        clone = self._frames[index].clone()

        if index < len(self._frames) - 1:

            self._frames.insert(self._current_frameIndex, clone)

        else:

            self._frames.append(clone)

        self.set_frame(index + 1)

    def set_frame(self, index):

        if index is None:

            self._current_frameIndex = -1

        else:

            index = utils.clamp(index, 0, len(self._frames) - 1)
            self._current_frameIndex = index

    def go_to_next_frame(self):

        self.set_frame(self._current_frameIndex + 1)

    def go_to_previous_frame(self):

        self.set_frame(self._current_frameIndex - 1)


class Frame(object):
    def __init__(self, animation, image=None):

        self._surfaces = []
        self._current_surface_index = -1
        self._animation = animation

        if image is not None:
            self.add_surface(image)

    @property
    def surfaces(self):
        return self._surfaces

    @property
    def surface_count(self):
        return len(self._surfaces)

    @property
    def current_surface(self):

        if self._current_surface_index == -1:
            return None

        return self._surfaces[self._current_surface_index]

    @property
    def current_surface_index(self):
        return self._current_surface_index

    def surface_at(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)
        return self._surfaces[index]

    def set_surface(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)

        self._current_surface_index = index

    def add_empty_surface(self, at=None):

        surface_image = utils.create_image(self._animation.sprite.width,
                                           self._animation.sprite.height)
        self.add_surface(surface_image, at)

    def paste_image(self, image):

        if image.width() > self._animation.sprite.width or image.height() > \
                self._animation.sprite.height:
            self._animation.sprite.resize(image.width(), image.height())

        self.current_surface.paste(image)

    def add_surface(self, image, at=None):

        sid = len(self._surfaces)

        frame_width = self._animation.sprite.width
        frame_height = self._animation.sprite.height

        if image.width() > frame_width or image.height() > frame_height:
            frame_width = image.width()
            frame_height = image.height()

            self._animation.sprite.resize(frame_width, frame_height)

        new_surface = Surface('Layer ' + str(sid), frame_width, frame_height)

        new_surface.paste(image)

        new_surface._id = sid

        if at is None:
            self._surfaces.append(new_surface)
        else:
            self._surfaces.append(new_surface)

        self._current_surface_index = len(self._surfaces) - 1

    def remove_current_surface(self):

        previous_length = len(self._surfaces)

        del self._surfaces[self._current_surface_index]

        if len(self._surfaces) > 0 and self._current_surface_index == previous_length - 1:
            self._current_surface_index -= 1

        elif len(self._surfaces) == 0:

            self.add_empty_surface()

    def move_surface(self, from_index, to_index):

        self._surfaces.insert(to_index, self._surfaces.pop(from_index))

        index = 0
        for surface in self._surfaces:
            if surface.id == self.current_surface.id:
                self._current_surface_index = index
                break

            index += 1

    def clone(self):

        clone = Frame(self._animation)

        for surface in self._surfaces:
            clone.add_surface(surface.image.copy())

        return clone

    def flatten(self):

        if len(self._surfaces) == 1:
            return self._surfaces[0].image

        flattened_image = utils.create_image(self._animation.frame_width(),
                                             self._animation.frame_height())

        painter = QPainter()
        painter.begin(flattened_image)

        for surface in self._surfaces:
            painter.drawImage(0, 0, surface.image)

        painter.end()

        return flattened_image

    def resize(self, width, height):

        for surface in self._surfaces:
            surface.resize(width, height)

    def scale(self, scale_width, scale_height):

        for surface in self._surfaces:
            surface.scale(scale_width, scale_height)


class Surface(object):
    def __init__(self, name, width, height):
        self._image = utils.create_image(width, height)
        self._pixelData = self._image.bits()
        self._pixelData.setsize(self._image.byteCount())

        self._byteArray = None

        self._name = name
        self._id = 0
        self._opacity = 1.0

    @property
    def width(self):
        return self._image.width() if self._image is not None else 0

    @property
    def height(self):
        return self._image.height() if self._image is not None else 0

    @property
    def image(self):
        return self._image

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def pixel_data(self):
        return self._pixelData

    def resize(self, width, height):

        new_image = utils.create_image(width, height)

        painter = QPainter(new_image)

        painter.drawImage(0, 0, self._image)

        self._image = new_image

        self._resize_pixel_buffer()

    def scale(self, scale_width, scale_height):

        cur_width = self.width()
        cur_height = self.height()

        new_width = cur_width * scale_width
        new_height = cur_height * scale_height

        self._image = self._image.scaled(new_width, new_height)

        self._resize_pixel_buffer()

    def paste(self, image, x=None, y=None):

        painter = QPainter(self._image)

        if x is None:
            x = self._image.width() // 2 - image.width() // 2

        if y is None:
            y = self._image.height() // 2 - image.height() // 2

        painter.drawImage(x, y, image)

    def _resize_pixel_buffer(self):

        self._pixelData = self._image.bits()
        self._pixelData.setsize(self._image.byteCount())

    def __getstate__(self):
        if self._byteArray is None or self._byteArray.is_empty():
            self._byteArray = utils.image_to_byte_array(self._image)

        state = self.__dict__.copy()

        del state['_image']
        del state['_pixelData']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._image = utils.byte_array_to_image(self._byteArray)
        self._byteArray.clear()