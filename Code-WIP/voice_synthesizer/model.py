import numpy as np

from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
from playsound import playsound
from scipy.io.wavfile import write
from pydub import AudioSegment
import pydub

print("libraries imported")

encoder.load_model("trained_models/encoder/saved_models/pretrained.pt")
synthesizer = Synthesizer("trained_models/synthesizer/saved_models/pretrained/pretrained.pt")
vocoder.load_model("trained_models/vocoder/saved_models/pretrained/pretrained.pt")

print("all the models imported \n")
voice_one = "samples/1320_00000.mp3" 
voice_two = "samples/3575_00000.mp3"
voice_three = "samples/p240_00000.mp3"


SAMPLE_RATE = 22050
record_seconds = 5

print("audio file imported \n")

global voice_embedding_one  
global voice_embedding_two  
global voice_embedding_three  


voice_embedding_one = encoder.embed_utterance(encoder.preprocess_wav(voice_one, SAMPLE_RATE))
voice_embedding_two = encoder.embed_utterance(encoder.preprocess_wav(voice_two, SAMPLE_RATE))
voice_embedding_three = encoder.embed_utterance(encoder.preprocess_wav(voice_three, SAMPLE_RATE))
print("encoder is sucessfull")




def write_it(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")


def synthesize(embed, text):
  print("Synthesizing new audio... \n")
  #with io.capture_output() as captured:
  specs = synthesizer.synthesize_spectrograms([text], [embed])
  print("systhesized")
  generated_wav = vocoder.infer_waveform(specs[0])
  print("vocoded")
  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
  print("sysnthesize complete \n")
  print(generated_wav)
  scaled = np.int16(generated_wav/np.max(np.abs(generated_wav)) * 32767)
  write('trial1.wav',synthesizer.sample_rate,scaled)
  AudioSegment.from_wav("trial1.wav").export("static/please.mp3", format="mp3")
  print("voice generated")


def output(text,voice):
    
    if voice == "Tina":
       embedding = voice_embedding_one 
    elif voice == "Rob":
       embedding = voice_embedding_two
    elif voice == "Vishnu":
       embedding = voice_embedding_three

    synthesize(embedding,text)


