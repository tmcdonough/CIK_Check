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

def run_through(cik_list, outfile):
    reject_count = 0
    master_count = 0
    current_count = 0
    CIKs = csv.reader(open(cik_list, "rU"))
    CIKs2 = []
    for i in CIKs:
        CIKs2.append(i)
    with open(outfile, "w") as out_file:
        for i in CIKs2:
            entry = []
            curr = time.clock()
            print "Checking: "+str(i[0])
            print "*******************"
            print "*******************"
            currentct = float(CIKs2.index(i)+1)
            totalct = float(len(CIKs2))
            time_remaining_seconds = (((curr-start)/currentct)*(totalct-currentct))
            time_remaining_hours = (((((curr-start)/currentct)*(totalct-currentct))/60)/60)
            est_completed = (currentct/totalct)
            print str(currentct)+" of "+str(totalct)+" CIKs checked..."
            print str(est_completed*100)+'% of CIKs checked...'
            print "*******************"
            print "*******************"
            print "Estimated time remaining: "+str(time_remaining_hours)+" hours"
            valid = True
            page = get_page(construct_link(i))
            for e in page:
                if "No matching CIK." in e:
                    entry.append(["","",i[0]])
                    valid = False
                    reject_count+=1
                    print "     "+str(i[0])+" is invalid ("+str(reject_count)+" total rejected)"
                    for CURRENT_CIK, MASTER_CIK, REJECTED_CIK in entry:
                        out_file.write("%s,%s,%s\n" % (CURRENT_CIK, MASTER_CIK, REJECTED_CIK))
                    entry = []
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
                                if '-' in new:
                                    year = new.split('-')[0]
                                    year = year.split('>')[1]
                                else:
                                    year = new.split('>')[1]
                                    year = year[:4]
                                if int(year) >= 2012:
                                    entry.append([i[0],i[0],""])
                                    master_count+=1
                                    current_count+=1
                                    print "     "+str(i[0])+" is valid and current ("+str(current_count)+" total current)"
                                else:
                                    entry.append(["",i[0],""])
                                    master_count = master_count + 1
                                    print "     "+str(i[0])+" is valid ("+str(master_count)+" total valid)"
                                for CURRENT_CIK, MASTER_CIK, REJECTED_CIK in entry:
                                    out_file.write("%s,%s,%s\n" % (CURRENT_CIK.strip(), MASTER_CIK.strip(), REJECTED_CIK.strip()))
                                entry = []
                                break
                            else:
                                position +=1
                        break       

start = time.clock()
run_through("CIK.csv", "master.csv")
end = time.clock()
print "runtime: "+str(end-start)