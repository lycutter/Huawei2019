

path = "D:/pythonWorkplace/Huawei/map/1.txt"
with open(path, 'r') as lines:
    for line in lines:
        print(line.split(','))