import re
import os
import sys
import csv

#global 변수
folderPath  = ""
filePath    = ""

readALines  = []
cutLines    = []
#

#저장을 위한 함수
def writeFile(saveLines) :
    global filePath

    baseName, _ = os.path.splitext(filePath)
    outputPath = baseName + '2Covn.csv'

    with open(outputPath, 'w', newline='') as csvFile :
        csvWriter = csv.writer(csvFile)

        for lines in saveLines :
            for line in lines :
                csvWriter.writerow(line.strip().split())
    return 0

#현재 폴더 위치를 받아오는 함수
def setFolderPath() :
    print("set Folder Path")

    global folderPath

    if getattr(sys, 'frozen', False):
        # 실행 파일로 실행될 때
        folderPath = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # 스크립트로 실행될 때
        folderPath = os.path.dirname(os.path.abspath(__file__))

    return 0

#리스트 슬라이싱 함수
def slicing(list_1, list_2, num, isFront) :
    """
    list_1에 list_2에 num을 기준으로
    True : 앞을
    False : 뒤를
    담는다.
    """
    if isFront :
        list_1 = list_2[:num]
    
    else :
        list_1 = list_2[num:]

    return list_1

#필요 없는 부분을 조정하는 함수. 
#앞에서 30번째까지 지우는 방식을 사용
def fixText() :
    global readALines, filePath, cutLines

    #local변수 선언부
    slaveNum = 0

    isPassFilter_1 = False
    #

    filter_1 = "slaves found"

    for text in readALines :
        if filter_1 in text :
            slaveNum = int(re.search(r'\d+', text).group())
            isPassFilter_1 = True
            break
    
    if not isPassFilter_1 :
        return 1
    
    # debug
    #readALines = PDOFilter()
    #return 0
    #

    if "map" in filePath :
        cutLines = PDOFilter(slaveNum)
    
    else :
        cutLines = SDOFilter(slaveNum)

    return 0

# 바로 위 함수에서 사용할 필터에 대한 함수
## SDO INFO에서 원하는 정보만 뽑아오기 위함
def SDOFilter(repeatNum) :
    #Global 변수 사용하겠다고 이야기 함.
    global cutLines

    #local 변수 선언부부
    x               = 0
    lenth           = 0
    countX          = 0
    countLen        = 0
    lineNum         = 0

    filter_1        = "CoE Object Description found,"
    filter_2        = "Configured address:"

    isPassFilter_1  = False

    locateList      = []
    bittleList      = []
    resultList      = []
    #

    locateList = readALines

    bittleList.append("Slave:1")

    for _ in range(repeatNum) :

        for text in locateList :
            if filter_2 in text :
                bittleList.append(text)

            if filter_1 in text :
                x = int(re.search(r'\d+', text).group())
                isPassFilter_1 = True
                break

            lineNum = lineNum + 1
        
        if not isPassFilter_1 :
            return 1
        
        locateList = slicing(locateList, locateList, lineNum + 1, False)

        lenth = len(locateList)

        while True :
            if countLen == lenth :
                break

            text = locateList[countLen]

            countLen = countLen + 1

            if text.strip() == "":
                continue

            if "Slave:" in text :
                bittleList.append(text)
                break;

            if not text.startswith(' ') :
                countX = countX + 1

            if countX > x :
                return 1
            
            text = re.sub(r'\s+', ' ', text)
            
            bittleList.append(f'{countX} {text}')

        
        x               = 0
        lenth           = 0
        countX          = 0
        countLen        = 0
        lineNum         = 0

        resultList.append(bittleList[:])

        bittleList.clear()

        


    return resultList

## PDO INFO에서 원하는 정보만 뽑아오기 위함
def PDOFilter(repeatNum) :
    #Global 변수 사용하겠다고 이야기 함.
    global cutLines

    #local 변수 선언부
    x              = 0
    lenth          = 0
    lineNum        = 0
    countLen       = 0

    filter_1       = "PDO mapping according to CoE :"
    filter_2       = "SM"

    isPassFilter_1 = False

    locateList     = []
    smNumList      = []
    resultList     = []
    #

    locateList = readALines

    smNumList.append("Slave:1")

    for _ in range(repeatNum) :
        #첫번째 필터를 거쳐서 찾음.
        for text in locateList :
            if filter_1 in text :
                isPassFilter_1 = True
                break
            lineNum = lineNum + 1

        if not isPassFilter_1 :
            return 1
        
        #담는 역할을 함.
        locateList = slicing(locateList, locateList, lineNum + 1, False)

        lenth = len(locateList)

        #두번째 필터를 거쳐 저장됨.
        # test 중
        while True :
            if countLen == lenth :
                break

            text = locateList[countLen]

            countLen = countLen + 1

            if text.strip() == "":
                continue

            if "Slave:" in text :
                smNumList.append(text)
                break;

            if filter_2 in text :
                indexNum = text.find(filter_2)
                x = int(text[indexNum + len(filter_2)])
                continue

            text = re.sub(r'\s+', ' ', text)

            smNumList.append(f'{x} {text}')

        locateList = slicing(locateList, locateList, lineNum + 1, False)
        x              = 0
        lenth          = 0
        lineNum        = 0
        countLen       = 0

        isPassFilter_1 = False
        
        resultList.append(smNumList[:]) 

        smNumList.clear()   

    return resultList
#

#txt 파일을 읽어와서 readALines 변수에 담는 역할할
def readFile() :
    global readALines, filePath

    #with open 구문은 자동으로 close를 사용해 주기 때문에 close를 따로 사용할 필요가 없다.
    #앞 공백을 지우면 안됨. 앞에 공백을 해야하는 것이 있기 때문임 SDOFilter에서 사용할 것임.
    with open(filePath, 'r', errors='ignore') as txtFile :
        for txt in txtFile :
            readALines.append(txt.rstrip()) #문장 뒤에 오는 공백 제거
    
    '''
    #with open 구문은 자동으로 close를 사용해 주기 때문에 close를 따로 사용할 필요가 없다.
    with open(filePath, 'r') as txtFile :
        #python의 내장 함수 중 하나인 enumerate를 이용하는데 for문을 2개를 사용하는 느낌을 낼 수 있다.
        for line_num, txt in enumerate(txtFile, 1):
            # 1부터 시작하여 30까지는 continue를 하게 됨.
            if line_num > 30 :
                continue
            readALines.append(txt.rstrip()) #문장 뒤에 오는 공백 제거
    
    '''

    return 0

def main() :
    global filePath

    if len(sys.argv) != 2 :
        print("error no argv")
        exit()

    filePath = sys.argv[1]
    print(filePath)

    readFile()
    fixText()
    writeFile(cutLines)

    return 0

def debug() :
    global filePath

    filePath = "mapINFO.txt"
    readFile()
    fixText()
    writeFile(cutLines)

#debug()
main()