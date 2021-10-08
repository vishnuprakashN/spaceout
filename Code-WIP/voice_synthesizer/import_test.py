import numpy as np

from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
from playsound import playsound
from scipy.io.wavfile import write

print("libraries imported")

encoder.load_model("encoder/saved_models/pretrained.pt")
synthesizer = Synthesizer("synthesizer/saved_models/pretrained/pretrained.pt")
vocoder.load_model("vocoder/saved_models/pretrained/pretrained.pt")

print("all the models imported \n")

SAMPLE_RATE = 22050
record_or_upload = "samples/1320_00000.mp3" 
record_seconds = 5
embedding = None

print("audio file imported \n")


def _compute_embedding(audio):
  global embedding
  embedding = None
  embedding = encoder.embed_utterance(encoder.preprocess_wav(audio, SAMPLE_RATE))
  print("encoder is sucessfull")

def synthesize(embed, text):
  print("Synthesizing new audio... \n")
  #with io.capture_output() as captured:
  specs = synthesizer.synthesize_spectrograms([text], [embed])
  generated_wav = vocoder.infer_waveform(specs[0])
  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
  print("sysnthesize complete \n")
  print(generated_wav)
  write('voice.wav',synthesizer.sample_rate,generated_wav)
  print("voice generated")



_compute_embedding(record_or_upload)

text = "hey this is vishnu and iam the king of the world"

synthesize(embedding,text)


