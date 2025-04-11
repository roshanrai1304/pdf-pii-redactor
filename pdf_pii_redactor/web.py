"""
Web interface for the PDF PII Redactor tool.
"""

import os
import sys
import tempfile
import uuid
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_pii_redactor.redactor import PDFRedactor
from pdf_pii_redactor.utils import validate_pdf



from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))


# Configure upload folder
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "pdf_pii_redactor")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configure allowed extensions
ALLOWED_EXTENSIONS = {"pdf"}

# Configure OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    """Handle the index page and file upload."""
    if request.method == "POST":
        # Check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Generate a unique filename
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{unique_id}_{filename}")
            output_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{unique_id}_redacted_{filename}")
            
            # Save the uploaded file
            file.save(input_path)
            
            # Validate the PDF
            if not validate_pdf(input_path):
                os.unlink(input_path)
                flash("Invalid PDF file")
                return redirect(request.url)
            
            # Get model from form
            model = request.form.get("model", "gpt-4o")
            
            # Process the PDF
            try:
                redactor = PDFRedactor(openai_api_key=OPENAI_API_KEY, model=model)
                stats = redactor.redact_pdf(input_path, output_path)
                
                # Clean up the input file
                os.unlink(input_path)
                
                # Redirect to download page
                return redirect(url_for("download", filename=f"{unique_id}_redacted_{filename}", 
                                        redacted_items=stats["redacted_items"]))
                
            except Exception as e:
                # Clean up files in case of error
                if os.path.exists(input_path):
                    os.unlink(input_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)
                
                flash(f"Error processing PDF: {str(e)}")
                return redirect(request.url)
        else:
            flash("File type not allowed. Please upload a PDF file.")
            return redirect(request.url)
    
    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    """Show download page for the redacted file."""
    return render_template("download.html", filename=filename)


@app.route("/preview_file/<filename>")
def preview_file(filename):
    """Serve the redacted file for preview in the browser."""
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        flash("File not found")
        return redirect(url_for("index"))
    
    # Serve the file for inline display (not as attachment)
    return send_file(file_path, mimetype='application/pdf')


@app.route("/get_file/<filename>")
def get_file(filename):
    """Serve the redacted file."""
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        flash("File not found")
        return redirect(url_for("index"))
    
    # Serve the file
    response = send_file(file_path, as_attachment=True, download_name=filename.split("_", 2)[2])
    
    # Store the file path in the response headers for cleanup
    response.headers.add('X-File-To-Remove', file_path)
    
    return response


@app.after_request
def cleanup_files(response):
    """Remove temporary files after response is sent."""
    file_to_remove = response.headers.get('X-File-To-Remove')
    if file_to_remove:
        # Remove the custom header before sending response
        response.headers.remove('X-File-To-Remove')
        
        # Schedule file for deletion
        @response.call_on_close
        def remove_file():
            try:
                if os.path.exists(file_to_remove):
                    os.unlink(file_to_remove)
                    app.logger.info(f"Removed file: {file_to_remove}")
            except Exception as e:
                app.logger.error(f"Error removing file: {str(e)}")
    
    return response


def run_web_app(host="0.0.0.0", port=5000, debug=False):
    """Run the web application."""
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_web_app(debug=True) 