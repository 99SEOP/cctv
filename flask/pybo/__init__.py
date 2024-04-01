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

# 방향별 카운트
car_count_up = 0
car_count_down = 0
car_count_left = 0
car_count_right = 0


# 길이계산
def calculate_length(points):
    total_length = 0
    for i in range(len(points) - 1):
        total_length += np.linalg.norm(points[i + 1] - points[i])
    return total_length


# Load YOLOv8 model
model = YOLO("car-cctv-6.pt")
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])

# Set of car IDs that crossed the line
crossed_car_ids = set()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
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
        cv2.putText(
            annotated_frame,
            f"Up: {car_count_up}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            annotated_frame,
            f"Down: {car_count_down}",
            (200, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            annotated_frame,
            f"Left: {car_count_left}",
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            annotated_frame,
            f"Right: {car_count_right}",
            (200, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        # 창에 표시
        #cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # q눌러서 종료
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

print("Car count - Up:", car_count_up)
print("Car count - Down:", car_count_down)
print("Car count - Left:", car_count_left)
print("Car count - Right:", car_count_right)

def GenerateFrames():
    while True:
        sleep(0.1)  # 프레임 생성 간격을 잠시 지연시킵니다.
        ref, frame = cap.read()  # 비디오 프레임을 읽어옵니다.
        if not ref:  # 비디오 프레임을 제대로 읽어오지 못했다면 반복문을 종료합니다.
            break
        else:
            ref, buffer = cv2.imencode('.jpg', frame)  # JPEG 형식으로 이미지를 인코딩합니다.
            frame = buffer.tobytes()  # 인코딩된 이미지를 바이트 스트림으로 변환합니다.
            # multipart/x-mixed-replace 포맷으로 비디오 프레임을 클라이언트에게 반환합니다.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


app = Flask(__name__)

CORS(app)

number = 0

@app.route('/')
def index():
    global number
    return jsonify({'number' : number})
    

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        return jsonify(message="GET request received, CORS is enabled!")

@app.route('/video', methods=['GET'])
def stream():
    return Response(GenerateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)