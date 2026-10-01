from flask import Flask, request, render_template_string, jsonify
import json, os

app = Flask(__name__)
JSON_FILE = 'data.json'

HTML = '''
<body>
    <h1>Gästbok</h1>
    <p>Fyll i följande:</p>
    <form method="POST" action="/write-json">
        <label for="name">Namn:</label><br>
        <input type="text" name="namn"><br>
        <label for="email">Email:</label><br>
        <input type="email" name="email"><br>
        <label for="hpage">Homepage:</label><br>
        <input type="text" name="homepage"><br>
        <label for="tele">Telefon nummer:</label><br>
        <input type="number" name="telefon"><br>
        <label for="comm">Comment:</label><br>
        <textarea name="comment" id="comment" rows="4" cols="50"></textarea><br>
        <button type="submit">Submit</button>
    </form>
    <h2>Tidigare inlägg</h2>
    <div class="posts-list">
        {% for post in posts %}
            <div class="post-card">
                <hr>
                användare: {{ post.namn }}<br> 
                email: {{ post.email }}<br> 
                homepage: {{ post.homepage }}<br> 
                telefon: {{ post.telefon }}<br> 
                comment: {{ post.comment }}<br>
            </div>
        {% endfor %}
</div>
</body> 
'''

def load_posts():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []   

@app.route('/')
def json_demo():
    return render_template_string(HTML, posts=load_posts(), indent=4, ensure_ascii=False)

@app.route('/write-json', methods=['POST'])
def write_json():
    posts = load_posts()
    posts.append({
        'namn': request.form.get('namn', ''),
        'email': request.form.get('email', ''),
        'homepage': request.form.get('homepage', ''),
        'telefon': request.form.get('telefon', ''),
        'comment': request.form.get('comment', '')
    })
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
    return render_template_string(HTML, posts=load_posts(), indent=4, ensure_ascii=False)

app.run(debug=True)

