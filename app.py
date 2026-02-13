import os
import numpy as np
import io
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from sklearn.cluster import KMeans
from flask import Flask, render_template, request, send_file, abort

app = Flask(__name__)

# Variable globale pour stocker le chemin de l'image sélectionnée
current_image_path = ""

def select_file_via_gui():
    """Ouvre une fenêtre Windows pour choisir une image"""
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale de tkinter
    root.attributes('-topmost', True)  # Met la fenêtre au premier plan
    file_path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png *.webp")]
    )
    root.destroy()
    return file_path

@app.route("/")
def home():
    global current_image_path
    
    # Si l'utilisateur clique sur "Sélectionner un fichier"
    if request.args.get("action") == "select":
        path = select_file_via_gui()
        if path:
            current_image_path = path

    algo = request.args.get("algo", "original")
    k = int(request.args.get("k", 6))

    return render_template(
        "home.html",
        selected_path=current_image_path,
        filename=os.path.basename(current_image_path),
        algo=algo,
        k=k
    )

@app.route("/photo")
def photo():
    global current_image_path
    if not current_image_path or not os.path.exists(current_image_path):
        return abort(404)

    algo = request.args.get("algo", "original")
    k = int(request.args.get("k", 6))
    
    # Ouvrir l'image
    img = Image.open(current_image_path).convert("RGB")
    
    if algo == "kmeans":
        # On réduit pour la vitesse de calcul
        img.thumbnail((500, 500))
        data = np.array(img)
        h, w, _ = data.shape
        pixels = data.reshape(-1, 3).astype(np.float32)

        km = KMeans(n_clusters=k, n_init="auto", random_state=0)
        labels = km.fit_predict(pixels)
        centers = km.cluster_centers_
        
        new_pixels = centers[labels].reshape(h, w, 3)
        img = Image.fromarray(np.clip(new_pixels, 0, 255).astype(np.uint8))

    # ENVOI EN MÉMOIRE (RAM) : Pas de fichier créé sur le PC
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, port=5002)