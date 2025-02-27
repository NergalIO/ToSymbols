# ToSymbols
Converting images, camera view, mp4 videos (with sound) to symbols representation
# Dependencies: numpy, opencv-python, pyaudio, moviepy

# Usage 

## To start program
python main.py --camera/--video [args] [path]

## Help menu
### --camera: Converts the camera image into a symbolic view in video format
### Usage:

python main.py --camera --colorize --new-height=64

#### Arguments:

--new-height: Resizes the original image, if the argument flag, no value, is enabled, the value is set automatically to 128
--colorize: Outputs the image in color (recommended for use in conjunction with --new-height=64), default = False

### --camera: Converts frames from video into character format and outputs to the console along with audio
#### Usage:

python main.py --video --colorize --new-height=64 [path]

#### Arguments:

--new-height: Resizes the original image, if the argument flag, no value, is enabled, the value is set automatically to 128
--colorize: Outputs the image in color (recommended for use in conjunction with --new-height=64), default = False
