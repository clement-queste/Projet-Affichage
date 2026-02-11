import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Update this to point to the actual folder structure: static/img
# Using os.path.join makes it work on both Windows and Linux
IMAGE_FOLDER = os.path.join('static', 'img')

@app.route('/')
def index():
    # We check if the folder exists first to avoid another crash
    if not os.path.exists(IMAGE_FOLDER):
        return f"Error: The folder '{IMAGE_FOLDER}' was not found. Please create it inside your project."

    # On récupère la liste de toutes les images
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('index.html', images=images)

@app.route('/img/<filename>')
def display_image(filename):
    # Flask is smart: it will now look inside static/img
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5002)