
import dataProcess
import SeekForPath
import init
import Schedue
carPath = './map/config_1/car.txt'
crossPath = './map/config_1/cross.txt'
roadPath = './map/config_1/road.txt'



path = "D:/pythonWorkplace/Huawei/map/1.txt"
secondProcess = []

thirdProcess = []
with open(path, 'r') as lines:
    for firstProcess in lines:
        firstProcess = firstProcess.strip().split('],')
    for i in range(len(firstProcess)):
        secondProcess.append(firstProcess[i].split('[')[1])
    secondProcess[-1] = secondProcess[-1].split(']')[0]

for i in range(len(secondProcess)):
    thirdProcess.append(secondProcess[i].split(','))

for i in range(len(thirdProcess)):
    for j in range(len(thirdProcess[i])):
        thirdProcess[i][j] = int(thirdProcess[i][j].strip())

result = thirdProcess
carData, crossData, roadData = dataProcess.dataProcess(carPath, crossPath, roadPath)


last = []

for i in range(len(result)):
    road = []
    for j in range(len(result[i]) - 1):
        for z in range(len(roadData)):
            if roadData[z][-1] == 1:
                if ((result[i][j] == roadData[z][-3] and result[i][j + 1] == roadData[z][-2])
                    or (result[i][j] == roadData[z][-2] and result[i][j+1] == roadData[z][-3])):
                    road.append(roadData[z][0])
                else:
                    continue
            else:
                if (result[i][j] == roadData[z][-3] and result[i][j + 1] == roadData[z][-2]):
                    road.append(roadData[z][0])
                else:
                    continue
    last.append(road)


with open('./path.txt', 'w') as f:
    for i in range(len(last)):
        for j in range(len(last[i])):
            f.write(str(last[i][j]))
            if j != len(last[i]) - 1:
                f.write(',')
        f.write('\n')
    f.close()

