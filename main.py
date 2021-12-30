import argparse
import time
import os
import requests
import re
import xmltodict


def find_link(link_to_vid):
    start = time.time()
    cc_GET = '#ytp-id-16'
    res = requests.get(link_to_vid + cc_GET)

    start_str = 'playerCaptionsTracklistRenderer'
    end_str = '","name"'

    list_to_str = ' '.join(map(str, res))
    sub = list_to_str[list_to_str.find(start_str):list_to_str.find(end_str) + len(end_str)]
    sub = re.sub(r"' b'", '', sub)
    sub = re.sub(r"\\\\u0026", '&', sub)
    sub = re.sub(r'playerCaptionsTracklistRenderer', '', sub)
    sub = re.sub(r'captionTracks', '', sub)
    sub = re.sub(r'baseUrl', '', sub)
    sub = re.sub(r'baseUrl', '', sub)
    sub = sub.removeprefix('":{"":[{"":"')
    sub = re.sub(r'","name"', '', sub)
    print("Finding the link took:", time.time() - start, "sec.")
    return sub


def cc_SRT(url, language, filename, filetype):
    language = f'&tlang={language}'
    new_url = url + language

    try:
        response = requests.get(new_url)
        dict_data = xmltodict.parse(response.content)
    except Exception as e:
        print("Try again!")

    try:
        with open(f"{filename}.{filetype}", "a", encoding="utf-8") as f:
            for x in range(1, (len(dict_data['transcript']['text']) + 1)):
                try:
                    cc = dict_data['transcript']['text'][x - 1]['#text']
                    cc = re.sub(r"&#39;", '', cc)

                    start_ms = dict_data['transcript']['text'][x - 1]['@start']
                    duration_ms = dict_data['transcript']['text'][x - 1]['@dur']

                    start_ms = int(float(start_ms) * 1000)
                    duration_ms = int(float(duration_ms) * 1000)

                    temp = time.strftime('%H:%M:%S.{}'.format(start_ms % 1000), time.gmtime(start_ms / 1000.0))
                    temp1 = time.strftime('%H:%M:%S.{}'.format((duration_ms + start_ms) % 1000),
                                          time.gmtime((duration_ms + start_ms) / 1000.0))

                    p_1 = x
                    p_2 = temp, '-->', temp1
                    p_2 = (' '.join(p_2))
                    p_3 = cc

                    f.writelines(str(p_1))
                    f.writelines('\n')
                    f.writelines(str(p_2))
                    f.writelines('\n')
                    f.writelines(str(p_3))
                    f.writelines('\n''\n')

                except Exception:
                    continue

    except Exception:
        print("Failed to download cc! Try again!")


def cc_CLEAN(url, language, filename, filetype):
    language = f'&tlang={language}'
    new_url = url + language

    try:
        response = requests.get(new_url)
        dict_data = xmltodict.parse(response.content)
    except Exception:
        print("Try again!")

    try:
        with open(f"{filename}.{filetype}", "a", encoding="utf-8") as f:
            for x in range(1, (len(dict_data['transcript']['text']) + 1)):
                try:
                    cc = dict_data['transcript']['text'][x - 1]['#text']
                    cc = re.sub(r"&#39;", '', cc)
                    f.write(cc + '\n')
                except Exception:
                    continue
    except Exception:
        print("Failed to download cc! Try again!")


def main():
    start = time.time()
    try:
        parser = argparse.ArgumentParser(description='Optional app description')

        parser.add_argument('URL', type=str, help='URL of the Youtube video')
        parser.add_argument("--type", default="clean", choices=["clean", "srt"], help="specify the type of subtitle, "
                                                                                      "clean- only text, srt - text "
                                                                                      "with time in HH:MM:SS")

        parser.add_argument("--language", default="en", help="the ISO language code")
        parser.add_argument("--filename", default="subtitle", help="specify the name of subtitle")
        parser.add_argument("--filetype", default="txt", choices=["txt", "srt"],
                            help="specify the output type of subtitle")

        args = parser.parse_args()
        if args.type == 'clean':
            cc_CLEAN(find_link(args.URL), args.language, args.filename, args.filetype)
        if args.type == 'srt':
            cc_SRT(find_link(args.URL), args.language, args.filename, args.filetype)
        print(f"The program has saved the subtitles to the file {args.filename} in:", time.time() - start, "sec.", 'to',
              os.getcwd())
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
