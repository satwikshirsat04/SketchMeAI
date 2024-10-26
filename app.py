from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from sketch_model import convert_to_sketch
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Convert image to sketch
        output_filename = f"sketch_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        convert_to_sketch(input_path, output_path)

        return render_template("index.html", uploaded_image=url_for('static', filename=f"uploads/{filename}"), sketch_image=url_for('static', filename=f"uploads/{output_filename}"))

    return render_template("index.html", uploaded_image=None, sketch_image=None)

@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
