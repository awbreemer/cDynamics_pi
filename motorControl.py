from flask import Flask, render_template, request, redirect, url_for
import serial
import time
from valueConfig import *
#from flask_sslify import SSLify



#MENU OPTIONS



def output_val(inVal):
    F = open("RecordVals.txt", 'a')
    F.write("\n" + str(inVal))
    F.close()



def to_arduino_serial(inString):
    """Write a string to arduino
    gets encoded with UTF-8
    function takes a string
    function returns a string that the arduino sends"""
    ser.write((inString + "\n").encode('UTF-8'))
    line = ser.readline().decode('UTF-8').rstrip()
    print(line)
    return line


class process_vals:
    """Class used to process button imputs from main page"""
    def __init__(self, adjustVal = ""):
        """Shoud be called with no input except for testing"""
        if adjustVal == "":
            self.adjustVal = 0.0
        else:
            self.adjustVal = float(adjustVal)

    def input_request_val(self, val):
        """Used for numeric string input on main page
        takes in a string value
        adds to the adjust value"""
        if val != "":
            try:
                self.adjustVal += float(val)
            except:
                pass

    def input_request_but(self, button_val, amount):
        """Used for handling adjust buttons
        takes in string or none, indicating if 'pressed' or not
        if pressed, adds amount on the the adjust value"""
        if button_val != None:
            self.adjustVal += amount

    def return_turn_amt(self):
        """Returns the adjust value that complies the buttons or input
        string. """
        return self.adjustVal
    
def menu_option_adjust(menu_option, value):
    """Takes String for the menu option to be changed.
    Takes a value for the menu_option to be adjusted to.
    Sets the global values to the new ones."""
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
    """This software uses a config.py file to store values between use sessions.
    config.py should be updated when global vaiables are changed so that values are saved between sessions. 
    This function updates all the values stored in the config.py file."""
    with open("valueConfig.py", 'w') as file:
        toFile = f"small_adjust_val = {small_adjust_val}\nlarge_adjust_val = {large_adjust_val}\nbaud_rate = {baud_rate}\n"
        toFile += f"password = '{password}'\nuser_name = '{user_name}'"
        file.write(toFile)
        file.close()


def test_3_args(a1, a2, a3 = 0):
    print(a1)
    print(a2)
    if a3 != 0:
        print(a3)   




app = Flask(__name__)
#sslify = SSLify(app)
#sslify = SSLify(app, permanent=True, age=300, subdomains=True, port=8443)



@app.route('/home', methods = ['GET', 'POST'])
def home():
    """This function handles the main page of the motor. """
    outText = "-"
    previous_step_size = 'a1'
    if request.method == 'POST':
        newVal = process_vals()
        newVal.input_request_val(request.form.get('user_val'))
        #test_3_args(request.form.get('big_decrease'), -large_adjust_val)
        newVal.input_request_but(request.form.get('big_decrease'), -large_adjust_val)
        newVal.input_request_but(request.form.get('decrease'), -small_adjust_val)
        newVal.input_request_but(request.form.get('increase'), small_adjust_val)
        newVal.input_request_but(request.form.get('big_increase'), large_adjust_val)
        stepSize = request.form.get('stepSize')
        previous_step_size = stepSize
        to_arduino_serial(stepSize)
        print(f"The output of the request form is {request.form.get('valueAdjust')} .")
        output_val(newVal.return_turn_amt()) 
        outText = to_arduino_serial(str(newVal.return_turn_amt()))
        time.sleep(1)
    return render_template("main.html", returnText=outText, default_step = previous_step_size)

@app.route('/menu', methods = ['GET', 'POST'])
def menu():
    """This function handles the value adjust page of the motor."""
    if request.method == 'POST':
        global small_adjust_val, large_adjust_val, baud_rate, password, user_name
        user_name = request.form['userNameChange']
        password = request.form['passwordChange']
        smallAdjustString = request.form.get('smallAdjustVal')
        try: 
            small_adjust_val =  float(smallAdjustString)
        except:
            pass
        largeAdjustString = request.form.get('largeAdjustVal')
        try:
            large_adjust_val = float(largeAdjustString)
        except:
            pass
        baudAdjustString = request.form.get('baudRateAdjust')
        try:
            baud_rate = int(baudAdjustString)
        except:
            pass
        rewriteValueConfigPy()
        return redirect(url_for('home'))

    return render_template("menu.html", smallAdjust=small_adjust_val, largeAdjust=large_adjust_val, baudRate=baud_rate, password = password, userName = user_name)

@app.route('/', methods=['GET', 'POST'])
def login():
    """This page handles the login page of the website."""
    print(f"the password is {password} and the username is {user_name}.")
    error = None
    if request.method == 'POST':
        if request.form['username'] != user_name or request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)        


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1)
    ser.reset_input_buffer()
    app.run(host="0.0.0.0", debug=True)

