import car
import cross
import road

carPath = './map/config_1/car.txt'
crossPath = './map/config_1/cross.txt'
roadPath = './map/config_1/road.txt'

carData = []
crossData = []
roadData = []

if __name__ == "__main__":

    with open(carPath, 'r') as lines:
        for line in lines:
            carData.append(line)
    with open(roadPath, 'r') as lines:
        for line in lines:
            roadData.append(line)
    with open(crossPath, 'r') as lines:
        for line in lines:
            crossData.append(line)
    print(len(carData), len(roadData), len(crossData))