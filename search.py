from flask import Flask, url_for, request, render_template
from elastic import search, es

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def form():
    return render_template('form_submit.html')

@app.route('/search', methods=['POST'])
def results():
    query=request.form['query']
    hits = search(query)
    hits = hits['hits']['hits']
    return render_template('form_action.html', hits = hits)

if __name__ == '__main__':
    """
    es.update(index='page',doc_type='website',
                body={"body": {"similarity": 'BM25'},
                      "header": {"similarity": 'BM25'},
                      "url": {"similarity": 'BM25'}})
    """
    app.run()
