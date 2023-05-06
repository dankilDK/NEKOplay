from zipfile import ZipFile

with ZipFile('ffmpeg/ffmpeg.zip', 'r') as arch:
    arch.extractall('ffmpeg')
    print('unzipped ffmpeg.zip')

with ZipFile('ffmpeg/ffplay.zip', 'r') as arch:
    arch.extractall('ffmpeg')
    print('unzipped ffplay.zip')

with ZipFile('ffmpeg/ffprobe.zip', 'r') as arch:
    arch.extractall('ffmpeg')
    print('unzipped ffprobe.zip')
