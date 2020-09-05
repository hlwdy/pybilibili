import requests,re,json,subprocess
from bs4 import BeautifulSoup

def download(referer_url,video_url,audio_url,video_name):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.3239.11',
        'Referer':referer_url,
        'Origin': 'https://www.bilibili.com',
    }
    #伪造headers
    print("开始下载视频：%s"%video_name)
    video_content=requests.get(video_url, headers=headers)
    print('%s视频大小：'%video_name, video_content.headers['content-length'])
    audio_content=requests.get(audio_url, headers=headers)
    print('%s音频大小：'%video_name, audio_content.headers['content-length'])
    #开始下载视频
    received_video=0
    with open('%s_video.mp4' % video_name, 'ab') as output:
        while int(video_content.headers['content-length']) > received_video:
            headers['Range'] = 'bytes=' + str(received_video) + '-'
            response = requests.get(video_url, headers=headers)
            output.write(response.content)
            received_video += len(response.content)
    print('视频下载完成')
    #下载视频结束,开始下载音频
    audio_content=requests.get(audio_url, headers=headers)
    received_audio=0
    with open('%s_audio.mp4' % video_name, 'ab') as output:
        while int(audio_content.headers['content-length']) > received_audio:
            #视频分片下载
            headers['Range'] = 'bytes=' + str(received_audio) + '-'
            response = requests.get(audio_url, headers=headers)
            output.write(response.content)
            received_audio += len(response.content)
      #下载音频结束
    print('音频下载完成')
    return video_name

def get_title(html):
    soup=BeautifulSoup(html,"html.parser")
    return soup.find_all('h1',attrs={"class":"video-title"})[0].span.get_text()

def merge(video_name,out_name):
    ffmpeg_str='ffmpeg -i %s_video.mp4 -i %s_audio.mp4 -c copy %s.mp4'%(video_name,video_name,out_name)
    #print(ffmpeg_str)
    x=subprocess.Popen(ffmpeg_str,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,err=x.communicate()

#url='https://www.bilibili.com/video/BV1XW411M7Gu'
url=input('输入视频完整地址: ')
text=requests.get(url).text
json_text=re.findall(r'<script>window.__playinfo__=(\{.*?\})</script>', text)[0]
playinfo=json.loads(json_text)
video_info_list=[]
quality_len=len(playinfo['data']['accept_description'])
for i in range(quality_len):
    video_info={}
    video_info['quality']=playinfo['data']['accept_description'][i]
    video_info['acc_quality']=playinfo['data']['accept_quality'][i]
    video_info['video_url']=playinfo['data']['dash']['video'][i]['baseUrl']
    video_info['audio_url']=playinfo['data']['dash']['audio'][0]['baseUrl']
    video_info_list.append(video_info)
    #print(video_info)

for i in range(quality_len):
    print(str(i)+video_info_list[i]['quality'])
quality_num=-1
while(quality_num<0 or quality_num>quality_len-1):
    tmp_str=input('请选择清晰度(输入对应数字0-%s): '%str(quality_len-1))
    try:
        quality_num=int(tmp_str)
    except:
        pass
print('选择清晰度| %s |成功'%video_info_list[quality_num]['quality'])
vname=get_title(text)
download(url,video_info_list[quality_num]['video_url'],video_info_list[quality_num]['audio_url'],'tmp')
print('进行合并...')
merge('tmp',vname)
print('下载完成: %s.mp4'%vname)
input('输入回车键以继续...')
