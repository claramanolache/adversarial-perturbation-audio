import os
from pydub import AudioSegment

# https://github.com/jiaaro/pydub

file_path = "/Users/claramanolache/adversarial-perturbation-audio/res/mama_youve_been_on_my_mind.mp3"
song = AudioSegment.from_mp3(file_path)
