## Introduction ##
This is a module that works with [audiogrep](https://github.com/antiboredom/audiogrep) to create timestamped transcripts of audio files. It is very experimental and in the early stages of development.

## Installation ##

This script also assumes you're getting a transcript from [audiogrep](https://github.com/antiboredom/audiogrep), so first you need to install that. 

Audiogrep requires [pip](https://pip.pypa.io/en/stable/installing/), [ffmpeg](http://ffmpeg.org/), and [pocketsphinx](http://cmusphinx.sourceforge.net/). DISCLAIMER: the audiogrep [installation instructions](https://github.com/antiboredom/audiogrep/blob/master/README.md) in general assume you're using a mac. 

Finally, this script uses [Python 3](https://www.python.org/downloads/). If you have 2.x installed on your machine, you can also install Python3; there are lots of instructions on the internet about how to do this, mostly using virtual environments. Because instructions vary depending on what OS you're using, use your judgement about which ones to use. 
To use this script (assuming 2.x is your primary version of Python), use the command ```python3``` rather than ```python```.

## Creating Transcripts ##

Once you have audiogrep and its dependencies installed, you'll follow several steps to create plain text of the transcript, as well as some structured XML that the Islandora Oral Histories module can use. 
* Assuming you don't have transcript files yet, use audiogrep to create the initial transcript files (per the audiogrep readme):

```
audiogrep --input path/to/*.mp3 --transcribe
```
This will transcribe all the audio files in a given directory. Budget some time for this; each transcript will take less than the total time of the audio recording, but could take up to half as long. In general, if you have a lot of audio files, expect that this step will be lengthy.
* To transcribe one file at a time, use ```cd``` to get to the folder containing the audio files, and then:

```
audiogrep --input filename.mp3 --transcribe
```
where "filename" is the name of the file you want to transcribe.
* Download make_transcripts and then copy the folder with you mp3s into ```make_transcripts/transcription```
* Navigate to ```transcription``` using the command line and then type ``python3 transcript_parsing.py```

You should get derivative folders for each audio recording, containing:
* a copy of the mp3 audio file
* a copy of the transcription.txt file generated by audiogrep
* a derivative .txt file with timestamp information (no chunks of text)
* a derivative .txt file with just text
* a derivative .xml file with timestamp information
* a structured XML document (filename_transcript.xml) for use with the Islandora Oral Histories module

## Use with Islandora ##
The XML transcript output is intended to fit the [Islandora Oral Histories Module](https://github.com/digitalutsc/islandora_solution_pack_oralhistories).
The Oral Histories Module has the following dependencies (per their github page): 
* [Islandora](https://github.com/islandora/islandora)
* [Tuque](https://github.com/islandora/tuque) 
* [Islandora Solr Search](https://github.com/Islandora/islandora_solr_search)
* [Islandora Video Solution Pack](https://github.com/Islandora/islandora_solution_pack_video)
* [Islandora Audio Solution Pack](https://github.com/Islandora/islandora_solution_pack_audio)
* [Transcripts UI](https://github.com/Islandora/islandora_solution_pack_audio)
