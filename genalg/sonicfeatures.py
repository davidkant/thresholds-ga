import librosa
import numpy as np

def silence_ratio(filename, thresh=20):
    """Ratio of quiet frames to not quiet frames."""
    # read audiofile
    y, sr = librosa.load(filename, mono=True, sr=44100)
    # loudness
    S, phase = librosa.magphase(librosa.stft(y))
    log_S = librosa.logamplitude(np.sum(S, axis=0), ref_power=1.0)
    # ratio
    ratio =  float(np.sum(log_S < thresh)) / log_S.shape[0]
    # return
    return ratio

def test_silence_ratio():
    f1 = "../resources/audio/sample1.wav"
    print silence_ratio(f1)

if __name__ == "__main__":
    test_silence_ratio()
