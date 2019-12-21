import json
import time
import wave
import string
import pyaudio
import requests
from tqdm import tqdm
from aip import AipSpeech
import speech_recognition as sr


class SmartChatRobot(object):
    '''
    Baidu Speech API
    '''
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    url = 'http://fjx.com/api/test'

    '''
    调用speech_recognition模块录音方法，从系统麦克风拾取音频数据，
    采样率为 16000（百度语音 Api 最高支持到 16k 的采样率）
    Then将采集到的音频数据以 wav 格式保存在当前目录下的 recording.wav 文件中，
    供后面的程序使用
    '''
    def recordBySr(self, rate=16000):
        r = sr.Recognizer()
        with sr.Microphone(sample_rate=rate) as source:
            print("please say something")
            audio = r.listen(source)

        with open("recording.wav", "wb") as f:
            f.write(audio.get_wav_data())

    '''
    将 SpeechRecognition 录制的音频格式为.wav文件使用Post方法上传上传至百度语音的服务，
    返回识别后的json数据并抽取result的文本进行输出
    '''
    def recogByBaiduApi(self):
        with open('recording.wav', 'rb') as f:
            audio_data = f.read()
            # 参数'dev_pid'普通话(支持简单的英文识别)
        result = self.client.asr(audio_data, 'wav', 16000, {
            'dev_pid': 1536,
        })
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text

    '''
    请求图灵，获取聊天内容
    '''
    def tuLing(self, content):
        # 图灵api
        api = r'http://openapi.tuling123.com/openapi/api/v2'
        # userid = int(time.time())
        # 创建post提交的数据
        data = {
            "perception": {
                "inputText": {
                    "text": content
                }
            },
            "selfInfo": {
                "location": {
                    "city": "淄博",
                    "street": "新村路"
                }
            },
            "userInfo": {
                "apiKey": "c6cff70bb7cd4827a40620c00a82ca36",
                "userId": '522490',
            }
        }
        # 转化为json格式
        jsondata = json.dumps(data)
        # 发起post请求
        response = requests.post(api, data=jsondata)
        # 将返回的json数据解码
        robot_res = json.loads(response.content)
        # 提取对话数据
        print(robot_res["results"][0]['values']['text'])
        robotRes = robot_res["results"][0]['values']['text']
        return robotRes

    '''
    发送请求，获取语音合成.wav
    '''
    def getBaiDuTts(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'per': 4,  # 发音人
            'spd': 5,  # 语速，取值0-15，默认为5中语速
            'pit': 5,  # 音调，取值0-15，默认为5中语调
            'vol': 5,  # 音量，取值0-9，默认为5中音量
            'aue': 6,  # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
        })

        if not isinstance(result, dict):
            with open('back.wav', 'wb') as f:
                f.write(result)

    '''
    播放百度AI合成语音
    '''
    def playAudio(self, path):
        # define stream chunk
        chunk = 1024
        # open a wav format music
        f = wave.open(path, "rb")
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        # read data
        data = f.readframes(chunk)
        # print(data)
        datas = []
        # paly stream
        while len(data) > 0:
            data = f.readframes(chunk)
            datas.append(data)
        for d in tqdm(datas):
            stream.write(d)
        # stop stream (4)
        stream.stop_stream()
        stream.close()
        # close PyAudio (5)
        p.terminate()

    '''
    发送API请求，查询最新温度，PHP实现
    '''
    def QrIndrTemp(self):
        res = requests.get(self.url)
        data = res.json()
        current = data[1]["temperature"]
        return current

    '''
    检测输入语音的关键字
    '''
    def find_string(self, s, t):
        try:
            str.index(s, t)
            return True
        except(ValueError):
            return False

    '''
    条件判断函数，根据关键字判别，决定是否激发其他功能    
    '''
    def cdJudument(self, result_text):
        interruptStr = "谈话结束"
        inquireTem = "查询一下室内温度"
        if interruptStr in result_text:
            res = self.find_string(result_text, interruptStr)
            if res:
                end = "那我就和你说拜拜啦"
                self.getBaiDuTts(end)
                self.playAudio("back.wav")
                exit(0)
            else:
                pass
        elif inquireTem in result_text:
            res1 = self.find_string(result_text, inquireTem)
            if res1:
                current = self.QrIndrTemp()
                currents = "当前最新查询到的室内温度为" + str(current) + "摄氏度"
                self.getBaiDuTts(currents)
                self.playAudio("back.wav")
                time.sleep(1)
            else:
                pass
        else:
            robotRes = self.tuLing(result_text)
            self.getBaiDuTts(robotRes)
            self.playAudio("back.wav")
            time.sleep(1)

    def dialogue(self):
        while True:
            # 输入对话内容
            self.recordBySr()
            result_text = self.recogByBaiduApi()
            self.cdJudument(result_text)


if __name__ == '__main__':
    test = SmartChatRobot()
    test.dialogue()
