#!/usr/bin/env python3

import argparse
import datetime
import os
import subprocess
import urllib.parse

from tqdm import tqdm

FNULL = open(os.devnull, "w")
ERROR_LOG = datetime.datetime.now().isoformat() + "-voxceleb-dl-error.log"


def log_error(msg):
    FERROR = open(ERROR_LOG, "a")
    FERROR.write(msg + "\n")


def download_video(name, video_id, segments_file_path, output_dir):
    global FNULL

    youtube_url = "https://www.youtube.com/watch?v=" + video_id
    audio_stream_url = None
    try:
        audio_stream_url_bytes = subprocess.check_output(["youtube-dl",
                                                          "-f",
                                                          "bestaudio",
                                                          "-g",
                                                          youtube_url])
        audio_stream_url = audio_stream_url_bytes.decode("utf-8").rstrip()
        audio_stream_url = urllib.parse.unquote(audio_stream_url)
    except subprocess.CalledProcessError:
        log_error("Failed to get url for {0}.".format(
            os.path.join(name, video_id)))
        return
    audio_format = audio_stream_url.replace(
        "=", "/").replace("&", "/").split("mime/audio/")[1].split("/")[0]

    output_dir = os.path.join(output_dir, video_id)
    os.mkdir(output_dir)

    with open(segments_file_path, "r") as f:
        # read 5 header lines
        for _ in range(5):
            f.readline()

        segments = []

        while True:
            line = f.readline()
            if not line:
                break

            write_path, start_time, end_time = line.split(" ")[:3]
            write_path = write_path.split('/')[1]
            write_path += "." + audio_format
            write_path = os.path.join(output_dir, write_path)
            start_time = float(start_time)
            end_time = float(end_time)

            segments += [(write_path, start_time, end_time)]

        segment_cnt = 0
        segments_pbar = tqdm(segments, leave=False,
                             desc="Downloading segment [{0}, {1}]".format(
                                 segments[segment_cnt][1],
                                 segments[segment_cnt][2]))
        for segment in segments_pbar:
            write_path, start_time, end_time = segment

            try:
                subprocess.run(["ffmpeg",
                                "-ss",
                                "{:0.2f}".format(start_time),
                                "-i",
                                audio_stream_url,
                                "-t",
                                "{:0.2f}".format(end_time - start_time),
                                "-c:a",
                                "copy",
                                write_path],
                               check=True,
                               stdout=FNULL,
                               stderr=FNULL)
            except subprocess.CalledProcessError:
                log_error("Failed to download {0} segment [{1}, {2}].".format(
                    os.path.join(name, video_id), start_time, end_time))
                return

            segment_cnt = segment_cnt + 1
            if segment_cnt < len(segments):
                segments_pbar.set_description((
                    "Downloading segment [{0}, {1}]".format(
                        segments[segment_cnt][1],
                        segments[segment_cnt][2])))


def download_all(input_dir, output_dir):
    names = os.listdir(input_dir)
    names.sort()

    name_cnt = 0
    names_pbar = tqdm(names, desc="Downloading audio for {0}".format(names[0]))

    for name in names_pbar:
        try:
            os.mkdir(os.path.join(output_dir, name))
            names_pbar.set_postfix(folder_created=False)
            names_pbar.refresh()
        except FileExistsError:
            names_pbar.set_postfix(folder_created=True)
            names_pbar.refresh()
            continue

        videos = os.listdir(os.path.join(input_dir, name))
        videos.sort()

        video_cnt = 0
        videos_pbar = tqdm(
            videos, leave=False,
            desc="Downloading audio from {0}".format(videos[video_cnt][:-4]))

        for video in videos_pbar:
            video_id = video[:-4]
            download_video(name,
                           video_id,
                           os.path.join(input_dir, name, video),
                           os.path.join(output_dir, name))

            video_cnt = video_cnt + 1
            if video_cnt < len(videos):
                videos_pbar.set_description(
                    "Downloading audio from {0}".format(videos[video_cnt][:-4]))

        name_cnt = name_cnt + 1
        if name_cnt < len(names):
            names_pbar.set_description(
                "Downloading audio for {0}".format(names[name_cnt]))


def main():
    parser = argparse.ArgumentParser(description="VoxCeleb Download Tool")
    parser.add_argument("input_dir", metavar="input-dir",
                        help="Path to voxceleb1_test (inclusive)")
    parser.add_argument("output_dir", metavar="output-dir",
                        help="Path to output folder (inclusive)")
    args = parser.parse_args()
    download_all(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
