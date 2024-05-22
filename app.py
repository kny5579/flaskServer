from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import glob
from datetime import datetime

app = Flask(__name__)

# 파일 업로드 폴더 설정
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 파일 확장자 설정
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return 'This is Home!'


@app.route('/upload', methods=['POST'])
def multi_upload_file():
    # 파일 받기
    student_files = request.files.getlist("student_files")
    answer_files = request.files.getlist("answer_files")
    date = request.form.get("exam_date")

    # exam_date 검증
    try:
        exam_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # 업로드 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # 업로드 디렉토리 비우기
    files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    # 받은 파일 저장
    saved_files = []
    for files in (student_files, answer_files):
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                saved_files.append((filename, file_path))

    # 처리된 파일들 보관할 딕셔너리
    response = {
        'excel_files': [],
        'image_files': []
    }

    # 파일을 읽고 응답에 추가
    for filename, file_path in saved_files:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            if filename.endswith('.xlsx'):
                response['excel_files'].append({
                    'filename': filename,
                    'data': file_data.decode('latin1')  # 바이너리 데이터를 JSON으로 전송할 수 있도록 문자열로 인코딩
                })
            else:
                response['image_files'].append({
                    'filename': filename,
                    'data': file_data.decode('latin1')
                })

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
