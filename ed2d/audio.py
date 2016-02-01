
import ctypes as ct
import struct
import wave

from ed2d.openal import al
from ed2d.openal import alc
from ed2d import typeutils

class AudioContext(object):
    def __init__(self):
        self.device = None
        self.context = None

    def create(self):
        self.device = alc.alcOpenDevice(None)
        if not self.device:
            self.destroy()
            print("Error OpenAL init error.") # TODO - Make this an exception.
            return

        self.context = alc.alcCreateContext(self.device, None)
        alc.alcMakeContextCurrent(self.context)
        if not self.context:
            self.destroy()
            print("Error OpenAL init error.") # TODO - Make this an exception.
            return

    def destroy(self):
        alc.alcMakeContextCurrent(None)
        if self.context:
            alc.alcDestroyContext(self.context)
        if self.device:
            alc.alcCloseDevice(self.device)

channelMap = {1:al.AL_FORMAT_MONO16, 2:al.AL_FORMAT_STEREO16}

class AudioFile(object):
    def __init__(self, filePath):
        wav = wave.open(filePath, mode='rb')
        audioFormat = channelMap[wav.getnchannels()]
        self.audioBitdepth = wav.getsampwidth() * 8
        self.samplerate = wav.getframerate()

        self.source = al.ALuint()
        al.alGenSources(1, ct.byref(self.source))

        al.alSourcef(self.source, al.AL_PITCH, 1.0)
        al.alSourcef(self.source, al.AL_GAIN, 1.0)
        al.alSource3f(self.source, al.AL_POSITION, 0.0, 0.0, 0.0)
        al.alSource3f(self.source, al.AL_VELOCITY, 0.0, 0.0, 0.0)
        al.alSourcei(self.source, al.AL_LOOPING, al.AL_FALSE)

        self.buffer = al.ALuint()
        al.alGenBuffers(1, ct.byref(self.buffer))
        al.alSourcei(self.source, al.AL_BUFFER, al.ALint(self.buffer.value))

        pyBuffer = wav.readframes(wav.getnframes())
        print(len(pyBuffer), wav.getnframes())

        cBuffer = ct.create_string_buffer(pyBuffer)
        bufferData = ct.cast(ct.pointer(cBuffer), ct.c_void_p)
        al.alBufferData(self.buffer, audioFormat, bufferData, self.audioBitdepth // 8, self.samplerate)
        wav.close()

    def destroy(self):
        al.alDeleteSources(1, ct.byref(self.source))
        al.alDeleteBuffers(1, ct.byref(self.buffer))

    def play(self):
        al.alSourcePlay(self.source)

    def stop(self):
        al.alSourceStop(self.source)

    def pause(self):
        al.alSourcePause(self.source)

    def get_pos(self):
        byteoffset = al.ALint()
        al.alGetSourcei(self.source, al.AL_BYTE_OFFSET, ct.byref(byteoffset))
        byteoffset = byteoffset.value
        return float(byteoffset) / self.samplerate

    def volume(self, vol):
        pass


class Audio(object):
    def __init__(self):
        self.context = AudioContext()
        self.context.create()

        # setup listener
        al.alListener3f(al.AL_POSITION, 0.0, 0.0, 0.0)
        al.alListener3f(al.AL_VELOCITY, 0.0, 0.0, 0.0)
        al.alListener3f(al.AL_ORIENTATION, 0.0, 0.0, 0.0)

    def destroy(self):
        self.context.destroy()
