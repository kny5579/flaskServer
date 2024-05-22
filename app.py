from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import zipfile
import glob
import os
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return 'This is Home!'


@app.route('/upload', methods=['POST'])
def multi_upload_file():
    #파일 받기
    student_files=request.files.getlist("student_files")
    answer_files=request.files.getlist("answer_files")

    # 업로드 디렉토리 비우기
    files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    # 학생 파일 저장
    for file in student_files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, 'student_' + filename))

    # 정답 파일 저장
    for file in answer_files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, 'answer_' + filename))
    
    # 파일 처리- 채점 코드 추가+엑셀 파일, 채점된 이미지 저장 코드 추가해야 함
    processed_files= [] #채점된 이미지 리스트 여기에 저장 예정
    
    # ZIP 파일 생성
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for processed_file in processed_files:
            zip_file.write(processed_file, os.path.basename(processed_file))
    
    zip_buffer.seek(0)
        

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='processed_files.zip'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
