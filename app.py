from flask import Flask, render_template, request

app = Flask(__name__)

f = open("RecordVals", 'a')

def valid_nums(inVal):
    if inVal > 0 and inVal < 10:
        return True
    return False

def send_value(inVal):
    f.write(str(inVal))


@app.route('/', methods = ['GET', 'POST'])
def provide_values():

    if request.method == 'POST':
        curVal = request.form.get('val')
        return str(curVal)
        if valid_nums(curVal):
        #here is where somthing should be done with the value
            send_value(curVal)

            return render_template('form.html')
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')





