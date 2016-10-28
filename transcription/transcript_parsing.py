# transcription/transcript_pasing.py

import os
import shutil
from lxml import etree as etree
import re

output_file_trns = 'only_transcript.txt'
output_file_time = 'only_timestamp.txt'
# this is the folder you're keeping your source audio files in
folder = 'mp3s'

# This is the whole file path to the mp3 folder
# path = '/Volumes/LIBSTU/AlumniOralHistories/TEST'
# path = '/Users/loaner/transcriptinator/transcription/'
path ='.'

def create_cues(root, speaker, beginning, ending, transcript_text):
    cue = etree.SubElement(root, 'cue')
    spkr = etree.SubElement(cue, 'speaker')
    start = etree.SubElement(cue, 'start')
    end = etree.SubElement(cue, 'end')
    transcript = etree.SubElement(cue, 'transcript')

    spkr.text = str(speaker)
    start.text = str(beginning)
    end.text = str(ending)
    # t = remove_numbers(transcript_text)  # Removes occurences of word(x)
    clean = transcript_text.replace("\xe2", "'")  # Replaces character \xe2 with normal apostrophe
    cleaner = clean.replace("(2)", "")  # Removes (2) 's
    cleanest = cleaner.replace("(3)", "")  # Removes (3) 's
    xmltext = re.sub(u"[^\x20-\x7f]+", u"", cleanest)  # Remove non-printable characters outside of given range
    transcript.text = xmltext


def create_root(in_file):
    root = etree.Element('cues')
    disclaimer = etree.SubElement(root, 'disclaimer')
    disclaimer.text = ('These transcripts were created by a software program; '
                       'we make no guarantees as to the quality of the '
                       'output. We know some of the words are incorrect.')
    return root


def file_names(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith('.transcription_only_timestamp.txt'):
                input_file = os.path.join(dirpath, f)
                iterator(input_file)


# The iterator...where the rubber meets the road!
def iterator(in_file):
    root = etree.Element('cues')
    count = 0
    start_time = 0
    end_time = 0
    speaker = "something"

    # file_name = os.path.basename(in_file)

    beginsplit = os.path.splitext(in_file)[0]
    basefile = beginsplit.split('.')[0]
    out_file = basefile + '_transcript.xml'

    with open(in_file) as transcriptfile:

        for line in transcriptfile:

            # If we find a new <speaker> tab when count > 0 then we need to output the block.
            if '<speaker>' in line:
                if count > 0:
                    end_time = split_vals[2]
                    create_cues(root, speaker, start_time, end_time, " ".join(transcript_words))
                split_vals = line.split(">")
                spk = split_vals[1]
                speaker = spk.replace("\n", "")
                count = 0  # reset the count

            # If the line begins with an alpha character or a digit...process it.
            elif (line[0].isalpha() or line[0].isdigit()):

                # split_vals = line.split()
                # Call our own function to parse the line.  If not as expected...continue to next line
                split_vals = t_split(line)
                if not split_vals:
                    continue

                # Found a first word.  Reset the words array, add to it, and capture the start time.
                if count == 0:
                    # Start a new list of words
                    transcript_words = []
                    # Grab the start time of the first word
                    start_time = split_vals[1]
                    # Save the first word to the list
                    transcript_words.append(split_vals[0])
                    count += 1

                # Found the 120th word...output a cue.
                elif count == 120:
                    # Grab the stop time of the last word
                    end_time = split_vals[2]
                    # Save the last word to the list
                    transcript_words.append(split_vals[0])
                    # Assemble the cue
                    create_cues(root, speaker, start_time, end_time, " ".join(transcript_words))
                    count = 0  # reset the count

                # Otherwise, seave the intervening words to the list
                else:
                    # Save the intervening words to the list
                    transcript_words.append(split_vals[0])
                    count += 1

    # EOF is reached, create a cue for the remaining part of transcription, even if it isn't 120 words long.
    end_time = split_vals[2]
    # Save the last word to the list
    transcript_words.append(split_vals[0])
    # Assemble the cue
    create_cues(root, speaker, start_time, end_time, " ".join(transcript_words))

    tree = etree.ElementTree(root)
    tree.write(out_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')


def make_folders(path):
    for files in os.listdir(path):
        if not files.startswith('.'):
            start_splitting = os.path.splitext(files)[0]
            new_folder = start_splitting.split('.')[0]
            file_loc = os.path.join(path, files)
            derivs_folder = path + new_folder
            if os.path.isdir(derivs_folder):
                pass
            else:
                os.makedirs(derivs_folder)

            if files.endswith('.mp3'):
                shutil.copy2(file_loc, derivs_folder)
            elif files.endswith('.txt'):
                shutil.copy(file_loc, derivs_folder)
            else:
                pass

            for files in os.listdir(derivs_folder):
                input_file = os.path.join(derivs_folder, files)
                if 'transcription.txt' in files:
                    filestart = os.path.splitext(files)[0]

                    transcript_output = os.path.join(
                        derivs_folder, filestart + '_only_transcript.txt')
                    timestamp_output = os.path.join(
                        derivs_folder, filestart + '_only_timestamp.txt')
                    timestamp_xml_out = os.path.join(
                        derivs_folder, filestart + '_only_timestamp.xml')

                    text_lines = scrape_text(input_file)
                    time_lines = scrape_timestamps(input_file)

                    store_text(text_lines, transcript_output)
                    store_timestamps(time_lines, timestamp_output)
                    store_xml(time_lines, timestamp_xml_out)
                else:
                    pass
            file_names(derivs_folder)


            # def remove_numbers(text_string):
            # return re.sub(r'\W\d+\W', '', text_string)


def scrape_text(in_file):
    transcript_lines = []
    with open(in_file, "r") as f:
        for line in f:
            if not any(char.isdigit() for char in line):
                transcript_lines.append(line)
    return transcript_lines


# Finds all the lines with timestamp info from an audiogrep output file,
# and appends them into a list that gets returned
def scrape_timestamps(in_file):
    timestamp_lines = []
    with open(in_file, "r") as f:
        for line in f:
            if '<speaker>' in line:
                timestamp_lines.append(line)
            elif any(char.isdigit() for char in line):
                timestamp_lines.append(line)
    return timestamp_lines


# Writes the text returned from scrape_text to a file
def store_text(transcript, out):
    with open(out, "w") as f:
        for transcript_lines in transcript:
            f.write(transcript_lines)


# Writes the timestamp lines returned from scrape_timestamps to a text file
def store_timestamps(timestamps, out):
    with open(out, "w") as f:
        for timestamp_lines in timestamps:
            f.write(timestamp_lines)


# Writes the timestamp lines returned from scrape_timestamps to an xml file
def store_xml(timestamps, out):
    with open(out, "w") as f:
        for timestamp_lines in timestamps:
            f.write(timestamp_lines)


# Returns the text portion of a 'this is text 1.234 2.345 0.123456' expression.
def t_split(line):
    pattern = r'(.+) ([0-9]+.[0-9]+) ([0-9]+.[0-9]+) (0.[0-9]+)'
    result = re.match(pattern, line)
    if (result):
        return result.groups( )

# Main
make_folders(path)
