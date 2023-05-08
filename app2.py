from flask import Flask, render_template, request
import serial
import time
from valueConfig import *
#from flask_sslify import SSLify



#MENU OPTIONS


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
    line = ser.readline().decode('UTF-8').rstrip()
    print(line)
    return line


class process_vals:
    def __init__(self, adjustVal = None):
        if adjustVal == "":
            self.adjustVal = 0.0
        else:
            self.adjustVal = float(adjustVal)

    def input_request_val(self, val):
        if val != None:
            self.adjustVal += float(val)

    def input_request_but(self, button_val, amount):
        if button_val != None:
            self.adjustVal += amount

    def return_turn_amt(self):
        return self.adjustVal
    
def menu_option_adjust(menu_option, value):
    if menu_option == "small_adjust_val":
        global small_adjust_val 
        small_adjust_val = value
    elif menu_option == "large_adjust_val":
        global large_adjust_val
        large_adjust_val = value
    elif menu_option == "baud_rate":
        global baud_rate
        baud_rate = value  

def rewriteValueConfigPy():
    with open("valueConfig.py", 'w') as file:
        toFile = f"small_adjust_val = {small_adjust_val}\nlarge_adjust_val = {large_adjust_val}\nbaud_rate = {baud_rate}"
        file.write(toFile)


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
        print(f"The output of the request form is {request.form.get('valueAdjust')} .")
        output_val(newVal.return_turn_amt()) 
        outText = to_arduino_serial(str(newVal.return_turn_amt()))
    return render_template("form2.html", returnText=outText)

@app.route('/menu', methods = ['GET', 'POST'])
def menu():
    if request.method == 'POST':
        pass
    return render_template("valueChangePage.html", smallAdjust=small_adjust_val, largeAdjust=large_adjust_val, baudAdjust=baud_rate)
        


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1)
    ser.reset_input_buffer()
    app.run(host="0.0.0.0", debug=True)

