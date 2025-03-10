import io
from PIL import Image

def capture_full_page(driver, save_path):
   # # PNG 형식으로 스크린샷 찍기 (메모리에 저장)
    screenshot_png = driver.get_screenshot_as_png()
    # PNG → JPG 변환 후 저장
    image = Image.open(io.BytesIO(screenshot_png))
    image = image.convert("RGB")  # JPG 변환
    image.save(save_path, "JPEG", quality=95)  # JPG 저장