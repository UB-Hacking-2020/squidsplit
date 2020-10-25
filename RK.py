import json
from pydub import AudioSegment

# IBMjson should be the JSON provided by the IBM voice recog, whether JSON format or the string
# mp3filename should be formatted as "filename.mp3", tell me if you want that changed
def mp3AndTimestampsToSpliced(IBMjson, mp3filename):
    decodedJSON = json.loads(IBMjson)
    results = decodedJSON["results"]
    alternatives = results[0]["alternatives"]
    timestamps = alternatives[0]["timestamps"]
    song = AudioSegment.from_mp3(mp3filename)
    directory = mp3filename.strip(".mp3")
    for wossname in timestamps:
        word = wossname[0].lower()
        start = wossname[1]
        end = wossname[2]
        spliced = song[start*1000 : end*1000]
        path = "data/" + directory + "/" + word + ".mp3"
        spliced.export(path, format="mp3")