import win32com.client

# 한글 자동화 객체 생성
hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")

# 한글 창을 화면에 표시
hwp.XHwpWindows.Item(0).Visible = True

print("한글 실행 성공")

# 확인할 때까지 프로그램 유지
input("한글 창을 확인한 뒤 Enter를 누르세요: ")

# 테스트로 실행한 한글 종료
hwp.Quit()