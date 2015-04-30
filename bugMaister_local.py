import os
import sys
from nltk import sent_tokenize, word_tokenize, pos_tag

reload(sys)
sys.setdefaultencoding('utf8')


# filter keywords by word type
def filterTags( tagsToFilter ):
        ct       = 0
        toDelete = []
        for word, tag in tagsToFilter:
                if tag not in ["NNP","NN","JJ","NNS","VB","VBD","VBC"]:
                    toDelete = [ct] + toDelete #we will delete from end to beginning
                ct += 1
        for idx in toDelete:
                del tagsToFilter[idx]
        return tagsToFilter

descSearchString    = "Description:"
descSearchStringLen = len(descSearchString)
subjSearchString    = "Subject:"
subjSearchStringLen = len(subjSearchString)
idSearchString      = "ID:"
idSearchStringLen   = len(idSearchString)

bugDir              = "/home/scantrel/testing/bugs/"
bugMatchValues      = []
bugIds              = []

inputSubj           = raw_input('Enter bug subject: ')
iSubjTokens         = word_tokenize(inputSubj)
iSubjTags           = pos_tag(iSubjTokens)
iSubjTags           = filterTags(iSubjTags)
inputDesc           = raw_input('Enter bug desc: ')
iDescTokens         = word_tokenize(inputDesc)
iDescTags           = pos_tag(iDescTokens)
iDescTags           = filterTags(iDescTags)

#loop through bugs saved locally and
#compare keywords with input bug
for bug in os.listdir(bugDir):
        subjMatchValue      = 0
        descMatchValue      = 0
        bugFile             = open(bugDir + bug)
        bugTxt              = bugFile.read()
        bugDesc             = bugTxt[bugTxt.find(descSearchString)+descSearchStringLen:]
        bugSubj             = bugTxt[bugTxt.find(subjSearchString)+subjSearchStringLen:bugTxt.find(descSearchString)]
        bugID               = bugTxt[bugTxt.find(idSearchString)+idSearchStringLen:bugTxt.find(subjSearchString)]
        bugIds              = bugIds + [bugID]
        bugSubjTokens       = word_tokenize(bugSubj)
        bugSubjTags         = pos_tag(bugSubjTokens)
        bugSubjTags         = filterTags(bugSubjTags)
        bugDescTokens       = word_tokenize(bugDesc)
        bugDescTags         = pos_tag(bugDescTokens)
        bugDescTags         = filterTags(bugSubjTags)

        for bugWord in bugSubjTags:
                for inputWord in iSubjTags:
                        if bugWord==inputWord:
                            subjMatchValue += 1
        
        for bugWord in bugDescTags:
                for inputWord in iDescTags:
                        if bugWord==inputWord:
                                descMatchValue += 1

        if len(bugSubjTags) != 0:
            subjMatchPercentage = (float(subjMatchValue) / len(bugSubjTags)) * 100.0
            descMatchPercentage = (float(descMatchValue) / len(bugDescTags)) * 100.0
        else:
            subjMatchPercentage = 0.0
            descMatchPercentage = 0.0

        bugMatchValues = bugMatchValues + [(subjMatchPercentage+descMatchPercentage) / 2]
        bugFile.close()

#loop through bugs and output match percentage
ct = 0
for bg in bugIds:
        print bg + str(int(bugMatchValues[ct])) + '%'
        ct += 1
