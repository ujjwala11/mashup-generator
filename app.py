print("THIS IS THE RUNNING FILE")

from flask import Flask, render_template, request, send_file
import zipfile
from mashup_logic import create_mashup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        singer = request.form['singer']
        count = int(request.form['count'])
        duration = int(request.form['duration'])

        output = "output.mp3"
        zipname = "mashup.zip"

        print("Mashup started...", flush=True)

        create_mashup(singer, count, duration, output)

        print("Mashup finished!", flush=True)

        with zipfile.ZipFile(zipname, 'w') as zipf:
            zipf.write(output)

        print("Zip created!", flush=True)

        return send_file(
            zipname,
            as_attachment=True,
            download_name="mashup.zip"
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
