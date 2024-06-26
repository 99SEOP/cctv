from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
from time import sleep

# Define line coordinates for direction determination
LINE1_START = (120, 350)
LINE1_END = (715, 330)

LINE2_START = (100, 330)
LINE2_END = (720, 350)

# 길이 임계값
THRESHOLD_LENGTH = 50

# 길이계산
def calculate_length(points):
    total_length = 0
    for i in range(len(points) - 1):
        total_length += np.linalg.norm(points[i + 1] - points[i])
    return total_length


# Load YOLOv8 model
model = YOLO("148-epoch.pt")
video_path = "video-01.mp4"
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])

# Set of car IDs that crossed the line
crossed_car_ids = set()

# 방향별 카운트
car_count_up = 0
car_count_down = 0
car_count_left = 0
car_count_right = 0


def GenerateFrames():
    global car_count_up, car_count_down, car_count_left, car_count_right
    while cap.isOpened():
        success, frame = cap.read() 
        if success:
            
            results = model.track(
                frame, persist=True, verbose=False, tracker="bytetrack.yaml"
            )
            
            # Get the boxes and track IDs
            if results[0].boxes.id != None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
    
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            # Plot the tracks and count cars based on direction
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 30:  # Retain 90 tracks for 90 frames
                    track.pop(0)

            # 이동경로 그리기
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(
                    annotated_frame,
                    [points],
                    isClosed=False,
                    color=(0, 255, 255),
                    thickness=5,
                )
                length = calculate_length(points)

                # 길이 체크
                if length > THRESHOLD_LENGTH:
                    # 차량 중복 제거
                    if track_id not in crossed_car_ids:
                        if len(points) >= 2:
                            # 배열 형태 예외처리
                            if (
                                points.ndim == 3
                                and points.shape[1] == 1
                                and points.shape[2] == 2
                            ):
                                # 점과 점의 차이로 방향 구분
                                dx = points[-1][0][0] - points[0][0][0]
                                dy = points[-1][0][1] - points[0][0][1]

                                crossed_car_ids.add(track_id)
                                if dx > 0:  # right
                                    car_count_right += 1
                                elif dx < 0:  # left
                                    car_count_left += 1
                                if dy > 0:  # down
                                    car_count_down += 1
                                elif dy < 0:  # up
                                    car_count_up += 1
            # q눌러서 종료
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            cap.release()
            cv2.destroyAllWindows()
            break
        
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return

@app.route('/video', methods=['GET'])
def stream():
    return Response(GenerateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/statistics', methods=['GET'])
def car_statistics():
    global car_count_up, car_count_down, car_count_left, car_count_right
    return jsonify(
        {
            "car_count_up": car_count_up,
            "car_count_down": car_count_down,
            "car_count_left": car_count_left,
            "car_count_right": car_count_right,
        }
    )

if __name__ == '__main__':
    app.run(debug=True)