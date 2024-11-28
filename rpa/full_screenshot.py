def capture_full_page(driver, save_path):
    """
    Capture the full page screenshot using Chrome DevTools Protocol (CDP).
    """
    original_size = driver.get_window_size()
    required_width = driver.execute_script("return document.body.scrollWidth")
    required_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(required_width, required_height)
    driver.save_screenshot(save_path)
    driver.set_window_size(original_size['width'], original_size['height'])
