from flask import Flask, render_template, request, session
from vsearch import search4letters
from markupsafe import escape
from DBcm import UseDatabase
from checker import check_logged_in


app = Flask(__name__)
    # Infor conection 
app.config['dbconfig'] = { 'host': '127.0.0.1',
            'user': 'vsearch',
            'password': 'vsearchpasswd',
            'database': 'vsearchlogDB',}

def log_request (req: 'flask_request', res: str) -> None: # type: ignore
    """Log details of the web request and the results."""
    with UseDatabase (app.config['dbconfig']) as cursor:
         _SQL = """INSERT INTO log  
         (phrase, letters, ip, browser_string, results)
          values 
          (%s, %s, %s, %s, %s)"""
         cursor.execute(_SQL, (req.form['phrase'],
                        req.form['letters'],
                        req.remote_addr,
                        req.headers.get('User-Agent'), 
                        res,))
@app.route('/status')

@app.route('/search4', methods=['POST'])
def do_search() -> 'html': # type: ignore
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase,letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase = phrase,
                           the_letters = letters,
                           the_title = title,
                           the_results = results)
 
@app.route('/')           
@app.route('/entry')
def entry_page() -> 'html': # type: ignore
    return render_template('entry.html',
                           the_title = 'Welcome to search4letters on the web!')
                           
@app.route('/viewlog') 
@check_logged_in
def view_the_log() -> 'html':  # type: ignore
    
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SLQ = """select phrase, letters, ip, browser_string, results 
        from log"""
        cursor.execute(_SLQ)
        contents =cursor.fetchall()
        
        titles = 'Phrase','Letters', 'Remote_addr', 'User_agente','Results'
        return render_template('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)
    
@app.route('/login')
def do_login ()-> str:
    session['logged_in'] = True
    return 'Agora você está logado.'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'Agora você está desconectado'

app.secret_key = 'computador'

if __name__=='__main__':
    app.run(debug=True)
    
