from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

def fetch_numbers_from_url(url, timeout=0.5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except requests.exceptions.Timeout:
        pass  # Ignore URLs that exceed the timeout
    except Exception as e:
        print(f"Error fetching numbers from {url}: {e}")
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')

    merged_numbers = []
    for url in urls:
        numbers = fetch_numbers_from_url(url)
        merged_numbers.extend(numbers)

    merged_numbers = list(set(merged_numbers))  # Remove duplicates
    merged_numbers.sort()  # Sort in ascending order

    return jsonify(numbers=merged_numbers)

if __name__ == '__main__':
    app.run(port=8008)
