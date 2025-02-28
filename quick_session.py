from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'computador'

@app.route('/setuser/<user>')
def setuser (user: str) -> str:
    session['user'] = user
    return'User value is currently ser to: ' + session['user']
    
if __name__ == '__main__':
    app.run(debug=True)