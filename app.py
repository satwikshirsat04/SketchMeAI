import tempfile
import logging
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from sketch_model import convert_to_sketch
import os

# Initialize Flask application
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if 'file' not in request.files:
                logging.error("No file part")
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                logging.error("No selected file")
                return redirect(request.url)
            
            # Use a temporary file for the uploaded image
            with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
                input_path = temp_input_file.name
                file.save(input_path)

                # Create a temporary file for the output sketch
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_output_file:
                    output_path = temp_output_file.name

                    # Convert image to sketch
                    convert_to_sketch(input_path, output_path)

            # Serve the uploaded image and the sketch directly
            return render_template("index.html", 
                                   uploaded_image=input_path,  # Direct file path for uploaded image
                                   sketch_image=output_path)    # Direct file path for sketch image

        except Exception as e:
            logging.error(f"Error processing file: {e}")
            return "Internal Server Error", 500

    return render_template("index.html", uploaded_image=None, sketch_image=None)

@app.route("/download/<path:filename>")
def download_file(filename):
    try:
        # Construct the full path for the file to download
        path = os.path.join("/tmp", filename)
        return send_file(path, as_attachment=True)
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True)
