from PIL import Image, ImageFilter
import pytesseract
import os
import json

# Tesseract 경로 설정 (설치 위치에 따라 다를 수 있음)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# 이미지 파일 불러오기
image_path = "C:\\Users\\kimms\\OneDrive\\바탕 화면\\vinci2.jpg"
img = Image.open(image_path)

# 이미지 전처리
img = img.convert('L')  # 이미지를 흑백으로 변환
img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 이진화
img = img.filter(ImageFilter.SHARPEN)  # 이미지 선명화

# 확대 비율
scale_factor = 1.3 # 원하는 배율 

# 새로운 크기 계산
new_width = int(img.width * scale_factor)
new_height = int(img.height * scale_factor)
img = img.resize((new_width, new_height), Image.LANCZOS)  # 이미지 확대

# 이탈리아어로 OCR 수행
custom_config = r'--oem 3 --psm 6 -l ita'  # l은 이탈리아어 설정
boxes = pytesseract.image_to_boxes(img, config=custom_config)  # 각 글자의 경계 박스 정보 추출

# 결과를 저장할 폴더 및 JSON 파일 생성
output_dir = 'output_chars'
os.makedirs(output_dir, exist_ok=True)
json_data = []

# 글자 영역을 바탕으로 자르기
width, height = img.size

for i, box in enumerate(boxes.splitlines()):
    # box의 형식: 문자 x1 y1 x2 y2 페이지
    char, x1, y1, x2, y2, _ = box.split()
    
    # 좌표 변환 (Pillow는 이미지 좌측 상단이 (0,0) 기준이지만, Tesseract는 좌측 하단이 기준)
    x1, y1, x2, y2 = int(x1), height - int(y2), int(x2), height - int(y1)
    
    # 글자 이미지 자르기
    char_img = img.crop((x1, y1, x2, y2))
    
    # 일반 파일명으로 저장
    filename = f'char_{i}.png'
    char_img.save(os.path.join(output_dir, filename))
    
    # JSON 데이터에 파일명과 해당 글자 추가
    json_data.append({"file": filename, "char": char})

# JSON 파일로 저장
json_path = os.path.join(output_dir, 'characters.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("각 글자를 이미지로 저장하고, OCR 데이터를 JSON 파일에 기록했습니다.")


