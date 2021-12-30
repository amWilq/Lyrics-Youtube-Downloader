#
cc Youtube Downloader
Lyrics Youtube Downloader
Youtube Subtitle Downloader

Download subtitle from youtube without API

usage: main.py [-h] [--type {clean,srt}] [--language LANGUAGE] [--filename FILENAME] [--filetype {txt,srt}] URL

Optional app description

positional arguments:
  URL                   URL of the Youtube video

optional arguments:
  -h, --help            show this help message and exit
  --type {clean,srt}    specify the type of subtitle, clean- only text, srt - text with time in HH:MM:SS
  --language LANGUAGE   the ISO language code
  --filename FILENAME   specify the name of subtitle
  --filetype {txt,srt}  specify the output type of subtitle
  
  
Example:
1) python main.py https://www.youtube.com/watch?v=kFpy1OXpLak
2) python main.py https://www.youtube.com/watch?v=kFpy1OXpLak --type clean --language pl --filename CC --filetype txt
3) python main.py https://www.youtube.com/watch?v=kFpy1OXpLak --type srt --filetype srt

