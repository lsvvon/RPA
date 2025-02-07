from selenium.webdriver.chrome.options import Options
import common_module
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import re

#sentences = ("그건 아닌데 어떤 이상한 놈 때문에 기분 다 잡쳤어", 
#"아닌데 어떤 이상한 놈 때문에 기분 다 잡쳤어")

sentences = ("노블레르", "등촌노블레르")

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
print("코사인 유사도 측정")
print(cos_similar[0][0])

answer_string = "노블레르"
input_string = "등촌노블레르"

intersection_cardinality = len(set.intersection(*[set(answer_string), set(input_string)]))
union_cardinality = len(set.union(*[set(answer_string), set(input_string)]))
similar = intersection_cardinality / float(union_cardinality)

print(similar)


answer_string = "노블레르2차"
input_string = "등촌노블레르"

answer_bytes = bytes(answer_string, 'utf-8')
input_bytes = bytes(input_string, 'utf-8')
answer_bytes_list = list(answer_bytes)
input_bytes_list = list(input_bytes)

sm = difflib.SequenceMatcher(None, answer_bytes_list, input_bytes_list)
similar = sm.ratio()

print(similar)


# Compile a regular expression pattern
pattern = re.compile(r"노블레르") 
# Use the compiled pattern to search for matches
text1 = "등촌노블레르"
matches1 = pattern.findall(text1)
print(matches1)  # Output: ['ai', 'ai', 'ai'] text2 = "I have a pet cat."matches2 = pattern.findall(text2)print(matches2)  # Output: ['a']

text = '111234'
com = re.compile(r'\d\w\S...').search(text).group()
print(com)  # 111234


# 드라이버 초기화
# chrome_options = Options()
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")

# driver = common_module.initialize_driver()
# url = "https://bizssl.shinhanci.co.kr/SHSCHER/Asp/RPA/CA_RPA_Condition.asp"
# driver.get(url)
# #print("RPA_main.driver: ", driver)
# time.sleep(5)


# # 파일 업로드 요소 찾기
# file_input = driver.find_element(By.ID, "txtFile")  # ID를 사용해 찾기
# time.sleep(3)

# file_name = "5000000000_901.png"  # 업로드하려는 파일 이름
# folder_path = r"C:\python\RPA\rpa\capImg"  # capImg 폴더의 절대 경로
# file_path = os.path.join(folder_path, file_name)

# # 파일이 실제로 존재하는지 확인
# if os.path.exists(file_path):
#     print(f"File exists at: {file_path}")
# else:
#     print("File does not exist. Check the path.")

# file_input.send_keys(file_path)

# uploaded_image = driver.find_element(By.ID, "uploadedImagePreview")
# uploaded_image_src = uploaded_image.get_attribute("src")
# print(f"Uploaded image URL: {uploaded_image_src}")

# if "expected_image_name" in uploaded_image_src:
#     print("Correct image uploaded.")
# else:
#     print("Incorrect image uploaded.")

time.sleep(3)

# 필요한 경우 제출 버튼 클릭
# submit_button = driver.find_element(By.ID, "submitButton")
# submit_button.click()

# 브라우저 종료


