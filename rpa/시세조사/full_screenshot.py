import io
from PIL import Image

def capture_full_page(driver, save_path):
   # # PNG 형식으로 스크린샷 찍기 (메모리에 저장)
    screenshot_png = driver.get_screenshot_as_png()
    # PNG → JPG 변환 후 저장    
    # with 문을 사용하여 이미지 객체 자동 관리
    with Image.open(io.BytesIO(screenshot_png)) as image:
        # RGB로 변환 (JPEG로 저장을 위해 필요)
        image = image.convert("RGB")   # JPG 변환

        # JPG 형식으로 저장
        image.save(save_path, "JPEG", quality=95)  # JPG 형식, 품질 95로 저장