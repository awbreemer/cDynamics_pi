from flask import Flask, request

app = Flask(__name__)
user_strings = []

@app.route('/', methods=['GET', 'POST'])
def record_strings():
    if request.method == 'POST':
        user_string = request.form.get('user_string')
        user_strings.append(user_string)
    return '''
        <form method="POST">
            <label>Enter a string:</label>
            <input type="text" name="user_string">
            <button type="submit">Submit</button>
        </form>
        <br>
        <h3>Recorded strings:</h3>
        <ul>
            {% for string in user_strings %}
            <li>{{ string }}</li>
            {% endfor %}
        </ul>
    '''

if __name__ == '__main__':
    app.run(debug=True)