import speech_recognition as sr

'''
调用speech_recognition模块录音方法，从系统麦克风拾取音频数据，
采样率为 16000（百度语音 Api 最高支持到 16k 的采样率）
Then将采集到的音频数据以 wav 格式保存在当前目录下的 recording.wav 文件中，
供后面的程序使用
'''
def recordBySr(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())

recordBySr()
