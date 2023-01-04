import csv
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("movie.ui")[0]

#콤보박스 comboBox_title 에 들어갈 것
action_list = ['아바타']
drama_list = ['영웅','러브레터']
crime_list = ['젠틀맨']
thriller_list = ['올빼미']
movie_list = ['아바타','영웅','러브레터','젠틀맨','올빼미']

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # ui 시작 인덱스 0으로 고정
        self.stackedWidget.setCurrentIndex(0)

        ### 메인 페이지
        self.btn_mainticketing.clicked.connect(self.to_tab_movie) # '영화예매' 버튼
        self.btn_ticketlookup.clicked.connect(self.to_tab_lookup)# '영화예매조회'  버튼

        ### 영화 예매 페이지
        self.btn_search.clicked.connect(self.showMoviesearch)    # '검색' 버튼
        # 콤보박스
        self.comboBox_genre.addItem('검색')
        self.comboBox_genre.addItem('액션')
        self.comboBox_genre.addItem('드라마')
        self.comboBox_genre.addItem('범죄')
        self.comboBox_genre.addItem('스릴러')
        # 선택되면 두번째 콤보박스의 내용이 바뀜
        self.comboBox_genre.activated[str].connect(lambda: self.selectedComboItem(self.comboBox_genre))
        self.btn_ticketing.clicked.connect(self.ticketing) # '예매하기' 버튼

        ### 예매하기 페이지
        self.lineEdit_name2.textChanged.connect(self.reserve_check) # 예매 정보 입력 이름 입력란이 바뀔때마다 실행 할 함수
        self.lineEdit_phone2.textChanged.connect(self.reserve_check)  # 예매 정보 입력 휴대폰번호 입력란이 바뀔때마다 실행 할 함수
        self.pushButton_done2.clicked.connect(self.movieSelect) # 정보 입력 후 '확인' 버튼

        ### 예매조회 페이지
        self.pushButton_done1.clicked.connect(self.lookup)      ## 이름, 휴대폰번호 입력하고 '확인' 버튼 누를 때마다.


    ### 콤보박스 관련 함수
    def selectedComboItem(self, text):
        print(text.currentText())
        self.comboBox_title.addItem('영화 전체 검색')
        if text.currentText() == '액션':
            print("1")
            self.comboBox_title.clear()
            self.comboBox_title.addItems(action_list)
        if text.currentText() == '드라마':
            print("1")
            self.comboBox_title.clear()
            self.comboBox_title.addItems(drama_list)
        if text.currentText() == '범죄':
            print("1")
            self.comboBox_title.clear()
            self.comboBox_title.addItems(crime_list)
        if text.currentText() == '스릴러':
            print("1")
            self.comboBox_title.clear()
            self.comboBox_title.addItems(thriller_list)
        if text.currentText() == '검색':
            print("1")
            self.comboBox_title.clear()
            self.comboBox_title.addItem('영화 전체 검색')




    ### 메인 페이지
    def to_tab_movie(self):     # '영화예매' 버튼
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
    def to_tab_lookup(self):    # '영화예매조회'  버튼
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)

    ### 영화예매 페이지
    def showMoviesearch(self):  # '검색' 버튼
        self.moviesearch(0, 0)
        self.moviesearch(1, 0)
        self.moviesearch(2, 0)
        self.moviesearch(2, 1)
        self.moviesearch(3, 0)
        self.moviesearch(4, 0)
    def moviesearch(self, genreIndex, titleIndex):   # '검색' 버튼에 적용할 함수
        f = open('movie.csv', 'r', encoding='utf-8')  # csv 파일 오픈
        file = csv.reader(f)
        # print(file)                 ## <_csv.reader object at 0x00000257BE33D760>
        datali = list(file)
        print(f'검색\n{datali}')               ## [['액션', '아바타 ...]]
        row = len(datali)  # 15
        col = len(datali[0])  # 7
        self.tableWidget_search.setRowCount(row)  # 현재 Table Widget_search의 행의 개수를 row개로 설정합니다.
        self.tableWidget_search.setColumnCount(col)  # 현재 Table Widget_search의 열의 개수를 col개로 설정합니다.
        self.movieli1 = []          # 이차원 리스트 만듦
        for i in range(row):
            self.movieli2 = []      # 이차원 리스트 만듦
            for j in range(col):
                # 콤보박스 장르 선택 & 콤보박스 제목 선택 한게 일치할 때,
                if self.comboBox_genre.currentIndex() == genreIndex and self.comboBox_title.currentIndex() == titleIndex:
                    if genreIndex == 0 :        #  장르콤보박스 인덱스가 '검색'일 때 영화 전체 검색.
                        self.tableWidget_search.setItem(i, j, QTableWidgetItem(datali[i][j]))  # csv 리스트 전체를
                    if self.comboBox_title.currentText() == datali[i][1]: # 제목콤보박스 인덱스가 csv리스트 제목과 일치할 때
                        self.tableWidget_search.clearContents()           # 전체 검색한 걸 지우기 위해서, 행/열 헤더를 제외한 항목 삭제
                        self.movieli2.append(datali[i][j])                # 리스트안 리스트에 <제목과 일치하는 요소들> 추가
            self.movieli1.append(self.movieli2)
            self.movieli1 = list(filter(None,self.movieli1))
        for i in range(len(self.movieli1)):
            for j in range(len(self.movieli1[i])):
                self.tableWidget_search.setItem(i, j, QTableWidgetItem(self.movieli1[i][j]))
        f.close()

    def ticketing(self):        # '예매하기'버튼
        self.stackedWidget.setCurrentIndex(2)   # 스택인덱스 2(예매 정보 입력 페이지)로 넘어감
        print('예매하기')



    ### 예매하기 페이지
    def reserve_check(self) : # 예약자 정보 입력란 유효성 검사
        self.reserveName = self.lineEdit_name2.text()
        self.reserveTel = self.lineEdit_phone2.text()
        if self.reserveName != '' and self.reserveTel != '':  # 이름, 전화번호 모두 공백이 아닐 때 확인 버튼 활성화
            self.pushButton_done2.setEnabled(True)

    def movieSelect(self):      # 예매-정보입력-'확인'버튼
        self.select = self.tableWidget_search.selectedItems()  # 테이블에 선택한 항목들을 리스트 형식으로 반환.->self.select는 리스트
        self.strli = []                      # self.select 안에 있는 요소를 문자로 가져와서 반복문으로 넣어줄 리스트 self.strli 선언
        for i in self.select:
            self.strli.append(str(i.text()))  # self.select의 i번째를 문자로 가져오고, str형으로 반환해서 바꿀때마다 self.strli에 넣어줌
        reply = QMessageBox.question(self, '영화예매', f'{self.strli[1]}, {self.strli[2]}, {self.reserveName}, {self.reserveTel}\n예매하시겠습니까?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:  ## 큐 메시지박스에서 yes 버튼 눌렀을 때 csv파일에 넣기
            f = open('ticketing.csv', 'a', encoding='utf-8-sig', newline='')  # csv 파일 오픈
            file = csv.writer(f)
            file.writerow([self.strli[1],self.strli[2],self.reserveName,self.reserveTel])
            f.close()
            QMessageBox.information(self,'영화예매', '예매 성공')
            self.stackedWidget.setCurrentIndex(0)
            self.lineEdit_name2.clear()
            self.lineEdit_phone2.clear()
        else:
            print('예매취소')
            self.stackedWidget.setCurrentIndex(0)
            self.lineEdit_name2.clear()
            self.lineEdit_phone2.clear()

    ### 예매 조회 페이지
    def lookup(self):
        print('조회')
        f = open('ticketing.csv', 'r', encoding='utf-8')  # csv 파일 오픈
        file = csv.reader(f)
        datali = list(file)
        print(datali)               ## [['액션', '아바타 ...]]
        for i in datali :
            for j in datali[0] :
                if str(i[j]) == self.lineEdit_name1.text() and str(i[j]) == self.lineEdit_phone1.text() :
                    print(datali[2],datali[3])





if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()