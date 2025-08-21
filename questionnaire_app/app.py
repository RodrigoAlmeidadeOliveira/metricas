from flask import Flask, render_template, request, url_for
import csv
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

OPTIONS = {
    "1": "Nunca ou raramente (de cada 10 situações reage dessa forma sem necessidade de ajuda no máximo 2 vezes)",
    "2": "Com pouca frequência (de cada 10 situações desse tipo reage dessa forma sem necessidade de ajuda 3 a 4 vezes)",
    "3": "Com regular frequência (de cada 10 situações reage dessa forma sem necessidade de ajuda 4 a 6 vezes)",
    "4": "Muito frequentemente (de cada 10 situações reage dessa forma sem necessidade de ajuda 6 a 8 vezes)",
    "5": "Sempre ou quase sempre (de cada 10 situações reage dessa forma sem necessidade de ajuda 8 a 10 vezes)",
}

QUESTIONS = [
    "Olhar para o adulto quando chamada pelo nome",
    "Manter contato pocular por pelo menos 1 segundo, quando chamada pelo nome",
    "Olhar nos olhos de uma pessoa durante uma interação (aprox. 3 segundos)",
    "Olhar nos olhos de uma pessoa durante 5 segundos",
    "Olhar quando engajada numa brincadeira",
    "Olhar à distância de 3 metros",
    "Olhar à distância de 5 metros",
    "Olhar à distancia de 5 metros e engajada numa brincadeira",
    "Olhar para mais de uma pessoa (duas pessoas chamam a criança alternadamente)",
    "Olhar para mais de uma pessoa alternadamente quando engajada em alguma brincadeira",
]

@app.route('/', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        responses = [request.form.get(f'q{i}', '') for i in range(1, len(QUESTIONS) + 1)]
        filename = Path(__file__).with_name('responses.csv')
        first_write = not filename.exists()
        with filename.open('a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if first_write:
                writer.writerow(['timestamp'] + [f'q{i}' for i in range(1, len(QUESTIONS) + 1)])
            writer.writerow([datetime.now().isoformat()] + responses)
        return render_template('results.html', responses=responses, options=OPTIONS, questions=QUESTIONS)
    return render_template('index.html', questions=QUESTIONS, options=OPTIONS)

if __name__ == '__main__':
    app.run(debug=True)
