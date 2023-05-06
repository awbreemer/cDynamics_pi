from flask import Flask, render_template, request
import serial
import time
#from flask_sslify import SSLify

small_adjust_val = .1
large_adjust_val = .5
baud_rate = 9600

# def determine_input(cust, big_d, d, i, big_i):
#     args = locals()
#     for j in args:
#         if j is not None:
#             return j, 

def output_val(inVal):
    F = open("RecordVals.txt", 'a')
    F.write("\n" + str(inVal))
    F.close()

def to_arduino_serial(inString):
    ser.write((inString + "\n").encode('UTF-8'))
    line = ser.readline().decode('ASCII').rstrip()
    print(line)
    time.sleep(1)
    return line


class process_vals:
    def __init__(self, adjustVal = None):
        if adjustVal == None:
            self.adjustVal = 0.0
        else:
            self.adjustVal = adjustVal

    def input_request_val(self, val):
        if val != "":
            self.adjustVal += float(val)

    def input_request_but(self, button_val, amount):
        if button_val != None:
            self.adjustVal += amount

    def return_turn_amt(self):
        return self.adjustVal

def test_3_args(a1, a2, a3 = 0):
    print(a1)
    print(a2)
    if a3 != 0:
        print(a3)   

app = Flask(__name__)
#sslify = SSLify(app)
#sslify = SSLify(app, permanent=True, age=300, subdomains=True, port=8443)



@app.route('/', methods = ['GET', 'POST'])
def provide_values():
    outText = "-"
    if request.method == 'POST':
        newVal = process_vals()
        newVal.input_request_val(request.form.get('user_val'))
        #test_3_args(request.form.get('big_decrease'), -large_adjust_val)
        newVal.input_request_but(request.form.get('big_decrease'), -large_adjust_val)
        newVal.input_request_but(request.form.get('decrease'), -small_adjust_val)
        newVal.input_request_but(request.form.get('increase'), small_adjust_val)
        newVal.input_request_but(request.form.get('big_increase'), large_adjust_val)
        output_val(newVal.return_turn_amt()) 
        outText = to_arduino_serial(str(newVal.return_turn_amt()))
    return render_template("form2.html", returnText=outText)


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1)
    ser.reset_input_buffer()
    app.run(host="0.0.0.0", debug=True)

