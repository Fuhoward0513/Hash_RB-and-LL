from flask import Flask, render_template, send_file, jsonify
import io
import requests
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
@app.route('/tour')
def getTourData():
    r = requests.get(url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/u?key=0ee0aa7e-394f-48bc-a9ba-3c9960029c94", headers={"accept": "application/json"})
    data = r.json()
    print(data[0])
    return data[0]

if __name__ == '__main__':
    app.run(debug=True)
    
