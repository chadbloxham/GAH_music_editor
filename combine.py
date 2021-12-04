import os
import sys
from pydub import AudioSegment

def combine_tracks(track1, track2, out_track_name):
    track1_wav = AudioSegment.from_wav(track1)
    track2_wav = AudioSegment.from_wav(track2)
    comb_wav = track1_wav.overlay(track2_wav, position=0)
    out_track_file = os.getcwd() + '/' + out_track_name + '.wav'
    file_handle = comb_wav.export(out_track_file, format="wav")

if __name__ == '__main__':
    track1 = sys.argv[1]
    track2 = sys.argv[2]
    out_track = sys.argv[3]
    combine_tracks(track1, track2, out_track)
