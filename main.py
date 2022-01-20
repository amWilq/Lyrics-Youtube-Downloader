import argparse
import time
import os
import requests
import re
import xmltodict



class lyrcis():

    def __init__(self, link_to_vid="www.youtube.com", type="clean", language='en', filename='subtitle', filetype='txt'):
        self.link_to_vid = link_to_vid
        self.type = type
        self.language = language
        self.filename = filename
        self.filetype = filetype

    def fink_link(self):

        cc_GET = '#ytp-id-16'
        start_str = 'playerCaptionsTracklistRenderer'
        end_str = '","name"'

        try:
            res = requests.get(self.link_to_vid + cc_GET)
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

            if sub:
                return sub
            else:
                print('retrying...')
                return self.fink_link()

        except Exception:
            return Exception

    def CLEAN(self):
        language = f'&tlang={self.language}'
        new_url = self.fink_link() + language

        try:
            response = requests.get(new_url)
            dict_data = xmltodict.parse(response.content)

        except xmltodict.expat.ExpatError as err:
            print("Problem with parse --->", err)

        try:
            with open(f"{self.filename}.{self.filetype}", "w", encoding="utf-8") as f:
                for x in range(1, (len(dict_data['transcript']['text']) + 1)):
                    try:
                        cc = dict_data['transcript']['text'][x - 1]['#text']
                        cc = re.sub(r"&#39;", '', cc)
                        f.write(cc + '\n')
                    except IOError:
                        continue
        except IOError:
            print("Failed to download cc! Try again!")

    def SRT(self):

        language = f'&tlang={self.language}'
        new_url = self.fink_link() + language

        try:
            response = requests.get(new_url)
            dict_data = xmltodict.parse(response.content)
        except xmltodict.expat.ExpatError as err:
            print("Problem with parse --->", err)

        try:
            with open(f"{self.filename}.{self.filetype}", "w", encoding="utf-8") as f:
                tmp = []
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

                        p_2 = temp, '-->', temp1
                        p_2 = (' '.join(p_2))

                        f.writelines(str(x))
                        f.writelines('\n')
                        f.writelines(str(p_2))
                        f.writelines('\n')
                        f.writelines(cc)
                        f.writelines('\n''\n')

                    except IOError:
                        print(Exception)

        except IOError:
            print("Failed to download cc! Try again!")


def main():
    start = time.time()
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
    os.system("cls")
    if args.type == 'clean':
        url = lyrcis(link_to_vid=args.URL, type=args.type, language=args.language, filename=args.filename,
                     filetype=args.filetype)
        if url.CLEAN():
            print(f"The program has saved the subtitles to the file '{args.filename}.{args.filetype}' in:",
                  '{0:.2g}'.format(time.time() - start), "sec.", 'to', os.getcwd())

    if args.type == 'srt':
        url = lyrcis(link_to_vid=args.URL, type=args.type, language=args.language, filename=args.filename,
                     filetype=args.filetype)
        if url.SRT():
            print(f"The program has saved the subtitles to the file '{args.filename}.{args.filetype}' in:",
                  '{0:.2g}'.format(time.time() - start), "sec.", 'to', os.getcwd())


if __name__ == "__main__":
    main()
