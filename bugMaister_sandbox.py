import os
import sys
import json
from nltk import sent_tokenize, word_tokenize, pos_tag

reload(sys)
sys.setdefaultencoding('utf8')


print "                                                                                                  (\.   \      ,/)"
print "                                                                                                   \(   |\     )/"
print "    ___   __  _______  _________________ ____________  __  ______   _________________  ____        //\  | \   /\\\\"
print "   / _ | /  |/  / __/ /_  __/  _/ ___/ //_/ __/_  __/ /  |/  / _ | /  _/ __/_  __/ _ \/ __ \\      (/ /\_#oo#_/\ \)"   
print "  / __ |/ /|_/ /\ \    / / _/ // /__/ ,< / _/  / /   / /|_/ / __ |_/ /_\ \  / / / , _/ /_/ /       \/\  ####  /\/"
print " /_/ |_/_/  /_/___/   /_/ /___/\___/_/|_/___/ /_/   /_/  /_/_/ |_/___/___/ /_/ /_/|_|\____/             `##'\n\n"                                                                                                              

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

def loadTickets():
        with open('result.json') as result_file:
            result = json.load(result_file)
        return result

percentFilter       = 50
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
ticketHistory = loadTickets()
for ticket in ticketHistory["result"]:
        subjMatchValue      = 0
        descMatchValue      = 0
        bugDesc             = str(ticket["description"])
        bugSubj             = str(ticket["short_description"])
        bugID               = str(ticket["number"])
        bugIds              = bugIds + [bugID]
        bugSubjTokens       = word_tokenize(bugSubj)
        bugSubjTags         = pos_tag(bugSubjTokens)
        bugSubjTags         = filterTags(bugSubjTags)
        bugDescTokens       = word_tokenize(bugDesc)
        bugDescTags         = pos_tag(bugDescTokens)
        bugDescTags         = filterTags(bugSubjTags)

        #subject to subject
        for bugWord in bugSubjTags:
                for inputWord in iSubjTags:
                        if str(bugWord).upper()==str(inputWord).upper():
                            subjMatchValue += 1
                            break
        #subject to description
        for bugWord in bugSubjTags:
                for inputWord in iDescTags:
                        if str(bugWord).upper()==str(inputWord).upper():
                            subjMatchValue += 1

        #description to description
        for bugWord in bugDescTags:
                for inputWord in iDescTags:
                        if str(bugWord).upper()==str(inputWord).upper():
                            descMatchValue += 1
                            break
        #description to subject
        for bugWord in bugDescTags:
                for inputWord in iSubjTags:
                        if str(bugWord).upper()==str(inputWord).upper():
                            descMatchValue += 1
                            break

        if len(bugSubjTags) != 0:
            subjMatchPercentage = (float(subjMatchValue) / len(bugSubjTags)) * 100.0
            descMatchPercentage = (float(descMatchValue) / len(bugDescTags)) * 100.0
        else:
            subjMatchPercentage = 0.0
            descMatchPercentage = 0.0

        bugMatchValues = bugMatchValues + [(subjMatchPercentage+descMatchPercentage) / 2]

#loop through bugs and output match percentage
ct = 0
for bg in bugIds:
        if int(bugMatchValues[ct]) >= percentFilter:
            print bg + ": " + str(int(bugMatchValues[ct])) + '%'
        ct += 1
