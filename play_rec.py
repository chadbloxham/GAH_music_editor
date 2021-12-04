#!/usr/bin/env python3
"""Create a recording with arbitrary duration.
The soundfile module (https://PySoundFile.readthedocs.io/) has to be installed!
"""
# import tempfile
import queue
import sys
import os
from shutil import copyfile
from pydub import AudioSegment
from pydub.playback import play
import threading
import keyboard

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

# global variable so both threads can access
q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


def play_record(song_name, track_name):
    num_wavs = 0
    for file in os.listdir(song_name):
        if file[-4:] == '.wav':
            num_wavs += 1
    track_name = song_name + '/' + track_name + '.wav'
    # If there is a master track, play it in a thread
    if num_wavs > 0:
        song_master = song_name + '/master.wav'
        play_thread = threading.Thread(target=play_audio, args=[song_master])
        play_thread.start()
    try:
        device_info = sd.query_devices(None, 'input')
        samplerate = int(device_info['default_samplerate'])
        # Make sure the file is opened before recording anything:
        # this code creates two threads. One in which captured audio data is
        # put on the FIFO queue and another where it is grabbed and written to file
        with sf.SoundFile(track_name, mode='x', samplerate=samplerate, channels=1, subtype=None) as out_file:
            with sd.InputStream(samplerate=samplerate, device=None, channels=1, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    out_file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished.')
        keep_track = input('Keep track? (y/n) ')
        if keep_track == 'y':
            if num_wavs > 0:
                add_to_master = input('Add track to master? (y/n) ')
                if add_to_master == 'y':
                    master_wav = AudioSegment.from_wav(song_master)
                    track_wav = AudioSegment.from_wav(track_name)
                    new_master = master_wav.overlay(track_wav, position=0)
                    file_handle = new_master.export(song_name + '/master.wav', format="wav")
            else:
                copyfile(track_name, song_name + '/master.wav')
        else:
            os.remove(track_name)
        exit()
    except Exception as e:
        print(e)
        exit()


def play_audio(filename):
    song = AudioSegment.from_wav(filename)
    play(song)


if __name__ == '__main__':
    song_name = sys.argv[1]
    track_name = sys.argv[2]
    play_record(song_name, track_name)
