from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        value = request.form['value']
        #here is where somthing should be done with the value
        return 'You entered: {}'.format(value)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')