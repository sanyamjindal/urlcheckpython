from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

# Initialize the model
model = DecisionTreeClassifier()

# Example function to extract features from a URL
def extract_features(url):
    parsed_url = urlparse(url)
    
    features = {
        'url_length': len(url),
        'path_length': len(parsed_url.path),
        'query_length': len(parsed_url.query),
        'has_ip': int(parsed_url.netloc.count('.') == 3 and all(part.isdigit() for part in parsed_url.netloc.split('.'))),
    }
    
    return list(features.values())

# Dummy data for demonstration (replace with your dataset)
X_train = [
    extract_features("https://www.example.com"),
    extract_features("https://www.anotherexample.com"),
    # Add more samples...
]

y_train = [0, 1]  # 0 for legitimate, 1 for phishy (replace with your labels)

# Train the model
model.fit(X_train, y_train)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_url', methods=['POST'])
def check_url():
    try:
        url = request.form['url']
        url_features = extract_features(url)
        prediction = model.predict([url_features])[0]
        result = "Legit" if prediction == 0 else "Phishy"
        return render_template('result.html', url=url, result=result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
