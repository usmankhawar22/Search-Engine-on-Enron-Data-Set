from pathlib import Path
import os,os.path
import email
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
import mysql.connector

stop_word = ["a's",',','_',"-","In", 'able','a','b','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s','t','u','v','w','x','y','z',"'", 'about', 'above', 'according', 'accordingly', 'across','s', 'actually', 'after', 'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'available', 'away', 'awfully', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', "c'mon", "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', "couldn't", 'course', 'currently', 'definitely', 'described', 'despite', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'during', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'far', 'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'four', 'from', 'further', 'furthermore', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'had', "hadn't", 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here', "here's", 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', "i'd", "i'll", "i'm", "i've", 'ie', 'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'inner', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's", 'its', 'itself', 'just', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'mainly', 'many', 'may', 'maybe', 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my', 'myself', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor', 'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably', 'probably', 'provides', 'que', 'quite', 'qv', 'rather', 'rd', 're', 'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', "t's", 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'value', 'various', 'very', 'via', 'viz', 'vs', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll", "we're", "we've", 'welcome', 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever', 'when', 'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who's", 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', "won't", 'wonder', 'would', 'would', "wouldn't", 'yes', 'yet', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'zero']

conn = mysql.connector.connect(user="root", password = "mankhokhar", host = "localhost")
cursor = conn.cursor()
cursor.execute("Drop schema if exists Mission_Enron1")
cursor.execute("Create schema Mission_Enron1")
cursor.execute("use Mission_Enron1")
cursor.execute("create table Rev_index_Subject (Word_S varchar(80),Doc_id int ,Word_Count_s int)")
#cursor.execute("create table Rev_index_Subject (Word varchar(80),Doc_id int ,Word_Count int, index (Word, Doc_ID))")
cursor.execute("create table Rev_index_Body (Word_B varchar(80),Doc_id_B int ,Word_Count_B int)")

formula1 = "Insert into Rev_index_Subject values (%s,%s,%s)"
formula2 = "Insert into Rev_index_Body values (%s,%s,%s)"


ps = PorterStemmer()

#emailFolder = "C:/Users/Ahmad Naeem Khokhar/Desktop/Data Structures and Algorithms/DSA proj/mail"
emailFolder = "C:/Users\Ahmad Naeem Khokhar/Downloads/Video/Compressed/enron_mail_20150507/maildir"

#getting all the paths of emal
allDocs = Path(emailFolder).glob("**/*")

#files = [x for x in allDocs if x.is_file()]
files=[]
for x in allDocs:
    if len(files)<50000:
        if x.is_file():
            files.append(x)
    else:
        break

print ("no. of file", len(files))
reverseIndex=dict()
subjectDic=dict()
count1=0
#ireverse indexing
print("Creating Index:")
for i in range(50000):
#reading emails
        print(count1)
        count1 = count1 + 1
        eachFile = files[i]
        myFile = open(eachFile,'r')
        emailData = myFile.read()
        doc_id=i
        tempEmail = email.message_from_string(emailData)
        tempSender = tempEmail['from']
        tempReciever = tempEmail['to']
        tempSubject = tempEmail['subject']
        tempDate = tempEmail['date']

        tempMessage = tempEmail.get_payload(decode = True)
        tempMessage = str(tempMessage)
        #if email has multiple parts like images etc
        if tempEmail.is_multipart():
                for part in tempEmail.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))

                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                                tempMessage = part.get_payload(decode = False)
                                break
        else:
                tempMessage = tempEmail.get_payload(decode = False)

                if (tempSender == '') :
                	break


        ps = PorterStemmer()


        dist = re.sub(r'[^a-zA-Z1-9]'," ",tempMessage)

        dis = word_tokenize(dist)
        sub = word_tokenize(tempSubject)

        reverseindex=[doc_id,1]
        for tokens in dis:
                ps.stem(tokens)
                if tokens in stop_word:
                        continue
                else:
                    if tokens in reverseIndex:
                        if reverseIndex[tokens][-1][0] == doc_id:
                                reverseIndex[tokens][-1][1]+=1
                        else: reverseIndex[tokens].append([doc_id, 1])
                    else:reverseIndex[tokens]=[[doc_id,1]]


        for tokens in sub:
                if tokens in stop_word:
                        continue
                else:
                    if tokens in subjectDic:
                        if subjectDic[tokens][-1][0] == doc_id:
                                subjectDic[tokens][-1][1]+=1
                        else: subjectDic[tokens].append([doc_id, 1])
                    else:subjectDic[tokens]=[[doc_id,1]]

#print(subjectDic)

#moving to database

print("adding subjects to database")
for h in subjectDic:
    for c1 in subjectDic[h]:
        doc = (h,c1[0],c1[1])
        cursor.execute(formula1,doc)
        count1 = count1 + 1
        if (count1%10000 == 0):
            print(count1, " subject entries added")
    conn.commit()

print("adding message to database")
count1 = 0
for word in reverseIndex:
    for c2 in reverseIndex[word]:
        doc = (word,c2[0],c2[1])
        cursor.execute(formula2,doc)
        count1 = count1 + 1
        if (count1%10000 == 0):
            print(count1, " body entries added")
    conn.commit()