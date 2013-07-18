import urllib
import csv
import time

master = []
current = []
#rejected = []

def get_page(link):
    attempts = 0
    initial = ''    
    while attempts < 5:
        try:
            initial = urllib.urlopen(link)
            break
        except:
            print "Error, trying again"
            if attempts == 0:
                time.sleep(15)
            elif attempts == 1:
                time.sleep(60)
            elif attempts == 2:
                time.sleep(180)
            else:
                time.sleep(1000)
            attempts += 1
    page = []
    for i in initial:
        page.append(i)
    return page

def construct_link(cik):
    cik = cik[0]
    part1 = 'http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK='
    part2 = '&filenum=&State=&Country=&SIC=&owner=exclude&Find=Find+Companies&action=getcompany'    
    link = part1+cik+part2
    return link

CIKs = csv.reader(open("CIK.csv", "rU"))
start = time.clock()
for i in CIKs:
    print "Checking: "+str(i[0])
    print str((CIKs.index(i)/len(CIKs))*100)+"% of CIKs checked..."
    curr = time.clock()
    print "Estimated time remaining: "+str((curr-start/CIKs.index(i))*(len(CIKs)-CIKs.index(i)))
    valid = True
    page = get_page(construct_link(i))
    for e in page:
        if "No matching CIK." in e:
            #rejected.append(i)
            valid = False
            print "     "+str(i[0])+" is invalid"
            break
        else:
            continue
    if valid:
        #page2 = get_page(construct_link(i))
        for k in page:
            if '<td nowrap=' in k:
                position = page.index(k)
                for o in range(0,5):
                    new = page[position+1]
                    if '<td>' in new:
                        year = new.split('-')[0]
                        year = year.split('>')[1]
                        if int(year) >= 2012:
                            current.append(i)
                            master.append(i)
                            print "     "+str(i[0])+" is valid and current ("+str(len(current))+" total current)"
                        else:
                            master.append(i)
                            print "     "+str(i[0])+" is valid ("+str(len(master))+" total valid)"
                        break
                    else:
                        position +=1
                break
end = time.clock()
print "runtime: "+str(end-start)
with open("master_CIK.csv", "w") as out_file:
    for c in master:
        out_file.write("%s\n" % (c[0]))

with open("current_CIK.csv", "w") as out_file2:
    for d in current:
        out_file2.write("%s\n" % (d[0]))

#with open("rejected_CIK.csv", "w") as out_file3:
 #   for e in rejected:
  #      out_file3.write("%s\n" % (e[0]))