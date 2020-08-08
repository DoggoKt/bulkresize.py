from sys import platform
from os import system, listdir
from os.path import isfile

class BoolValueError(Exception):
  """Raised when input is not 'Y' or 'N'"""
  pass
class TooLargeError(Exception):
  """Raised when the size specified is out of bounds"""
  pass
class NoImagesError(Exception):
  """Raised when there are no images in the directory"""
  pass

def Error(message):
  print("")
  print("\033[31m"+message+"\033[0m")
def BoolInput(message):
  response = input(message)
  if response.lower() != "yes" and response.lower() != "no":
    raise BoolValueError
    return
  boolean = response.lower() == "yes"
  return boolean
def clear():
  print(chr(27)+'[2j')
  print('\033c')
  print('\x1bc')

try:
  if platform.lower() == "win32":
    system('color')
  clear()

  from PIL import Image
  ResizeTo = (int(input("What width should I scale the images to (in px): ")),int(input("What height should I scale the images to (in px): ")))
  PreserveRatio = BoolInput("Preserve aspect ratio during resize? (Yes/No) ")
  clear()
  print("Resizing...")

  imageCount = 0
  for file in list(filter(lambda f: isfile(f), listdir())):
  
    try:
      image = Image.open(file)
    except IOError:
      continue
    
    if PreserveRatio:
      image.thumbnail(ResizeTo, Image.NEAREST)
    else:
      image = image.resize(ResizeTo)
    
    filenameArray = file.split(".")
    image.save("{0}-{1}x{2}.{3}".format(".".join(filenameArray[0:len(filenameArray)-1]), image.width, image.height, filenameArray[len(filenameArray)-1]))
    imageCount+=1
  if imageCount == 0: raise NoImagesError
  print("Resized {0} images successfully!".format(imageCount))


except IOError:
  Error("Something went wrong when trying to load an image. Double-check for any non-image files in the current directory and try again.")
except ValueError:
  Error("The supplied value needs to be a number - don't include the 'px'!")
except BoolValueError:
  Error("The supplied value may be 'yes' or 'no' only.")
except NoImagesError:
  Error("There are no applicable images in this directory! Check where you're running this from and try again.")
except ModuleNotFoundError:
  Error("Pillow isn't installed! Make sure you installed it as per instructions in [bit.ly/bulkresize-setup]")
except:
  Error("An unexpected error occured.")
else:
  print("All files were saved by their original name with the new size suffixed.")
finally:
  input("\033[1;30mPress [ENTER] to exit\033[0m")
