from flask import Flask, render_template, send_file
import io
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/results')
def results_img():
    with open("./static/results/yuri.jpg", 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/jpg'
        )
    return send_file('./static/results/yuri.jpg',mimetype='image/jpg')
    # return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
