#--------------------------------------------------
# Name:             Sprite
# Purpose:          Represents a graphic entity composed of Animations which are composed of Frames which are composed
#                   of Surfaces (Layers) that can be edited by the Canvas
#
# Author:           Rafael
# Date:             24/03/13
# License:          
#--------------------------------------------------
import pickle
import os

from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QPainter

import src.utils as utils
import src.cropper as cropper
import src.appdata as appdata
from src.packer import RectanglePacker


class Sprite(object):

    def __init__(self, width, height):

        self._width = width
        self._height = height
        self._animations = []
        self._filePath = ""
        self._currentAnimationIndex = -1


    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, value):
        self._filePath = value

    @property
    def activeSurface(self):
        return self.currentAnimation.currentFrame.currentSurface.image

    def activeSurfacePixelData(self):
        return self.currentAnimation.currentFrame.currentSurface.bytes

    @property
    def currentAnimation(self):

        if self._currentAnimationIndex == -1:
            return None

        return self._animations[self._currentAnimationIndex]

    @property
    def currentAnimationIndex(self):
        return self._currentAnimationIndex

    @property
    def animations(self):
        return self._animations

    @property
    def animationCount(self):
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

    def animationAt(self, index):

        index = utils.clamp(index, 0, len(self._animations) - 1)
        return self._animations[index]


    def resize(self, width, height):

        self._width = width
        self._height = height

        for animation in self._animations:

            for frame in animation.frames():

                frame.resize(width, height)


    def scale(self, scale_width, scale_height=None):

        self._width = int(round(self._width * scale_width))
        self._height = int(round(self._height * scale_height))

        if scale_height is None:

            scale_height = scale_width

        for animation in self._animations:

            for frame in animation.frames():

                frame.scale(scale_width, scale_height)


    def pasteImage(self, image):

        self.currentAnimation.currentFrame.pasteImage(image)


    # ----- STATIC METHODS ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create(width, height):

        new_sprite = Sprite(width, height)
        new_sprite.addAnimation()
        return new_sprite

    @staticmethod
    def loadFromFile(file):

        with open(file, 'rb') as spriteFile:
            new_sprite = pickle.load(spriteFile)

        if new_sprite is not None:

            if new_sprite.filePath != file:
                new_sprite.filePath = file

            return new_sprite

        raise Exception('[SpriteManager] : Error loading sprite file')

    @staticmethod
    def save(sprite, save_path):

        sprite.filePath = save_path

        with open(save_path, 'wb+') as outFile:
            pickle.dump(sprite, outFile)

    @staticmethod
    def importFromImageFiles(image_files):

        biggest_width = 0
        biggest_height = 0

        image_list = []

        for imageFile in image_files:
            image = utils.loadImage(imageFile)
            image_list.append(image)

            if image.width() > biggest_width:
                biggest_width = image.width()
            if image.height() > biggest_height:
                biggest_height = image.height()

        new_sprite = Sprite(biggest_width, biggest_height)
        new_sprite.addAnimation()

        for image in image_list:

            new_sprite.currentAnimation.add_frame(image)

        return new_sprite

    @staticmethod
    def importFromSpritesheet(image):
        pass

    @staticmethod
    def export(sprite, directory):

        created_folder_successfuly = True

        directories = {}

        for animation in sprite.animations:

            directory = utils.makeDirectory(directory, animation.name)

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
    def exportToSpritesheet(sprite, directory):

        packer = RectanglePacker(appdata.max_texture_size,appdata.max_texture_size)

        animation = sprite.animations[0]

        frames = animation.frames

        croppedImages = []

        spriteSheetRegions = []

        for frame in frames:

            flattenedFrameImage = frame.flatten()

            croppedFrameImage = cropper.crop(flattenedFrameImage)

            croppedImages.append(croppedFrameImage)

        imagesRemaining = len(croppedImages)

        while imagesRemaining > 0:

            for image in croppedImages:

                imageWidth = image.width()
                imageHeight = image.height()

                point = packer.pack(imageWidth, imageHeight)

                if point is None:

                    raise Exception("Can't fit all sprite frames. Max image size is 4096x4096.")

                imagesRemaining -= 1

                spriteSheetRegions.append((image, point))

        spriteSheet = utils.createImage(packer.actual_packing_area_width(),
                                        packer.actual_packing_area_height())
        painter = QPainter()

        painter.begin(spriteSheet)

        for sprRegion in spriteSheetRegions:

            sprImage = sprRegion[0]
            targetPoint = QPoint(sprRegion[1].x, sprRegion[1].y)

            painter.drawImage(targetPoint, sprImage)

        painter.end()

        file_path = os.path.join(directory, ('{0}Sheet.png'.format(animation.name)))

        try:

            spriteSheet.save(file_path, "PNG")

        except Exception as e:

            raise e

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def setAnimation(self, index):

        index = utils.clamp(index, 0, len(self._animations) - 1)

        self._currentAnimationIndex = index


    def addAnimation(self):

        name = 'Animation ' + str(len(self._animations) + 1)
        new_animation = Animation(name, self)
        new_animation.addEmptyFrame()

        self._animations.append(new_animation)

        self._currentAnimationIndex = len(self._animations) - 1

    def removeCurrentAnimation(self):

        previous_length = len(self._animations)

        del self._animations[self._currentAnimationIndex]


        if len(self._animations) > 0 and self._currentAnimationIndex == previous_length - 1:
                self._currentAnimationIndex -= 1

        elif len(self._animations) == 0:

            self.addAnimation()


class Animation(object):

    def __init__(self, name, sprite):

        self._frames = []
        self._currentFrameIndex = -1
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
    def frameWidth(self):
        return self._frameWidth

    @property
    def frameHeight(self):
        return self._frameHeight

    @property
    def frames(self):
        return self._frames

    @property
    def frameCount(self):
        return len(self._frames)

    @property
    def currentFrame(self):

        if self._currentFrameIndex == -1:
            return None

        return self._frames[self._currentFrameIndex]

    @property
    def currentFrameIndex(self):
        return self._currentFrameIndex

    @property
    def isOnLastFrame(self):
        return self._currentFrameIndex == len(self._frames) - 1

    @property
    def isOnFirstFrame(self):
        return self._currentFrameIndex == 0

    @property
    def lastFrame(self):
        return self._frames[-1]

    def frameAt(self, index):

        index = utils.clamp(index, 0, len(self._frames) - 1)
        return self._frames[index]

    def addFrame(self, image, at=None):

        if self._currentFrameIndex == -1:

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

        self.setFrame(len(self._frames) - 1)

    def addEmptyFrame(self, at=None):

        frame_image = utils.createImage(self._sprite.width, self._sprite.height)
        self.addFrame(frame_image, at)

    def removeFrame(self, index=None):

        if index is None:
            index = self._currentFrameIndex
        else:
            index = utils.clamp(index, 0, len(self._frames) - 1)

        new_index = index

        if self._currentFrameIndex == index:

            if self.isOnLastFrame:
                new_index -= 1

        del self._frames[index]

        if len(self._frames) > 0:

            self.setFrame(new_index)

        else:

            self.setFrame(None)

    def copyFrame(self, index=None):

        if index is None:
            index = self._currentFrameIndex
        else:
            index = utils.clamp(index, 0, len(self._frames) - 1)

        clone = self._frames[index].clone()

        if index < len(self._frames) - 1:

            self._frames.insert(self._currentFrameIndex, clone)

        else:

            self._frames.append(clone)

        self.setFrame(index + 1)

    def setFrame(self, index):

        if index is None:

            self._currentFrameIndex = -1

        else:

            index = utils.clamp(index, 0, len(self._frames) - 1)
            self._currentFrameIndex = index

    def goToNextFrame(self):

        self.setFrame(self._currentFrameIndex + 1)

    def goToPreviousFrame(self):

        self.setFrame(self._currentFrameIndex - 1)


class Frame(object):

    def __init__(self, animation, image=None):

        self._surfaces = []
        self._currentSurfaceIndex = -1
        self._animation = animation

        if image is not None:
            self.addSurface(image)

    @property
    def surfaces(self):
        return self._surfaces

    @property
    def surfaceCount(self):
        return len(self._surfaces)

    @property
    def currentSurface(self):

        if self._currentSurfaceIndex == -1:
            return None

        return self._surfaces[self._currentSurfaceIndex]

    @property
    def currentSurfaceIndex(self):
        return self._currentSurfaceIndex


    def surfaceAt(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)
        return self._surfaces[index]

    def setSurface(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)

        self._currentSurfaceIndex = index

    def addEmptySurface(self, at=None):

        surface_image = utils.createImage(self._animation.sprite.width, self._animation.sprite.height)
        self.addSurface(surface_image, at)

    def pasteImage(self, image):

        if image.width() > self._animation.sprite.width or image.height() > self._animation.sprite.height:

            self._animation.sprite.resize(image.width(), image.height())

        self.currentSurface.paste(image)

    def addSurface(self, image, at=None):

        sid = len(self._surfaces)

        frame_width = self._animation.sprite.width
        frame_height = self._animation.sprite.height

        if image.width() > frame_width or image.height() > frame_height:

            frame_width = image.width()
            frame_height = image.height()

            self._animation.sprite.resize(frame_height, frame_height)

        new_surface = Surface('Layer ' + str(sid), frame_width, frame_height)

        new_surface.paste(image)

        new_surface._id = sid

        if at is None:
            self._surfaces.append(new_surface)
        else:
            self._surfaces.append(new_surface)

        self._currentSurfaceIndex = len(self._surfaces) - 1

    def removeCurrentSurface(self):

        previous_length = len(self._surfaces)

        del self._surfaces[self._currentSurfaceIndex]

        if len(self._surfaces) > 0 and self._currentSurfaceIndex == previous_length - 1:
                self._currentSurfaceIndex -= 1

        elif len(self._surfaces) == 0:

            self.addEmptySurface()

    def moveSurface(self, from_index, to_index):

        self._surfaces.insert(to_index, self._surfaces.pop(from_index))

        index = 0
        for surface in self._surfaces:
            if surface.id == self.currentSurface.id:
                self._currentSurfaceIndex = index
                break

            index += 1


    def clone(self):

        clone = Frame(self._animation)

        for surface in self._surfaces:
            clone.addSurface(surface.image.copy())

        return clone

    def flatten(self):

        if len(self._surfaces) == 1:
            return self._surfaces[0].image

        flattened_image = utils.createImage(self._animation.frame_width(), self._animation.frame_height())

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
        self._image = utils.createImage(width, height)
        self._name = name
        self._bytes = None
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
    def bytes(self):
        return self._bytes


    def resize(self, width, height):

        new_image = utils.createImage(width, height)

        painter = QPainter(new_image)

        painter.drawImage(0, 0, self._image)

        self._image = new_image

    def scale(self, scale_width, scale_height):

        cur_width = self.width()
        cur_height = self.height()

        new_width = cur_width * scale_width
        new_height = cur_height * scale_height

        self._image = self._image.scaled(new_width, new_height)

    def paste(self, image, x=None, y=None):

        painter = QPainter(self._image)

        if x is None:

            x = self._image.width() // 2 - image.width() // 2

        if y is None:

            y = self._image.height() // 2 - image.height() // 2

        painter.drawImage(x, y, image)

    def __getstate__(self):
        if self._bytes is None or self._bytes.isEmpty():
            self._bytes = utils.imageToByteArray(self._image)

        state = self.__dict__.copy()

        del state['_image']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._image = utils.byteArrayToImage(self._bytes)
        self._bytes.clear()