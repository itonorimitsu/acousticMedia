#coding: utf-8
import wave
import struct
import numpy as np
import pyaudio
from pylab import *

"""正弦波の作成"""
def createSinWave(A, f0, fs, length): 
    """振幅, 基本周波数, サンプリング周波数, 時間"""
    time = np.arange(0, fs * length)
    sin_wave = A * np.sin(2 * np.pi * f0 * time / fs)
    sin_wave = [int(x * 32767.0) for x in sin_wave]

    sin_bin = struct.pack("h" * len(sin_wave), *sin_wave)

    # plot(data[0:100]); show()
    return sin_bin

"""三角波の作成"""
def createTriangleWave(A, f0, fs, length, n):
    data = []
    
    time = np.arange(0, fs * length)
    
    for i in arange(length * fs):
        s = 0.0
        for k in range(1, n):
            s += (-1)**k * (A / (2 * k + 1)**2) * np.sin((2 * k + 1) * 2 * np.pi * f0 * i / fs)
        data.append(s)

    triangle_wave = [int(x * 32767.0) for x in data]
    triangle_bin = struct.pack("h" * len(triangle_wave), *triangle_wave)

    return triangle_bin


"""矩形波の作成"""
def createRectangularWave(A, f0, fs, length, n):
    data = []

    for i in arange(length * fs):
        s = 0.0
        for k in arange(1, n):
            s += (A / (2*k-1)) * np.sin((2*k-1) * 2 * np.pi * f0 * i / fs)
        
        data.append(s)

    rectangular_wave = [int(x * 32767.0) for x in data]
    rectangular_bin = struct.pack("h" * len(rectangular_wave), *rectangular_wave)
    return rectangular_bin

# ここまで

"""ノコギリ波の生成"""
def createSawtoothWave(A, f0, fs, length, n):
    data = []
    for i in arange(length * fs):
        s = 0.0
        for k in range(1, n):
            s += (A / k) * np.sin(2 * np.pi * k * f0 * i / fs)

        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    data = [int(x * 32767.0) for x in data]
    data = struct.pack("h" * len(data), *data)
    return data



def play (data, fs, bit):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels = 1, rate = int(fs), output = True)
    chunk = 1024
    sp = 0
    buffer = data[sp: sp + chunk]
    while True:
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp: sp + chunk]
        if buffer == b'':
            break
    stream.close()
    p.terminate()


def save(filename, data):
    w = wave.Wave_write(filename)
    p = (1, 2, 8000, len(data), 'NONE', 'not compressed')
    w.setparams(p)
    w.writeframes(data)
    w.close()



if __name__ == "__main__" :
    A = 1.0
    A_half = 0.5
    fs = 44100
    length = 1.0
    print('作成する音響波形の基本周波数を指定してください\nf0: ', end="")
    f0 = int(input())
    print('三角波, 矩形波, のこぎり波の高調波の数を指定してください\nn: ', end="")
    n = int(input())
    # 各波形のデータ作成
    data_sin = createSinWave(A, f0, fs, length)
    data_triangle = createTriangleWave(A_half, f0, fs, length, n)
    # data_rectangular = createRectangularWave(A_half, f0, fs, length, n)
    # data_sawtooth = createSawtoothWave(A_half, f0, fs, length, n)
    # waveファイルに出力
    # save("output_sin.wav", data_sin)
    # save("triangle.wav", data_triangle)
    # save("rectangular.wav", data_rectangular)
    # save("sawtooth.wav", data_sawtooth)
    # 音声出力を行う
    play(data_sin, fs, 16)
    play(data_triangle, fs, 16)
    # play(data_rectangular, 8000, 16)
    # play(data_sawtooth, 8000, 16)

