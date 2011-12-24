

import os,sys,shutil
from datetime import datetime


if len(sys.argv) < 3:
    print 'Usage: python DialogResult.py Dir1 Dir2 [detail]'
    exit()
elif len(sys.argv) == 4 and sys.argv[3] == 'detail':
    specifyResult = True
else:
    specifyResult = False
        
paths = sys.argv[1:3]

dialogStats = []
noTurnNumber = 0
sufficientTurnNumber = 0
shortDialogSuccessNumber = 0
successNumber = 0
totalTurnNumber = 0

for path in paths:
    if os.path.isdir(path):
        for root,dirs,files in os.walk(path):
            for filename in files:
                if filename.endswith('dialog.log'):
                    turnNumber = 0
                    dialogResult = ''
                    dialogSuccess = False
                    dialogNumber = int(filename.split('-')[-2])
                    print 'Dialog number: %d'%dialogNumber
                    filename = os.path.join(root,filename)
                    print filename
                    file = open(filename,'r')
                    contents = file.read().split('\n')
                    date = contents[0].split(' ')[0]
                    print date
                    hour = int(contents[0].split(' ')[1].split(':')[0])
                    print hour
                    if  hour >= 9 and hour < 19:
                        file.close()
                        continue  
#                    for line in reversed(contents):
                    for line in contents:
#                        print line
                        if line.find('Dialog result:') > -1:
                            print line
                            dialogResult = line.split(':')[-1].strip()
                            print dialogResult
                            if dialogResult == 'Fail':
                                dialogSuccess = False
                            else:
                                dialogSuccess = True
#                                if turnNumber < 4:
#                                    shortDialogSuccessNumber += 1
                                successNumber += 1
#                            dialogStats.append((date,dialogNumber,dialogSuccess,turnNumber,dialogResult))
#                            break
                        if line.find('Number of turns:') == 0:
                            print line
                            turnNumber = int(line.split(':')[-1].strip())
                            print turnNumber
                            if turnNumber == 0:
                                noTurnNumber += 1
                            if turnNumber >= 4:
                                sufficientTurnNumber += 1
                            elif dialogSuccess:
                                shortDialogSuccessNumber += 1
                            totalTurnNumber += turnNumber
                            dialogStats.append((date,dialogNumber,dialogSuccess,turnNumber,dialogResult))
                            break
                    file.close()
                            
report = open('DailyReport-%s.txt'%datetime.now().isoformat().split('T')[0],'w')
report.write("\nStatistics for RL Let's Go System on %s\n"%date)
report.write("----------------------------------------------\n")
report.write("Number of sessions: %d\n"%len(dialogStats))
report.write("Number of no-turn sessions: %d\n"%noTurnNumber)
report.write("Number of sessions >= 4 turns: %d\n"%sufficientTurnNumber)
report.write("Average number of turns per sessions: %f\n"%(0.0 if len(dialogStats) == 0 else float(totalTurnNumber)/len(dialogStats)))
report.write("\n")
report.write("Number of estimated successes: %d (%f%%)\n"%\
             (successNumber,0.0 if sufficientTurnNumber == 0 else float(successNumber)/(sufficientTurnNumber+shortDialogSuccessNumber)*100))
report.write("----------------------------------------------\n")
report.write("\n")
report.write("Session Specific Statistics (Session: Total Turns, Success):\n")
for (date,dialogNumber,dialogSuccess,turnNumber,dialogResult) in dialogStats:
    report.write("Session %s-%d: "%(date,dialogNumber))
    report.write("%d, "%turnNumber)
    report.write("%s"%('Success' if dialogSuccess else 'Fail'))
    report.write("%s"%(', %s\n'%dialogResult if specifyResult else '\n'))
        
report.close()
