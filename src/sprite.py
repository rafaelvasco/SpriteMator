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

from PyQt4.QtGui import QPainter

import src.utils as utils

import src.drawing as drawing


class Sprite(object):

    def __init__(self):

        self._animations = []
        self._filePath = ""
        self._currentAnimation = None
        self._currentAnimationIndex = -1

    def currentAnimation(self):
        return self._currentAnimation
    
    def currentAnimationIndex(self):
        return self._currentAnimationIndex
    
    def animations(self):
        
        return self._animations
    
    def animationCount(self):
        
        return len(self._animations)
    
    # ----- STATIC METHODS ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create(width, height):

        newSprite = Sprite()
        newSprite.addAnimation()
        newSprite.currentAnimation().addEmptyFrame(width, height)

        return newSprite

    @staticmethod
    def loadFromFile(file):

        with open(file, 'rb') as spriteFile:
            newSprite = pickle.load(spriteFile)

        if newSprite is not None:

            if newSprite.filePath() != file:
                print('Sprite was moved.. setting new path: ', file)
                newSprite.setFilePath(file)

            return newSprite

        raise Exception('[SpriteManager] : Error loading sprite file')

    @staticmethod
    def save(sprite, savePath):

        sprite.setFilePath(savePath)

        with open(savePath, 'wb+') as outFile:
            pickle.dump(sprite, outFile)

   

    @staticmethod
    def importFromImageFiles(imageFiles):

        newSprite = Sprite()
        newSprite.addAnimation()

        for imageFile in imageFiles:
            image = utils.loadImage(imageFile)
            newSprite.currentAnimation().addFrame(image)

        return newSprite

    @staticmethod
    def importFromSpritesheet(image):
        pass

    @staticmethod
    def export(sprite, directory):
        
        createdFolderSuccessfuly = True
        
        directories = {}
        
        for animation in sprite.animations():
            
            directory = utils.makeDir(directory, animation.name())
            
            if(directory is not None):
                
                directories[animation] = directory
                
            else:
                
                createdFolderSuccessfuly = False
                directories.clear()
                break
                
                
        
        if createdFolderSuccessfuly:
            
            for animation, animationDirectory in directories.items():
                
                for index, frame in enumerate(animation.frames()):
                    
                    flattenedFrameImage = frame.flatten()
                    
                    filePath = os.path.join(animationDirectory, ('frame{0}.png'.format(index)))
                    
                    try:
                    
                        flattenedFrameImage.save(filePath, "PNG")
                    
                    except Exception as e:
                        
                        raise e
                        
        

    @staticmethod
    def exportToSpritesheet(sprite, directory):
        
        pass
                

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def filePath(self):
        return self._filePath

    def setFilePath(self, path):
        self._filePath = path

    def setAnimation(self, index):

        index = utils.clamp(index, 0, len(self._animations) - 1)

        self._currentAnimationIndex = index
        self._currentAnimation = self._animations[index]

    def animationAt(self, index):
        index = utils.clamp(index, 0, len(self._animations) - 1)
        return self._animations[index]

    def addAnimation(self):

        name = 'Animation ' + str(len(self._animations)+1)
        newAnimation = Animation(name)

        if self._currentAnimation is not None:

            newAnimation.addEmptyFrame(self._currentAnimation.frameWidth(), self._currentAnimation.frameHeight())

        self._animations.append(newAnimation)
        
        self._currentAnimation = newAnimation
        self._currentAnimationIndex += 1
        
    def removeCurrentAnimation(self):
        
        del self._animations[self._currentAnimationIndex]
        
        if self._currentAnimationIndex == len(self._animations) - 1 :
            
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

    def setName(self, text):
        
        self._name = text

    def frames(self):
        return self._frames
    
    def frameWidth(self):
        return self._frameWidth

    def frameHeight(self):
        return self._frameHeight

    def frameCount(self):

        return len(self._frames) if self._frames is not None else 0

    def currentFrame(self):
        return self._currentFrame

    def currentFrameIndex(self):
        return self._currentFrameIndex

    def isOnLastFrame(self):
        return self._currentFrameIndex == len(self._frames) - 1

    def isOnFirstFrame(self):
        return self._currentFrameIndex == 0

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

                self.resize(image.width(), image.height())
                
            elif self._frameWidth > image.width() or self._frameHeight > image.height():
                
                frameImage = utils.createImage(self._frameWidth, self._frameHeight)
                
                drawing.pasteImage(image, frameImage)
                
                image = frameImage
                

        newFrame = Frame(self, image)

        if at is None:
            self._frames.append(newFrame)
        else:
            self._frames.insert(at, newFrame)

        
        self.setFrame(len(self._frames) - 1)

    def addEmptyFrame(self, width, height, at=None):

        frameImage = utils.createImage(width, height)
        self.addFrame(frameImage,at)

    def removeFrame(self, index=None):

        if index is None:
            index = self._currentFrameIndex
        else:
            index = utils.clamp(index, 0, len(self._frames) - 1)
        
        newIndex = index
        
        if self._currentFrameIndex == index:

            if self.isOnLastFrame():
                newIndex -= 1

        del self._frames[index]

        if len(self._frames) > 0:
            
            self.setFrame(newIndex)

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
            
            self._currentFrame = None
            self._currentFrameIndex = -1
        else:
            
            index = utils.clamp(index, 0, len(self._frames) - 1)
    
            self._currentFrame = self._frames[index]
            self._currentFrameIndex = index

    def goToNextFrame(self):

        self.setFrame(self._currentFrameIndex+1)

    def goToPreviousFrame(self):

        self.setFrame(self._currentFrameIndex-1)

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

            self.addSurface(image)
    
    
    
    def surfaces(self):
        return self._surfaces

    def surfaceCount(self):
        return len(self._surfaces)

    def surfaceAt(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)
        return self._surfaces[index]

    def setSurface(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)

        self._currentSurfaceIndex = index
        self._currentSurface = self._surfaces[index]

    def addEmptySurface(self, width, height, at=None):

        surfaceImage = utils.createImage(width, height)
        self.addSurface(surfaceImage, at)

    def addSurface(self, image, at=None):

        sid = len(self._surfaces)

        newSurface = Surface(image, 'Layer ' + str(sid))
        newSurface._id = sid

        if newSurface.width() > self._animation.frameWidth() or newSurface.height() > self._animation.frameHeight():

            self._animation.resize(newSurface.width(), newSurface.height())


        if at is None:
            self._surfaces.append(newSurface)
        else:
            self._surfaces.append(newSurface)

        self._currentSurface = newSurface
        self._currentSurfaceIndex += 1

    def deleteSurface(self, index):

        index = utils.clamp(index, 0, len(self._surfaces) - 1)

        del self._surfaces[index]

        if self._currentSurfaceIndex == index:

            if self._currentSurfaceIndex > 0:
                self._currentSurfaceIndex -= 1

            self._currentSurface = self._surfaces[self._currentSurfaceIndex]

    def moveSurface(self, fromIndex, toIndex):

        self._surfaces.insert(toIndex, self._surfaces.pop(fromIndex))

        index = 0
        for surface in self._surfaces:
            if surface._id == self._currentSurface._id:
                self._currentSurfaceIndex = index
                break

            index += 1


        self._currentSurface = self._surfaces[self._currentSurfaceIndex]

    def currentSurface(self):
        return self._currentSurface

    def currentSurfaceIndex(self):
        return self._currentSurfaceIndex

    def flatten(self):
        
        if len(self._surfaces) == 1:
            
            return self._surfaces[0].image()
        
        flattenedImage = utils.createImage(self._animation.frameWidth(), self._animation.frameHeight())

        painter = QPainter()
        painter.begin(flattenedImage)

        for surface in self._surfaces:
            painter.drawImage(0, 0, surface.image())

        painter.end()

        return flattenedImage
    
    def resize(self, width, height):

        for surface in self._surfaces:
            surface.resize(width, height)
    
    def scaleToSize(self, width, height):
        
        for surface in self._surfaces:
            
            oldWidth = surface.width()
            oldHeight = surface.height()
            
            surface.scale(width / oldWidth, height / oldHeight)
    
    def scaleToFactor(self, factor):
        
        for surface in self._surfaces:
            
            surface.scale(factor, factor)
    
    def clone(self):
        
        clone = Frame(self._animation)
        
        for surface in self._surfaces:
            
            clone.addSurface(surface.image().copy())
            
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

    def resize(self, width, height):

        newImage = utils.createImage(width, height)

        painter = QPainter(newImage)

        painter.drawImage(0, 0, self._image)
        
        self._image = newImage
        
    def scale(self, scaleX, scaleY):

        curWidth = self.width()
        curHeight = self.height()

        newWidth = curWidth * scaleX
        newHeight = curHeight * scaleY

        self._image = self._image.scaled(newWidth, newHeight)

    def __getstate__(self):

        if self._bytes is None or self._bytes.isEmpty():
            self._bytes = utils.imageToByteArray(self._image)

        state = self.__dict__.copy()

        del state['_image']
        del state['_id']

        return state

    def __setstate__(self, state):

        self.__dict__.update(state)
        self._image = utils.byteArrayToImage(self._bytes)
        self._bytes.clear()

