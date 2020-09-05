import subprocess

x=subprocess.Popen('ffmpeg -i test_video.mp4 -i test_audio.mp4 -c copy out.mp4', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
output,err=x.communicate()
