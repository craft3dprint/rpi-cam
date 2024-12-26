import os
import zipfile
import shutil
import tempfile
from flask import Flask, render_template, send_from_directory, redirect, url_for, send_file

app = Flask(__name__)

# Set the directory where your images are stored
IMAGE_FOLDER = '/home/cam/3d-printer-pic'

# Ensure the folder exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)


@app.route('/')
def index():
    # Display root directory contents
    return list_directory("")


@app.route('/folder/<path:foldername>')
@app.route('/folder/', defaults={'foldername': ''})
def list_directory(foldername):
    # List the contents of a folder
    folder_path = os.path.join(IMAGE_FOLDER, foldername)
    items = []

    # Add a "Go Back" option unless in the root directory
    if foldername:
        parent_folder = os.path.dirname(foldername)
        items.append({'type': 'back', 'name': parent_folder})

    # Add folders and files
    for entry in os.scandir(folder_path):
        if entry.is_dir():
            items.append({'type': 'folder', 'name': os.path.join(foldername, entry.name)})
        elif entry.is_file() and entry.name.endswith('.jpg'):
            items.append({'type': 'file', 'name': os.path.join(foldername, entry.name)})

    # Sort folders and files in descending order
    items = sorted(items, key=lambda x: x['name'].lower(), reverse=True)

    return render_template('index.html', items=items)


@app.route('/download/folder/<path:foldername>', methods=['GET', 'POST'])
def download_folder(foldername):
    # Path to the folder
    folder_path = os.path.join(IMAGE_FOLDER, foldername)

    # Create a temporary directory for the ZIP file
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_filename = f"{foldername.replace('/', '_')}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        # Create the ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

        # Send the ZIP file for download
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)


@app.route('/delete/<path:filename>', methods=['GET'])
def delete(filename):
    file_path = os.path.join(IMAGE_FOLDER, filename)

    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Deletes non-empty folders
        else:
            os.remove(file_path)
        return redirect(url_for('list_directory', foldername=os.path.dirname(filename)))
    else:
        return f"File or folder {filename} not found!", 404


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(IMAGE_FOLDER, filename)

    if os.path.exists(file_path):
        return send_from_directory(IMAGE_FOLDER, filename, as_attachment=True)
    else:
        return f"File {filename} not found!", 404


@app.route('/image/<path:filename>', methods=['GET'])
def image(filename):
    file_path = os.path.join(IMAGE_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(IMAGE_FOLDER, filename)
    else:
        return f"Image {filename} not found!", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
