import os
import csv
import argparse
from pocketsphinx import AudioFile

data_path = os.getcwd()
parser = argparse.ArgumentParser(description='AutoCensor words in an audio file')
parser.add_argument('audioFile', type=str, help='audio file to censor')
args = parser.parse_args()
aF = args.audioFile
if (aF.split('.')[1] != 'wav'):
    os.system('ffmpeg -i ' + aF + ' ' + aF.split('.')[0] + '.wav') # convert non-wav to wav
    aF = aF.split('.')[0] + '.wav'
badwords = open("badwords.txt")
open("words.csv", "w").close()
f = open('words.csv', 'r+')
writer = csv.writer(f)
writer.writerow(['start', 'end', 'word'])
data = list(badwords)
r = []
fps = 100
config = {
    'verbose': False,
    'buffer_size': 2048,
    'audio_file': os.path.join(data_path, aF),
    'frate': fps,
    'no_search': False
}
audio = AudioFile(**config)
for phrase in audio:
    print(phrase)
    for s in phrase.seg():
        writer.writerow([s.start_frame / fps, s.end_frame / fps, s.word]) # writing timestamps of words to csv
mycsv = csv.reader(f)
for i in badwords:
    for row in mycsv:
        if row[2] == i:
            writer.writerow(row)


# Code Wasteland
# I leave code here and come back to it if I need to
# print('| %4ss | %4ss | %8s |' % (s.start_frame / fps, s.end_frame / fps, s.word))
# writer.writerow(['{0}'.format(s.start_frame),'{0}'.format(s.end_frame),'{0}'.format(s.word)]) ### this line of code is so long it doesnt fit on one line in brackets, generally it was a bad idea, i fixed it tho and it shall lay here in the code wasteland