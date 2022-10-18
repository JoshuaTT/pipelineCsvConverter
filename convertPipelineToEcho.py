import argparse
import csv
import json

pathToSubjMap = "./subjToDept.json"
pathToEmailMap = "./nameToEmail.json"

def convertCSV(pathToFileToConvert, pathToOutput, subjToDept, nameToEmail, term):
    """Converts a Harding Pipeline csv and converts it to an Echo csv."""
    organizations = {"Main": "HU - Main Campus"}

    readDicts = []
    with open(pathToFileToConvert, 'r', newline='', encoding="ISO-8859-1") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            readDicts.append(row)

    with open(pathToOutput, 'w', newline='') as echoFile:
        echoWriter = csv.writer(echoFile, delimiter=',')
        echoWriter.writerow(["Organization", "Department", "Course Code", "Course Name",
                         "Term", "Section Code", "Primary Instructor Email", "Secondary Instructor Emails"])
        for row in readDicts:
            org = organizations[row["CAMPUS"]]
            dept = subjToDept[row["SUBJ"]] if row["SUBJ"] in subjToDept.keys() else ""
            sect = row["SECT"].split('.')
            cc = f'{row["SUBJ"]}-{sect[0]}'
            className = row["TITLE"]
            email = nameToEmail[row["INSTR"]] if row["INSTR"] in nameToEmail else "TBA"
            echoWriter.writerow([org, dept, cc, className, term, sect[1], email])
        print(f"Output to: {pathToOutput}")

def getDepartments(pathToFormattedCSV, pathToOutput):
    """Reads an Echo CSV and write a json file containing a mapping from subhect to department."""
    readDicts = []
    with open(pathToFormattedCSV, 'r', newline='', encoding="ISO-8859-1") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            readDicts.append(row)

    subjToDept = {}
    for row in readDicts:
        subj = row["Course Code"].split('-')
        if subj[0] not in subjToDept.keys():
            subjToDept[subj[0]] = row["Department"]

    with open(pathToOutput, 'w') as jsonFile:
        json.dump(subjToDept, jsonFile, indent=4)

def getEmails(formattedPath, unformattedPath, outputPath):
    readUnformatted = []
    with open(unformattedPath, 'r', newline='', encoding="ISO-8859-1") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            readUnformatted.append(row)

    readFormatted = []
    with open(formattedPath, 'r', newline='', encoding="ISO-8859-1") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            readFormatted.append(row)

    pNames = []
    for urow in readUnformatted:
        pNames.append(urow["INSTR"])

    emails = []
    for frow in readFormatted:
        emails.append(frow["Primary Instructor Email"])
    
    pNames = set(pNames)
    emails = set(emails)
    nameToEmail = {}
    for name in pNames:
        eName = name.lower()
        eName = eName.split(" ")
        eName = f"{eName[0][0]}{eName[1]}" if len(eName) > 1 else eName
        for email in emails:
            if str(eName) in email:
                nameToEmail[name] = email
                break
        else:
            nameToEmail[name] = "none"

    with open(outputPath, 'w') as emailFile:
        json.dump(nameToEmail, emailFile, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="inputPath", help="Path to input csv file.")
    parser.add_argument("-o", dest="outputPath", default="./subjToDept.json", help="Path to output file.")
    parser.add_argument("-d", dest="getDepts", action="store_true", help="Only use this flag if you need to regenerate subjToDept.json")
    parser.add_argument("-e", dest="secondInput", default=None, help="Takes a second path to try and determine name/email mapping. Pass echo csv file to i argument.")
    parser.add_argument("-t", dest="term", help="The term for the converted file. (e.g. Fall 2022)")

    args = parser.parse_args()

    if args.getDepts:
        getDepartments(args.inputPath, args.outputPath)
    elif args.secondInput != None:
        getEmails(args.inputPath, args.secondInput, args.outputPath)
    else:
        with open(pathToSubjMap, 'r') as subToDep:
            subToDepMap = json.load(subToDep)
        with open(pathToEmailMap, 'r') as nToE:
            nameToEmail = json.load(nToE)
        convertCSV(args.inputPath, args.outputPath, subToDepMap, nameToEmail, args.term)

if __name__ == "__main__":
    main()