# ✅ app.py
from flask import Flask, render_template, request
import os
import shutil
from werkzeug.utils import secure_filename
from utils import process_image
from glob import glob

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["RESULT_FOLDER"] = "static/results"
TEMP_FOLDER = "static/temp"

# Pastikan semua folder sudah tersedia
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULT_FOLDER"], exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    dataset_groups = {
        'Darwin': 'dataset/Darwin/img/',
        'Montgomery': 'dataset/Montgomery/img/',
        'Shenzhen': 'dataset/Shenzhen/img/'
    }

    grouped_results = {}

    for name, folder in dataset_groups.items():
        if not os.path.exists(folder):
            continue

        image_paths = glob(os.path.join(folder, '*.jpg')) + glob(os.path.join(folder, '*.png'))
        selected = image_paths[:3]

        results = []
        for path in selected:
            filename = os.path.basename(path)
            temp_path = os.path.join(TEMP_FOLDER, f"{name}_{filename}")
            shutil.copy(path, temp_path)

            processed = process_image(temp_path, app.config["RESULT_FOLDER"], filename)

            results.append({
                'filename': filename,
                'original': temp_path.replace('\\', '/'),
                'gray': processed['gray'].replace('\\', '/'),
                'clahe': processed['clahe'].replace('\\', '/'),
                'edge': processed['edge'].replace('\\', '/'),
                'edge_count': processed['edge_count'],
                'histogram': processed['histogram'].replace('\\', '/')
            })

        grouped_results[name] = results

    return render_template('home.html', grouped_results=grouped_results)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('images')
        results = []

        for file in files:
            if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename = secure_filename(file.filename)
                input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(input_path)

                processed = process_image(input_path, app.config['RESULT_FOLDER'], filename)

                results.append({
                    'filename': filename,
                    'original': input_path.replace('\\', '/'),
                    'gray': processed['gray'],
                    'clahe': processed['clahe'],
                    'edge': processed['edge'],
                    'edge_count': processed['edge_count'],
                    'histogram': processed['histogram']
                })
            else:
                return "<h3>❌ Salah satu file tidak valid. Gunakan JPG, PNG, atau JPEG saja.</h3>"

        return render_template('result_multiple.html', results=results)

    return render_template('upload.html')

@app.context_processor
def inject_theme():
    return dict(app_name="Klinik X-ray", theme_color="#2563eb") 

# ✅ Run dengan cara aman
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
