from aip import AipSpeech

APP_ID = '17574280'
API_KEY = 'AZnUzamglnNguDrF0COwLX8C'
SECRET_KEY = 'MDUPKK0yu53hqIpej9eaVCDwm9LKvcGc'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def speak(text=""):
    result = client.synthesis(text, 'zh', 1, {
        'per': 4,# 发音人
        'spd': 5,# 语速，取值0-15，默认为5中语速
        'pit': 5,# 音调，取值0-15，默认为5中语调
        'vol': 5,# 音量，取值0-9，默认为5中音量
        'aue': 6,# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    })

    if not isinstance(result, dict):
        with open('back.wav', 'wb') as f:
            f.write(result)
speak("祝你生日快乐")