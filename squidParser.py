import sys
import os
import calendar, datetime

#need to do: sudo chmod +r /var/log/squid/access.log
log = open("/var/log/squid/access.log","r")
data = log.readlines()
log.close()

websiteList = []
for i in range(len(data)):
    a = data[i].split()
    if a[3] != "TCP_DENIED/403":
        websiteList.append(a[6])
        websiteList.append(a[2])
        websiteList.append(datetime.datetime.fromtimestamp(int(float(a[0]))))

web = ["www.facebook.com","piazza.com","twitter"]
ifBan = [".facebook.com",".piazza.com",".twitter.com"] #needs format .website.___
timeLimits = [2,4,10] #in minutes

time = []
allTimes = []
for i in range(len(web)):
    time.append([])
    allTimes.append([])
for i in range(0,len(websiteList),3):
    ap = 0
    for j in range(len(web)):
        if web[j] in websiteList[i]:
            print(websiteList[i+1], " visited: ", websiteList[i], "\ton: ", websiteList[i+2])
            time[j].append(websiteList[i+2])

for i in range(len(time)):
    pts = time[i]
    totalTime = 0
    for indx,data in enumerate(pts):
        if(indx < (len(pts)-1)):
            elapsedTime = pts[indx+1] - data
            minVisited = divmod(elapsedTime.total_seconds(),60)[0]
            if(minVisited < 5):
                totalTime += minVisited
    allTimes[i] = totalTime

#sudo chmod a+w /etc/squid/ban_domains.txt
bansFD = open("/etc/squid/ban_domains.txt","a")
for i in range(len(timeLimits)):
    if(allTimes[i] > timeLimits[i]):
        print("time exceeded for: ", web[i])
        bansFD.write(ifBan[i]+'\n')
bansFD.close()

