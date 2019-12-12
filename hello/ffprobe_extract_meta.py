import json
import os
import subprocess
from datetime import datetime
from os import path
from pathlib import Path

from ffprobe import FFProbe

# To view all tags (stream_tags=creation_time is one tag):
# ffprobe -v quiet -print_format json -show_entries stream_tags:format_tags 162443131116bcc8f8f3522133.mp4
# cmd = "C:/work/ffmpeg-20191201/bin/ffprobe.exe -v quiet -print_format json -show_entries stream_tags=creation_time C:/wutalk/test2/162443131116bcc8f8f3522133.mp4 "
cmd_prefix = "C:/work/ffmpeg-20191201/bin/ffprobe.exe -v quiet -print_format json -show_entries stream_tags=creation_time "


def get_video_created_time(full_path):
    probe = FFProbe(full_path)
    createdAt = probe.metadata.get('creation_time')
    newName = datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('VID_%Y%m%d_%H%M%S')
    return newName


def get_creation_time(full_filename):
    extract_cmd = cmd_prefix + full_filename

    returned_output = subprocess.check_output(extract_cmd)
    out_json = json.loads(returned_output)
    creation_time_ = out_json["streams"][0]["tags"]["creation_time"]

    createdAt = datetime.strptime(creation_time_, '%Y-%m-%dT%H:%M:%S.%fZ')
    newName = createdAt.strftime('VID_%Y%m%d_%H%M%S')

    simple_name = str(full_filename).split('/')[3]
    if not simple_name.startswith(newName):
        print()
        print(simple_name, "->", creation_time_)
    return newName


def rename(fullName):
    print('start process', fullName)
    # newName = get_video_created_time(vidPathStr)
    newName = get_creation_time(fullName)
    print('new name: {}'.format(newName))
    vidPath = Path(fullName)
    newFullName = str(vidPath.parent) + os.sep + newName + ".mp4"
    print(newFullName)
    count = 0
    while path.exists(newFullName):
        print("exist")
        newFullName = str(vidPath.parent) + os.sep + newName + '_' + str(count) + ".mp4"
        count += 1
        print(count, newFullName)

    os.rename(fullName, newFullName)
    print("renamed: {}->{}".format(fullName, newFullName))


def list_files(video_dir):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(video_dir):
        for file in f:
            if '.mp4' in file and 'VID' not in file:
                # if '.mp4' in file:
                files.append(os.path.join(r, file))
    return files


if __name__ == '__main__':
    video_dir = 'C:/wutalk/test/'
    video_files = list_files(video_dir)
    print('there are {} video files under {}'.format(len(video_files), video_dir))
    for f in video_files:
        # get_creation_time(f)
        # print(f)
        rename(f)
    # print_creation_time('C:/wutalk/test/VID_20170322_093721.mp4')
    print("process completed")
