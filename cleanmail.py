import imaplib
import re
import sys

class minmap:#class to hold each fic, the earliest chapter found, and the UIDs of the emails.
    def __init__(self):
        self.dict = {}
        self.bad = []
    def add(self, name, chapter, position):
        if name not in self.dict:#If it's a newly-found fic
            self.dict[name] = (int(chapter), position) #register its chapter as the earliest
        else:#duplicate fic
            if self.dict[name][0] > int(chapter):#if it's an earlier chapter
                self.bad.append(((name,self.dict[name][0]), self.dict[name][1])) #put the remembered email on the bad list
                self.dict[name] = (int(chapter), position) #keep the new email, and update the earliest chapter
            else: 
                self.bad.append(((name, chapter), position)) #If later, throw out.
    def clear(self):
        self.dict = {}
        self.bad = []

mail = imaplib.IMAP4_SSL("imap.gmail.com") #When connecting to Gmail via IMAP, you have to tell Gmail to accept connections from "less secure" applications. My password is secure enough, so I'm not worried.
user = input("Username:")
password = input("Password:")
print("Logging in...")
try:
    mail.login(user, password) #I'm not leaving my user/pass in plaintext!
except imaplib.IMAP4.error:
    sys.exit("Bad user/pass")
    
print("Logged in, retrieving email list...")
mail.select("Fanfic/FanFiction.net") #All the fics are in here. (At least, all the ones this script can prune)
mailList = mail.uid("SEARCH", None, "ALL")[1][0].split() #Get a list of all UIDs of fic emails.
sorter = minmap()
print("Mail list retrieved, parsing...")
for email in mailList:
    subject = mail.uid("fetch", email, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')[1][0][1].decode("utf-8") #Get the subject line, without marking the email as read
    match = re.compile(r"Subject: (?:(Chapter: )|(?:Story: |Crossover: ))(.*?)(?(1) Ch(\d+)) by").match(subject)
    #Complex regex to determine if it's a new story, get the name, and get the chapter if it's not new.
    #Example new story subject: "Subject: Story: This is a new story by Brian"
    #Example updated story subject: "Subject: Chapter: This is an updated story Ch17 by Brian"
    if match is not None: #If the subject could be parsed by the regex (One story includes japanese characters in its subject, and no matter how I decode it, I can't get it to output sensible text...)
        dump, name, chapter = match.groups()
        if chapter is None: #If it's a new story, then the "chapter" group will be skipped in the regex, and so will be None.
            chapter = 1
        sorter.add(name, chapter, email) #Register this email with the minmap defined above

for email in sorter.bad: #For each email that isn't wanted
    print("Deleting duplicate " + email[0][0] + " Ch" + email[0][1] + "...")
    mail.uid("COPY", email[1], "[Gmail]/Trash") #Gmail deletes any email you copy into "Trash" via IMAP. 

mail.close()
mail.logout()
final = "Completed. Deleted " + str(len(sorter.bad)) + " duplicate"
if len(sorter.bad) != 1:
      final += "s"
final += "."
print(final)
