# -*- coding: utf-8 -*-


import os
import uuid
from ffmpy import FFmpeg

import numpy as np
import random
import librosa.display
import soundfile
from new_label import get_new_label,get_speed_new_label


# 通过倍率提升
def raise_by_ratio(audio_path: str, output_dir: str, ratio):
    ext = os.path.basename(audio_path).strip().split('.')[-1]
    if ext not in ['wav', 'mp3']:
        raise Exception('format error')
    ff = FFmpeg(
        inputs={
            '{}'.format(audio_path): None}, outputs={
            output_dir: '-filter:a "volume={}"'.format(ratio)})
    print(ff.cmd)
    ff.run()
    return os.path.join(output_dir, '{}.{}'.format(uuid.uuid4(), ext))


# 通过分贝数提升
def raise_by_decibel(audio_path: str, output_dir: str, decibel):
    ext = os.path.basename(audio_path).strip().split('.')[-1]
    if ext not in ['wav', 'mp3']:
        raise Exception('format error')
    ff = FFmpeg(
        inputs={
            '{}'.format(audio_path): None}, outputs={
            output_dir: '-filter:a "volume={}dB"'.format(decibel)})
    print(ff.cmd)
    ff.run()
    return os.path.join(output_dir, '{}.{}'.format(uuid.uuid4(), ext))

def speed_aug(audio_path: str, output_dir: str, speed):
    ext = os.path.basename(audio_path).strip().split('.')[-1]
    if ext not in ['wav', 'mp3']:
        raise Exception('format error')
    ff = FFmpeg(
        inputs={
            '{}'.format(audio_path): None}, outputs={
            output_dir: '-filter:a "atempo={}"'.format(speed)})
    print(ff.cmd)
    ff.run()
    return os.path.join(output_dir, '{}.{}'.format(uuid.uuid4(), ext))

def pitch_aug(audio_path: str, output_dir: str, pit):
    ext = os.path.basename(audio_path).strip().split('.')[-1]
    if ext not in ['wav', 'mp3']:
        raise Exception('format error')
    ff = FFmpeg(
        inputs={
            '{}'.format(audio_path): None}, outputs={
            output_dir: '-filter:a "asetrate=8000*{},aresample=8000,atempo=1/{}"'.format(pit,pit)})
    print(ff.cmd)
    ff.run()
    return os.path.join(output_dir, '{}.{}'.format(uuid.uuid4(), ext))

def time_mask_aug(path,new_path,num):
    audio, sr = librosa.load(path)
    for i in range(num):
        t = np.random.uniform(low=0.0, high=300)
        t = int(t)
        time_len = len(audio)
        t0 = random.randint(0, time_len - t)
        audio[t0:t0 + t] = 0
    soundfile.write(new_path, audio, samplerate=sr)


def nature_noise_aug(path,new_path, max_db=0.5):
    """
    叠加自然噪声
    :param samples: 语音采样
    :param noise_list:噪声文件列表
    :param max_db:最大噪声增益
    :return:
    """
    samples,sr = librosa.load(path)  # frombuffer()导致数据不可更改因此使用拷贝
    data_type = samples[0].dtype
    noise_path = '../noise/noise.wav'
    # 随机音量
    db = np.random.uniform(low=0.1, high=max_db)
    aug_noise, fs = librosa.load(noise_path)
    # 噪声片段增长
    while len(aug_noise) <= len(samples):
        aug_noise = np.concatenate((aug_noise, aug_noise), axis=0)
    # 随机位置开始截取与语音数据等长的噪声数据
    diff_len = len(aug_noise) - len(samples)
    start = np.random.randint(0, diff_len)
    end = start + len(samples)
    # 叠加
    samples = samples + db * aug_noise[start:end]
    samples = samples.astype(data_type)
    soundfile.write(new_path, samples, samplerate=sr)

def white_noise_numpy(path,new_path, min_db=0.1, max_db=0.3):
    """
    高斯白噪声
    噪声音量db
        db = 10, 听不见
        db = 100,可以听见，很小
        db = 500,大
        人声都很清晰
    :param samples:
    :param max_db:
    :param min_db:
    :return:
    """
    samples,sr = librosa.load(path)  # frombuffer()导致数据不可更改因此使用拷贝
    data_type = samples[0].dtype
    #db = np.random.randint(low=min_db, high=max_db)
    noise = 0.1 * np.random.normal(0, 1, len(samples))  # 高斯分布
    samples = samples + noise
    samples = samples.astype(data_type)
    soundfile.write(new_path, samples, samplerate=sr)


def audio_augment(path,aug_path,method,pram):
    folders = os.listdir(path)
    for file in folders:
        if file.endswith('wav'):
            file_path = path+'\\\\'+file
            new_path = aug_path+'\\\\'+file[0:-4]+'_'+method+'.wav'
            label_path = file_path[0:-3] + 'TextGrid'
            new_label_path = new_path[0:-3] + 'TextGrid'
            if method == 'volume':
                raise_by_decibel(file_path,new_path,pram)
            elif method == 'pitch':
                pitch_aug(file_path,new_path,pram)
            elif method == 'speed':
                speed_aug(file_path,new_path,pram)
            elif method == 'time_mask':
                time_mask_aug(file_path,new_path,pram)
            elif method == 'nature_noise':
                nature_noise_aug(file_path,new_path)
            elif method == 'white_noise':
                white_noise_numpy(file_path,new_path)

            if method != 'speed':
                get_new_label(label_path,new_label_path)
            else:
                get_speed_new_label(label_path,new_label_path,pram)




if __name__ == '__main__':


    file_path = r'D:\\研究生\\研二上\\语音识别\\speech_data_augment-main\\audio'
    new_path = r'D:\\研究生\\研二上\\语音识别\\speech_data_augment-main\\audio_aug'
    audio_augment(file_path,new_path,'pitch',0.9)
