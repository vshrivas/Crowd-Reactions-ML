# Takes a URL for an image. Prints the emotions of the people in the image

subscription_key = "51fae3a010d1498d95a008972adb3547"
assert subscription_key

face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"

image_url = "https://how-old.net/Images/faces2/main007.jpg"

import requests
from IPython.display import HTML

headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

params = {
    'returnFaceAttributes': 'emotion',
}

response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()

for face in faces:
    print(face['faceAttributes']['emotion'])