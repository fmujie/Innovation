import wave
import pyaudio
from tqdm import tqdm

#define stream chunk
chunk = 1024

# open a wav format music
f = wave.open(r"back.wav", "rb")
# instantiate PyAudio
p = pyaudio.PyAudio()
# open stream
stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True)
# read data
data = f.readframes(chunk)

print(data)
datas = []
# paly stream
while len(data) > 0:
    data = f.readframes(chunk)
    datas.append(data)
for d in tqdm(datas):
    stream.write(d)
# while data != '':
#     stream.write(data)
#     data = f.readframes(chunk)

# stop stream
stream.stop_stream()
stream.close()

# close PyAudio
p.terminate()
