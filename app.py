from flask import Flask, render_template, request, send_from_directory
import os
import tools

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'

# 确保上传和下载文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        input_file = filename
        output_file = os.path.join(app.config['DOWNLOAD_FOLDER'], 'translated_' + file.filename)

        translated_filename = tools.translate_excel(input_file, output_file)
        if translated_filename:
            print(f"Translated filename: {translated_filename}")  # 调试信息
            return render_template('translate.html', filename=translated_filename)
        else:
            return "Error translating the file"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
