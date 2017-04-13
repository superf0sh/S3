#!/usr/bin/python 

import argparse
import sys
import xml.sax
import os.path
import xml.dom.minidom
from getpass import getpass
from neo4jrestclient.client import GraphDatabase
from xml.dom.minidom import parse as p


parser = argparse.ArgumentParser()
parser.add_argument("--input", help='Input file in XML format', type=str, required=True)
args = parser.parse_args()


def getXMLfile():
    if os.path.isfile(args.input):
        print 'Found -> %s' % args.input
        return 0
    else:
        print 'ERROR: Unable to find -> %s' % args.input
        sys.exit()

def create_session():
    '''
    Gets IP of server & returns session token
    '''

    neoip = "0"
    neoip = raw_input('Enter IP of neo4j DB or press [ENTER] for localhost: ')

    if neoip == '':
        print "Using 'localhost' "
        neoip = 'localhost'
    neoun = "0"
    neoun = raw_input('Enter neo4j DB username or press [ENTER] for neo4j: ')

    if len(neoun) == 0:
        neoun = "neo4j"
    addr = 'https://' + neoip + ':7473/db/data/'
    gdb = GraphDatabase(addr, username=neoun, password=getpass('Enter neo4j password: '))
    return gdb

class SecurityEventHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.Provider = ""
        self.EventID = ""
        self.Version = ""
        self.Level = ""
        self.Task = ""
        self.Opcode = ""
        self.Keywords = ""
        self.TimeCreated = ""
        self.EventRecordID = ""
        self.Correlation = ""
        self.Execution = ""
        self.Channel = ""
        self.Computer = ""
        self.Security = ""
        self.UserData = ""
        self.SubjectUserName = ""
        self.SubjectDomainName = ""
        self.SubjectLogonId = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "Event":
            print "____________________________"
            print attributes["xmlns"]
        elif tag == "TimeCreated":
            spl_time = attributes["SystemTime"].split()
            print ("Sys Time", spl_time)
        elif tag == "Provider":
            print ("Name", attributes["Name"])
            print ("GUID", attributes["Guid"])
        elif tag == "Execution":
            print ("PID", attributes["ProcessID"])
            print ("TID", attributes["ThreadID"])

    def endElement(self, tag):
        if self.CurrentData == "Computer":
            print ("CN", self.Computer)
        elif self.CurrentData == "EventID":
            print ("EID", self.EventID)
        elif self.CurrentData == "Version":
            print ("Version", self.Version)
        elif self.CurrentData == "Level":
            print ("Level", self.Level)
        elif self.CurrentData == "Task":
            print ("Task", self.Task)
        elif self.CurrentData == "Opcode":
            print ("Opcode", self.Opcode)
        elif self.CurrentData == "Keywords":
            print ("KW", self.Keywords)
        elif self.CurrentData == "EventRecordID":
            print ("ERID", self.EventRecordID)
        elif self.CurrentData == "SubjectLogonId":
            print ("Sub LID", self.SubjectLogonId)


    def characters(self, content):
        if self.CurrentData == "Provider":
            self.Provider = content
        elif self.CurrentData == "EventID":
            self.EventID = content
        elif self.CurrentData == "Version":
            self.Version = content
        elif self.CurrentData == "Level":
            self.Level = content
        elif self.CurrentData == "Task":
            self.Task = content
        elif self.CurrentData == "Opcode":
            self.Opcode = content
        elif self.CurrentData == "Keywords":
            self.Keywords = content
        elif self.CurrentData == "EventRecordID":
            self.EventRecordID = content
        elif self.CurrentData == "Computer":
            self.Computer = content
        elif self.SubjectLogonId == "SubjectLogonId":
            self.SubjectLogonId = content
'''
def parseXML(xml_file):

    DOMTree = p(xml_file)
    events = DOMTree.documentElement
    event = events.getElementsByTagName('Event')

    for attr in event:
        erid = attr.getElementsByTagName('EventRecordID')[0]
        print ("Event Record ID", erid.childNodes[0].data)
        
        pid = attr.getElementsByTagName('Execution')[0]
        print ("Process ID", pid.getAttribute('ProcessID'))
        print ("Thread ID", pid.getAttribute('ThreadID'))
        
        eidq = attr.getElementsByTagName('EventID')[0]
        print ("Qualifiers", eidq.getAttribute('Qualifiers'))
        print ("EventID", eidq.childNodes[0].data)

        provider = attr.getElementsByTagName('Provider')[0]
        print ("Name", provider.getAttribute('Name'))
        print ("GUID", provider.getAttribute('Guid'))

        version = attr.getElementsByTagName('Version')[0]
        print ("Version", version.childNodes[0].data)

        level = attr.getElementsByTagName('Level')[0]
        print ("Level", level.childNodes[0].data)

        task = attr.getElementsByTagName('Task')[0]
        print ("Task", task.childNodes[0].data)

        opcode = attr.getElementsByTagName('Opcode')[0]
        print ("Opcode", opcode.childNodes[0].data)

        keywords = attr.getElementsByTagName('Keywords')[0]
        print ("Kewords", keywords.childNodes[0].data)

        timestamp = attr.getElementsByTagName('TimeCreated')[0]
        print ("TimeCreated", timestamp.getAttribute('SystemTime'))
        
        crrln = attr.getElementsByTagName('Correlation')[0]
        print ("Activity ID", crrln.getAttribute('ActivityID'))
        print ("Related Activity ID", crrln.getAttribute('RelatedActivityID'))

        channel = attr.getElementsByTagName('Channel')[0]
        print ("Channel", channel.childNodes[0].data)

        computer = attr.getElementsByTagName('Computer')[0]
        print ("Computer", computer.childNodes[0].data)
        
        uid = attr.getElementsByTagName('Security')[0]
        print ("UID", uid.getAttribute('UserID'))

        susid = attr.getElementsByTagName('SubjectUserSid')[0]
        print ("SubjectUserSid", susid.childNodes[0].data)

        sun = attr.getElementsByTagName('SubjectUserName')[0]
        print ("SubjectUserName", sun.childNodes[0].data)

        sudn = attr.getElementsByTagName('SubjectDomainName')[0]
        print ("SubjectDomainName", sudn.childNodes[0].data)

        slid = attr.getElementsByTagName('SubjectLogonId')[0]
        print ("SubjectLogonID", slid.childNodes[0].data)

    return 0
'''

def main():
    '''
    This was written to take in windows security event logs in xml format that has been converted 
    from evtx using [evtxdump.py] from https://github.com/williballenthin/python-evtx (Thanks!)
    Syntax for evtxdump.py is >> python evtxdump.py yourevents.evtx > yourevents.xml
    '''

    getXMLfile()
    parser =xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = SecurityEventHandler()
    parser.setContentHandler(Handler)
    parser.parse(args.input)
    #gdb = create_session()

    return 0

if __name__ == '__main__':
    main()
