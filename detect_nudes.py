import cv2
import requests

url = 'https://api.deepai.org/api/nsfw-detector'

headers = {
    'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'
}

with open('test_img_nudes.png', 'rb') as file:
    img_for_resp = file.read()

response = requests.post(
    url,
    files={
        'image': img_for_resp
    },
    headers=headers
).json()

# print(response)

detections = response['output']['detections']
img = cv2.imread('test_img_nudes.png')
for item in detections:
    if float(item['confidence']) >= 0.5:
        x, y, w, h = map(int, item['bounding_box'])
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
cv2.imwrite('img_after_rec.png', img)
