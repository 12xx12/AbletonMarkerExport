import csv
import gzip
import sys
import os

from lxml import objectify


def bartominute(s: str, tempo: int) -> str:
    a = float(s)
    speed = 1 / (tempo / 60)
    time = a * speed
    frames = round(time * 30)

    seconds = frames // 30
    frames -= seconds * 30

    minutes = seconds // 60
    seconds -= minutes * 60

    hours = minutes // 60
    minutes -= hours * 60

    return str(hours) + ":" + str(minutes).zfill(2) + ":" +\
                        str(seconds).zfill(2) + ":" + str(frames).zfill(2)


def takesecond(elem):
    return float(elem[1])


with gzip.open(sys.argv[1], "rt") as file, open(sys.argv[1][:-4] + ".xml",
                                                "w") as outfile:
    projectFile = file.read()
    outfile.write(projectFile)

with open(sys.argv[1][:-4] + ".xml", "rb") as file:
    contents = file.read()

root = objectify.fromstring(contents)
attrib = root.attrib

locator = root.LiveSet.Locators.Locators

array = []

for child in locator.getchildren():
    helperArray = ["", ""]
    for e in child.getchildren():
        if e.tag == "Name":
            helperArray[0] = e.attrib["Value"].replace(" ", "")
        elif e.tag == "Time":
            helperArray[1] = e.attrib["Value"].replace(" ", "")
    array.append(helperArray)

tempo = float(
    root.LiveSet.MasterTrack.DeviceChain.Mixer.Tempo.Manual.attrib["Value"])

array.sort(key=takesecond)

with open(sys.argv[1][:-4] + ".csv", "w", newline='') as exportFile:
    writer = csv.writer(exportFile, delimiter=',')
    writer.writerow(["#", "Name", "Start", "End", "Length"])
    for i, e in enumerate(array):
        writer.writerow(["M" + str(i), e[0], bartominute(e[1], tempo), "", ""])

os.remove(sys.argv[1][:-4] + ".xml")
