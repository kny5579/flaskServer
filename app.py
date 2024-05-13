from flask import Flask, request

import glob
import os

app = Flask(__name__)


@app.route('/')
def home():
    return 'This is Home!'


@app.route('/upload', methods=['POST'])
def multi_upload_file():
    # 이미지 받기
    upload = request.files.getlist("file")

    # 사진이 저장되는 디렉토리(이후 변경)
    image_path = glob.glob('C:/Users/캡스톤/Images/*.jpg')

    # 기존의 사진 삭제
    for f in image_path:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    # 받은 사진 저장
    for f in upload:
        f.save('./uploads/' + f.filename)

    # 저장 이미지 리스트에 담기
    images = []
    for path in image_path:
        with open(path, 'rb') as f:
            images.append(f.read())

    # 리스트 전달 후 결과값 받음(pyfunc에 이미지처리 클래스명 입력)
    result = pyfunc(images)

    return result


if __name__ == '__main__':
    app.run(debug=True)
