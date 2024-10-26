import tempfile
import logging
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from sketch_model import convert_to_sketch
import os

# Initialize Flask application
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Allowed extensions for uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if 'file' not in request.files:
                logging.error("No file part")
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '' or not allowed_file(file.filename):
                logging.error("No selected file or unsupported file type")
                return redirect(request.url)

            # Use /tmp for the uploaded image
            input_path = f"/tmp/{secure_filename(file.filename)}"
            file.save(input_path)
            logging.debug(f"Uploaded image saved at: {input_path}")

            # Create a temporary file for the output sketch
            output_path = f"/tmp/sketch_{os.path.basename(input_path)}"
            convert_to_sketch(input_path, output_path)
            logging.debug(f"Sketch image saved at: {output_path}")

            # Serve the uploaded image and the sketch directly using url_for
            return render_template("index.html", 
                                   uploaded_image=url_for('serve_temp_file', filename=os.path.basename(input_path)),  
                                   sketch_image=url_for('serve_temp_file', filename=os.path.basename(output_path)))

        except Exception as e:
            logging.error(f"Error processing file: {e}")
            return "Internal Server Error", 500

    return render_template("index.html", uploaded_image=None, sketch_image=None)

@app.route("/temp/<filename>")
def serve_temp_file(filename):
    try:
        # Serve the temporary files created in the temporary directory
        return send_file(f'/tmp/{filename}', as_attachment=False)
    except Exception as e:
        logging.error(f"Error serving temporary file: {e}")
        return "File Not Found", 404

if __name__ == "__main__":
    app.run(debug=True)
