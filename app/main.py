from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", img_id="images/cloud.jpg")


@app.route('/home', methods=['POST'])
def process_post():
    img_dir = request.form.get("img_dir")

    print(img_dir)

    new_img_id = request.form.get("img_file")
    new_img_id = img_dir + "/" + new_img_id + '.jpg'

    print(new_img_id)

    return render_template("home.html", img_id=new_img_id)


if __name__ == "__main__":
    app.run(debug=True)
