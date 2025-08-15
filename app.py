from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, uuid, shutil, zipfile

from utils.split import split_each_page_in_two

UPLOAD_ROOT = os.environ.get("UPLOAD_ROOT", os.path.join(os.path.dirname(__file__), "workspace"))
os.makedirs(UPLOAD_ROOT, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}
def allowed_file(filename): return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")  # à changer en prod

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("files")
    if not files or files == [None]:
        flash("Aucun fichier envoyé.")
        return redirect(url_for("index"))

    job_id = str(uuid.uuid4())
    job_dir = os.path.join(UPLOAD_ROOT, job_id)
    in_dir, out_dir = os.path.join(job_dir, "in"), os.path.join(job_dir, "out")
    os.makedirs(in_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    converted = []
    for f in files:
        if not f or f.filename == "":
            continue
        if not allowed_file(f.filename):
            flash(f"Fichier ignoré (non PDF) : {f.filename}")
            continue

        fname = secure_filename(f.filename)
        src_path = os.path.join(in_dir, fname)
        f.save(src_path)

        base, _ = os.path.splitext(fname)
        dst_name = f"{base}_split2_vertical.pdf"
        dst_path = os.path.join(out_dir, dst_name)
        try:
            split_each_page_in_two(src_path, dst_path, direction="vertical")
            converted.append(dst_name)
        except Exception as e:
            flash(f"Erreur conversion {fname}: {e}")

    if not converted:
        flash("Aucun PDF converti.")
        shutil.rmtree(job_dir, ignore_errors=True)
        return redirect(url_for("index"))

    return render_template("result.html", job_id=job_id, files=converted)

@app.route("/download/<job_id>/<path:filename>")
def download(job_id, filename):
    out_dir = os.path.join(UPLOAD_ROOT, job_id, "out")
    return send_from_directory(out_dir, filename, as_attachment=True)

@app.route("/download-zip/<job_id>")
def download_zip(job_id):
    job_dir = os.path.join(UPLOAD_ROOT, job_id)
    out_dir = os.path.join(job_dir, "out")
    zip_path = os.path.join(job_dir, "converted.zip")
    if not os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for fname in os.listdir(out_dir):
                zf.write(os.path.join(out_dir, fname), arcname=fname)
    return send_from_directory(job_dir, "converted.zip", as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
