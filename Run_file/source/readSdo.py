import subprocess
import os
import sys

#해당 폴더 위치
folderPath = ""

#EtherCAT에 연결된 port 정보가 담긴 txt 파일 지정 경로
filePath = "userChoose.txt"

#읽어온 EtherCAT에 연결된 Port정보를 바탕으로 sdo mapping 정보를 생성할 프로그램 지정경로
launcherPath = '.\\test_in.exe'

#EtherCAT에 연결된 port 정보를 읽어와 저장할 변수
ethercatPortName = ""

#실행할 명령어 인자
command = [
    'powershell',
    'Start-Process',
    '',
    ''
]

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

#명령어 생성 함수
def setCommand() :
    global command

    print("command create")

    command[2] = launcherPath
    command[3] = f'"{ethercatPortName}", "-sdo"'

    return 0

#파일 실행 함수
def runFile() :
    print("runnig")

    try:
        process = subprocess.run(command, cwd=folderPath)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)

    return 0

#txt 파일에서 적힌 문구 읽어오는 함수
def readTxt() :
    global ethercatPortName

    print("reading")

    textFile = open(filePath, 'r')

    ethercatPortName = textFile.readline().strip()

    if not ethercatPortName :
        return 1
    textFile.close()
    return 0

#메인 실행 함수
def main() :
    setFolderPath()

    if readTxt() == 1 :
        print("Failed")
        return 0
    
    setCommand()

    runFile()


main()