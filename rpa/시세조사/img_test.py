# import pyautogui as p

# dest = "C:/python/RPA/rpa/capImg"

# p.screenshot()  #전체 화면 스크린샷 찍고 이미지 객체로 전달
# p.screenshot(dest +"all.jpg") #전체 화면 스크린샷 찍고 파일로 저장
# p.screenshot(region=(0, 0, 100, 100)) #지정영역 스크린샷 찍고 이미지 객체로 전달
# p.screenshot(dest +"part.jpg", region=(0, 0, 100, 100)) #지정영역 스크린샷 찍고 파

from PIL import ImageGrab 

# full screen
img_full = ImageGrab.grab()

# crob screen
img_crop = ImageGrab.grab([0,0,800,600])

# img show
img_full.save('C:/python/RPA/rpa/capImg/captured.png')
