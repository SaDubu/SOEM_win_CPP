etherCAT_ soem을 window cpp 환경에서 사용할 수 있도록 구성했습니다.

Run_file에는 TwinCAT의 드라이버를 설치 시 port name을 인식하여 연결된 etherCAT 장비의 sdo, pdo map을 가져옵니다.

일부 장치에서는 동작하지 않을 수 있습니다.

test_in : SOEM의 예제 코드 중 하나인 SlaveInfo를 개조하여 화면으로 출력되는 모든 문장을 txt 파일로 저장하도록 만들었다. -- socketParsher : 현재 기기의 port 드라이버의 이름들 중 EtherCAT이 물려 있을 것으로 추정되는 BackHOFF 드라이버를 저장해둔다. -- readSdo, readMapping : 각각 sdo와 pdo의 map 정보를 txt 파일로 출력한다. (test_in에 파라미터를 넣어 실행시키는 방식) -- txt2Csv : 바로 위에서 생성된 txt 파일을 읽어와 지정된 방식으로 데이터 파싱을 통해 csv파일화 시킨다. -- GetEtherCATINFOS : 위에 있는 것들을 정해진 순서에 맞게 실행시켜 해당 프로그램만 실행 시키면 csv까지 만들어진다.