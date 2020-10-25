import time

import pydub
import os
from gtts import gTTS


# Split string into a list of MP3 paths.
def splitIntoWords(string: str) -> [str]:
    words = []
    map = {',': "_comma", ' ': "_space", '.': "_period"}
    stringBuilder = ""
    for char in string:
        if (char in map.keys()) and stringBuilder != "":
            words.append(stringBuilder.replace(" ", ""))
            stringBuilder = ""
            words.append(map.get(char))
        else:
            stringBuilder += char
    return words


# Seperate directories by /
def toDirectory(listOfDirectories: [str]) -> str:
    length = len(listOfDirectories)
    stringBuilder = ""
    if (length > 0):
        for i in range(0, length):
            if (i == length - 1):
                stringBuilder += listOfDirectories[i]
            else:
                stringBuilder += listOfDirectories[i] + "/"
    return stringBuilder


# Generate generic mp3 is one doesn't exist.
def generateGeneric(word: str, genericPath: str):
    language = 'en'
    MP3File = gTTS(text=word, lang=language, slow=False)
    open(genericPath, 'w').close()
    MP3File.save(genericPath)
    return


# generate mp3.
def getMp3FromWord(id: str, word: str) -> str:
    directory = ""
    extension = ".mp3"
    IdPath = toDirectory(["data", id, word + extension])
    genericPath = toDirectory(["data", "generic", word + extension])
    if (os.path.exists(IdPath)):
        directory = IdPath
    elif (os.path.exists(genericPath)):
        directory = genericPath
    else:
        generateGeneric(word, genericPath)
        directory = genericPath
    return directory


# Checks if a mp3 exists. If not, create a generic speak mp3.
def getMp3sFromWords(id: str, words: [str]) -> [str]:
    paths = []
    for word in words:
        paths.append(getMp3FromWord(id, word))
    return paths


# Takes a list of mp3 file paths and the output file path
# Returns true if successful and false otherwise
def stitchMp3s(mp3s: [str], outputFilePath: str) -> bool:
    finalAudio = pydub.AudioSegment.empty()
    for wordMp3 in mp3s:
        if "_space" in wordMp3:
            finalAudio += pydub.AudioSegment.silent(duration=20)
        elif "_comma" in wordMp3:
            finalAudio += pydub.AudioSegment.silent(duration=300)
        elif "_period" in wordMp3:
            finalAudio += pydub.AudioSegment.silent(duration=500)
        else:
            finalAudio += pydub.AudioSegment.from_mp3(wordMp3)
    finalAudio.export(outputFilePath, format="mp3")
    return True


# Takes a source folder for the MP3 root, such as "jesse" and a string that we want the user to say
# Returns a path to the final MP3
def stringToMp3(sourceFolderName: str, string: str) -> str:
    words = splitIntoWords(string)
    paths = getMp3sFromWords(sourceFolderName, words)
    outputFileName = "data/out/{}.mp3".format(time.strftime("%Y%m%d-%H%M%S"))
    stitchMp3s(paths, outputFileName)
    return outputFileName
