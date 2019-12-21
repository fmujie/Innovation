from aip import AipSpeech
import string

APP_ID = '17574280'
API_KEY = 'AZnUzamglnNguDrF0COwLX8C'
SECRET_KEY = 'MDUPKK0yu53hqIpej9eaVCDwm9LKvcGc'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

'''
将 SpeechRecognition 录制的音频格式为.wav文件使用Post方法上传上传至百度语音的服务，
返回识别后的json数据并抽取result的文本进行输出
'''
def recogByBaiduApi():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()
    # 参数'dev_pid'普通话(支持简单的英文识别)
    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })
    result_text = result["result"][0]
    print("you said: " + result_text)
    return result_text



# def CdJudgment(res):
#     s = "你"
#     if str.find(s, res)!=-1:
#         print("有这个元素")
#     else:
#         print("没有这个元素")
#
# res = recogByBaiduApi()
# # CdJudgment(res)
# s = "wo"
# print(str.find(s, res))

def find_string(s,t):
    try:
        str.index(s,t)
        return True
    except(ValueError):
        return False

s='我们结束会话吧'
t='结束'
# result = s.find(t)
# print(result)
result = find_string(s,t)
print(result)
if result:
    exit(0)
    print("结束会话")
