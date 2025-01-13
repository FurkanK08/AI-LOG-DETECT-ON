from flask import Flask, request, render_template, send_from_directory, url_for, redirect
import os
import subprocess
import re
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PREDICTION_FOLDER = 'predictions'

ALLOWED_EXTENSIONS = {'log'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICTION_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREDICTION_FOLDER'] = PREDICTION_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    download_link = None  
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            log_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(log_file_path)
            
            try:
                
                output_file = subprocess.check_output(['python', 'model_predict.py', log_file_path])
                output_file_path = output_file.decode('utf-8').strip()
                output_file_path = re.sub(r'\x1b\[.*?m', '', output_file_path)  
                
                
                base_dir = os.path.dirname(os.path.abspath(__file__))  
                prediction_path = os.path.join(base_dir, 'predictions', os.path.basename(output_file_path))
                
                
                if os.path.exists(prediction_path):
                    
                    download_link = url_for('download_file', filename=os.path.basename(prediction_path))
                else:
                    return f"Error: Output file not found at {prediction_path}"
            
            except subprocess.CalledProcessError as e:
                return f"Error during prediction: {str(e)}"
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        else:
            return 'Geçerli bir log dosyası yüklemeniz gerekmektedir.'
    
    return render_template('index.html', download_link=download_link)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PREDICTION_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
