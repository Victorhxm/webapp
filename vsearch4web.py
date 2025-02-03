from flask import Flask, render_template, request
from vsearch import search4letters
from markupsafe import escape
import mysql.connector


app = Flask(__name__)

def log_request (req: 'flask_request', res: str) -> None:
    
    # Infor conection 
    dbconfig = { 'host': '127.0.0.1',
                'user': 'vsearch',
                'password': 'vsearchpasswd',
                'database': 'vsearchlogDB',}
                
    conn = mysql.connector.connect (**dbconfig)

    cursor = conn.cursor()
    
    _SQL =( "INSERT INTO log  (phrase, letters, ip, browser_string, results)"
            "values (%s, %s, %s, %s, %s)")
    cursor.execute(_SQL, (req.form['phrase'],
                        req.form['letters'],
                        req.remote_addr,
                        req.headers.get('User-Agent'), 
                        res,))
    conn.commit()
    cursor.close()
    conn.close()
    


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
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
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title = 'Welcome to search4letters on the web!')
                           

@app.route('/viewlog') #Criar a url.
def view_the_log() -> 'html': #Criando uma função que retorna HTML.
    contents = [] #Criação de uma lista chamada de contents.
    with open('vsearch.log') as log:  # Abrindo o arquivo e salvando os dados na variavel log.
        for line in log:
            contents.append([]) #Anexa uma nova lista vazia a contents.
            for item in line.split('|'):  # Divide cada linha (com base na barra vertical), então então processa cada item na "lista dividida" resultante.
                contents[-1].append(escape(item))  # A linha do momento no "for" é adicionada na utima lista da lista contents.
    titles = ('Form Data', ' Remote_addr', 'User_agent', 'Results')
    
    return render_template('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)


if __name__=='__main__':
    app.run(debug=True)
    
