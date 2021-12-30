
# Lyrics Youtube Downloader
## Setup

 Download subtitle from youtube without API

    Usage: main.py URL [-h] [--type {clean,srt}] [--language LANGUAGE] [--filename FILENAME] [--filetype {txt,srt}]
    
    
    positional arguments:
      url                   URL of the Youtube video

    optional arguments:
       -h, --help                   show this help message and exit
      --type {clean,srt}            specify the type of subtitle, clean- only text, srt - text with time in HH:MM:SS
      --language LANGUAGE           the ISO language code
      --filename FILENAME           specify the name of subtitle
      --filetype {txt,srt}          specify the output type of subtitle


## Install  requirements

```
pip install -r requirements.txt
```

## Running the script


```
Example:
- python main.py https://www.youtube.com/watch?v=kFpy1OXpLak
- python main.py https://www.youtube.com/watch?v=kFpy1OXpLak --type clean --language pl --filename CC
- python main.py https://www.youtube.com/watch?v=kFpy1OXpLak --type srt --filetype srt
```
