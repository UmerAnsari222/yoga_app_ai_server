from flask import Flask, request, jsonify
import cv2
from main import YogaAnalyzer
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/analyze_yoga', methods=['POST'])
def analyze_yoga():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    video_path = os.path.join("temp", video_file.filename)
    video_file.save(video_path)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return jsonify({"error": "Could not open video file"}), 400

    yoga_analyzer = YogaAnalyzer()

    fps = cap.get(cv2.CAP_PROP_FPS)
    results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result_frame = yoga_analyzer.analyze_pose(frame)
        results.append(yoga_analyzer.get_results())

    cap.release()
    os.remove(video_path)

    return jsonify(results)


@app.route('/analyze_yoga2', methods=['GET'])
def analyze_yoga2():
    return jsonify({"msg": "Hello"})


if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    # app.run(debug=True, host='192.168.43.231', port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)
