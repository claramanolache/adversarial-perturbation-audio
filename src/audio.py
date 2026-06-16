import os
from pydub import AudioSegment
from RealtimeSTT import AudioToTextRecorder

# https://github.com/jiaaro/pydub

file_path = "/Users/claramanolache/adversarial-perturbation-audio/res/mama_youve_been_on_my_mind.mp3"
song = AudioSegment.from_mp3(file_path)


if __name__ == "__main__":
    with AudioToTextRecorder() as recorder:
        print("Speak now")
        print(recorder.text())
