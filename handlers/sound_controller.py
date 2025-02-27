import pathlib
import pyaudio
import moviepy
import wave


class VideoToSoundConverter:
    @staticmethod
    def mp4_to_wav(path: str) -> str:
        if pathlib.Path(path.replace("mp4", "wav")).exists():
            return path.replace("mp4", "wav")
        video_file = moviepy.VideoFileClip(path)
        audio_file = video_file.audio
        if audio_file is None:
            return None
        audio_file.write_audiofile(path.replace("mp4", "wav"))
        return path.replace("mp4", "wav")


class SoundWav:
    def __init__(self, sound, fps):
        if sound is None:
            self.has_audio = False
        else:
            self.has_audio = True
            self.pyaudio = pyaudio.PyAudio()
            
            self.fps = fps
            self.sound = wave.open(sound)
            self.stream = self.pyaudio.open(
                format=pyaudio.get_format_from_width(self.sound.getsampwidth()),
                channels=self.sound.getnchannels(),
                rate=self.sound.getframerate(),
                output=True,
            ) 
    
    def stop(self) -> None:
        self.stream.close()
        self.pyaudio.terminate()
    
    def play_frame(self) -> None:
        if self.has_audio:
            data = self.sound.readframes(int(self.sound.getframerate()/self.fps))
            self.stream.write(data)