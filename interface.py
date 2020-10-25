import json
import os

from pydub import AudioSegment
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBMjson should be the JSON provided by the IBM voice recog, whether JSON format or the string
# mp3filename should be formatted as "filename.mp3", tell me if you want that changed
def mp3AndTimestampsToSpliced(IBMjson, mp3filename, directory):
    decodedJSON = json.loads(IBMjson)
    results = decodedJSON["results"]
    alternatives = results[0]["alternatives"]
    timestamps = alternatives[0]["timestamps"]
    song = AudioSegment.from_mp3("data/input/" + mp3filename + ".mp3")
    if not os.path.isdir("data/" + directory):
        os.mkdir("data/" + directory)
    for wossname in timestamps:
        word = wossname[0].lower()
        start = wossname[1]
        end = wossname[2]
        spliced = song[start*1000:end*1000]
        path = "data/" + directory + "/" + word + ".mp3"
        spliced.export(path, format="mp3")

def downloadAsMP3(uri):
    if not os.path.isfile("data/input/" + uri[-11:] + ".mp3"):
        os.system("youtube-dl.exe -x --audio-format mp3 --audio-quality 192k -o data/input/%(id)s.%(ext)s {}".format(uri))

def youtubeIBManalysis(mp3filename, tokenfilename):
    print("[watson] Starting upload to IBM...")
    f = open(tokenfilename, "r")
    APItoken = f.readline().strip("\n")
    serviceurl = f.readline()
    f.close()

    authenticator = IAMAuthenticator(APItoken)
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url(serviceurl)

    models = service.list_models().get_result()
    # print(json.dumps(models, indent=2))

    model = service.get_model('en-US_BroadbandModel').get_result()
    # print(json.dumps(model, indent=2))

    with open(join(dirname(__file__), "data\\input\\" + mp3filename + ".mp3"),
              'rb') as audio_file:
        return json.dumps(
            service.recognize(
                audio=audio_file,
                content_type='audio/mp3',
                timestamps=True,
                word_confidence=False,
                speech_detector_sensitivity=1.0).get_result(),
            indent=2)

def completeSlicer(url):
    downloadAsMP3(url)
    if not os.path.isdir("data/" + url[-11:]):
        IBMjson = youtubeIBManalysis(url[-11:], "token.txt")
        mp3AndTimestampsToSpliced(IBMjson, url[-11:], url[-11:])