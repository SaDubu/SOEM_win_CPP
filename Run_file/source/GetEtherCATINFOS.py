import subprocess
import os
import sys
import time

#실행 파일 이름 별 경로
readMapPath       = "readMapping.exe"
readSdoPath       = "readSdo.exe"

testInPath        = "test_in.exe"

socketParsherPath = "socketParsher.exe"

txt2CsvPath       = "txt2Csv.exe"
#

#txt 파일 이름
sdoTxt = "sdoINFO.txt"
pdoTxt = "mapINFO.txt"
#

#csv 파일 이름 결과 확인하기 위함
sdoCSV = "sdoINFO2Covn.csv"
pdoCSV = "mapINFO2Covn.csv"
#

#global 변수
folderPath = ""
#

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

def runExeFile(filePath) :
    try:
        process = subprocess.run(filePath, cwd=folderPath)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)

    return 0

def scheduler() :
    count = 0
    #soem을 통해 각 포트(socket) 정보를 담은 txt 파일 생성
    runExeFile(testInPath)

    #위에서 생성된 txt에서 BackHOFF 단어가 들어간 포트(socket) 찾아 txt로 저장
    runExeFile(socketParsherPath)

    #위에서 생성된 txt를 통해 ethercat장비에 접근 하여 PDO 정보 추출
    runExeFile(readMapPath)
    #SDO 정보 추출
    runExeFile(readSdoPath)

    while True:
        if count == 20 :
            return 1
        if os.path.exists(pdoTxt) and os.path.exists(sdoTxt):
            print("The file exists. Moving on now.")
            break  # 파일이 존재하면 루프 종료
        else:
            print("The file does not exist. Checking again...")
            time.sleep(0.5)  # 0.5초 후에 다시 확인
            count += 1

    #위에서 생성된 txt파일을 이용하여 사전에 구성된 필터를 거쳐 csv파일로 나오게 됨 PDO
    runExeFile([txt2CsvPath, pdoTxt])
    #SDO
    runExeFile([txt2CsvPath, sdoTxt])

    while True:
        if count == 200 :
            return 1
        if os.path.exists(pdoCSV) and os.path.exists(sdoCSV):
            print("The file exists. Done!!!")
            break  # 파일이 존재하면 루프 종료
        else:
            print("The file does not exist. Checking again...")
            time.sleep(0.5)  # 0.5초 후에 다시 확인
            count += 1

    return 0

setFolderPath()

scheduler()