#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUFFER_SIZE 1024 * 1024  // 파일을 한 번에 읽을 버퍼 크기 임의 지정.

// 파일에서 전체 내용을 읽어와서 줄 단위로 나누는 함수
int readFromFile(const char *fileName, char ***input, int *lineCount) {
    FILE *file = fopen(fileName, "r");
    if (file == NULL) {
        perror("Failed to open file");
        return 1;  // 파일 열기 실패
    }

    // 파일의 전체 내용을 읽기 위한 버퍼 할당
    char buffer[MAX_BUFFER_SIZE];
    size_t bytesRead = fread(buffer, 1, sizeof(buffer) - 1, file);
    if (bytesRead == 0) {
        perror("Failed to read file");
        fclose(file);
        return 1;  // 파일 읽기 실패
    }
    buffer[bytesRead] = '\0';  // 문자열 끝에 널 종료 문자 추가

    fclose(file);  // 파일 닫기

    // 전체 내용을 줄 단위로 나누기
    *lineCount = 0;
    for (size_t i = 0; i < bytesRead; i++) {
        if (buffer[i] == '\n') {
            (*lineCount)++;
        }
    }

    // 줄 수에 맞게 메모리 할당
    *input = (char **)malloc(sizeof(char *) * (*lineCount));
    if (*input == NULL) {
        perror("Failed to allocate memory");
        return 1;  // 메모리 할당 실패
    }

    // 문자열을 줄 단위로 나누어 배열에 저장
    char *line = strtok(buffer, "\n");
    int index = 0;
    while (line != NULL) {
        (*input)[index] = (char *)malloc(strlen(line) + 1);  // 각 줄에 메모리 할당
        if ((*input)[index] == NULL) {
            perror("Failed to allocate memory for line");
            return 1;  // 메모리 할당 실패
        }
        strcpy((*input)[index], line);  // 줄 복사
        line = strtok(NULL, "\n");  // 다음 줄로 이동
        index++;
    }

    return 0;  // 성공
}

// 메모리 해제 함수
void freeInput(char **input, int lineCount) {
    for (int i = 0; i < lineCount; i++) {
        free(input[i]);  // 각 줄에 할당된 메모리 해제
    }
    free(input);  // 전체 배열에 할당된 메모리 해제
}

// 문자열 찾는 함수.
int parsing(char **input, int lineCount, char *this) {
    int i;
    for (i = 0; i < lineCount; i++) {
        if (strstr(input[i], "TwinCAT") != NULL) {  // "TwinCAT"이 포함된 문장 찾기
            char *wpcap_pos = strstr(input[i], "wpcap:");  // "wpcap:" 찾기
            if (wpcap_pos != NULL) {
                wpcap_pos += strlen("wpcap: ");  // "wpcap:" 부분을 넘기기
                // wpcap 뒤의 문자열을 this에 복사
                strncpy(this, wpcap_pos, 99);  // 100자까지 복사
                this[99] = '\0';  // 널 종료 처리
                printf("Found wpcap string: %s\n", this);
                return 0;  // 찾았으면 종료
            }
        }
    }

    printf("TwinCAT not found or no wpcap found\n");
    return 1; 
}

void inputQ() {
    char input;
    while(1) {
        printf("input q : ");
        scanf("%c", &input);
        if (input == 'q') {
            break;
        }
   }
}

//선택형으로 할 경우 받아 올 수 있도록 설계계
int writeFile(char** input, size_t chooseNum, char *this) {
    FILE *outFile = fopen("userChoose.txt", "w");
    if(outFile == NULL) {
        perror("Failed\n");

        return 1;
    }

    if (this == NULL) {
        fprintf(outFile, "%s", input[chooseNum]);
    }

    else {
        fprintf(outFile, "%s", this);
    }    

    fclose(outFile);

    printf("saved\n");

    return 0;
}

//실행 시 인자를 넣고 실행을 시켰을 땐 원하는거로 선택을 하여 진행이 가능하도록 설계함.
int main(int argc, char *argv[]) {
    char **input = NULL;
    int lineCount = 0;
    char this[100];  // wpcap 뒤 문자열을 저장할 배열
    size_t chooseNum = 0;

    if (readFromFile("socketINFO.txt", &input, &lineCount) != 0) {
        return 1;  // 읽기 실패 시 종료
    }
////////// debug용 ///////////
    // argc = 2;
    // argv[1] = 0;
/////////////////////////////
    if(argc == 2) {
        chooseNum = (size_t)atoi(argv[1]);
        int isDone = writeFile(input, chooseNum, this);

        freeInput(input, lineCount);

        if (isDone == 1) {
            return 1;
        }

        return 0;
    }
////// debug 용 /////////////
    // 현재 작업 디렉토리 출력
    // char cwd[1024];
    // if (getcwd(cwd, sizeof(cwd)) != NULL) {
    //     printf("Current working directory: %s\n", cwd);
    // } else {
    //     perror("getcwd() error");
    // }
////////////////////////////
    // "socketINFO.txt" 파일에서 데이터 읽기

    // 파싱 함수 호출하여 wpcap: 뒤의 문자열을 찾기
    if (parsing(input, lineCount, this) == 0) {
        writeFile(input, 0, this);
    }

    // 읽은 메모리 해제
    freeInput(input, lineCount);

/////// debug용 ///////
    //inputQ();
//////////////////////

    return 0;
}