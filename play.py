
import sys
from pydub import AudioSegment
from pydub.playback import play

def play_audio(filename):
    track = AudioSegment.from_wav(filename)
    play(track)

if __name__ == '__main__':
    track_name = sys.argv[1]
    play_audio(track_name)
