from flask import Flask, jsonify

app = Flask(__name__)

# Contoh data artikel tentang ikan
articles = [
    {
        "id": 1,
        "title": "Mengenal Ikan Tuna",
        "description": "Ikan tuna merupakan salah satu ikan laut yang banyak dikonsumsi karena kaya akan protein.",
        "image_url": "https://example.com/images/tuna.jpg"
    },
    {
        "id": 2,
        "title": "Manfaat Ikan Salmon",
        "description": "Ikan salmon mengandung asam lemak omega-3 yang baik untuk kesehatan jantung.",
        "image_url": "https://example.com/images/salmon.jpg"
    },
    {
        "id": 3,
        "title": "Ikan Koi: Simbol Keberuntungan",
        "description": "Ikan koi dikenal sebagai simbol keberuntungan dalam budaya Jepang.",
        "image_url": "https://example.com/images/koi.jpg"
    }
]

@app.route('/articles', methods=['GET'])
def get_articles():
    return jsonify({"articles": articles})

if __name__ == '__main__':
    app.run(debug=True)
