
# PPE Detection Web App 🚧

A Flask-based web application for detecting Personal Protective Equipment (PPE) like helmets, vests, gloves, and masks in real-time or from uploaded videos using a YOLOv8 model. Users can choose detection **with alert sound** or **without alert**, and the app plays an audio warning if PPE violations are detected (when enabled).

## 🔧 Features

- 🎥 Webcam (Live Camera) and 🎞️ Uploaded Video input options
- ✅ Toggle detection mode: With or Without Alert
- 🔊 In-browser alert sound on PPE violation (via HTML5 audio)
- 🧠 YOLOv8 object detection
- 📷 Supports extension for image/photo input (optional)
- 🖥️ Live streaming of video with bounding boxes using OpenCV

## 🚀 Demo

![App Screenshot](static/Screenshot%202025-07-31%20175401.png)

## 🗂️ Project Structure

```
PPE-Detection/
│
├── main.py                  # Main Flask app
├── templates/
│   ├── index.html           # Input form UI
│   └── result.html          # Video streaming page
├── static/
│   ├── alert.mp3            # Alert sound file
│   ├── style.css            # CSS styling
│   └── uploads/             # Uploaded videos (optional)
├── best.pt                  # Trained YOLOv8 model
├── requirements.txt         # Python dependencies
├── config.py                # Alert config (mode flags)
└── README.md
```

## 📁 Requirements

- Python 3.8+
- Flask
- OpenCV
- cvzone
- ultralytics
- numpy

Install all using:

```bash
pip install -r requirements.txt
```

## 🔊 How Alert Works

- When "With Alert" is selected, the app sets `alert_enabled = True` in `config.py`
- On PPE violation (e.g., no helmet), `result.html` triggers the browser to play `alert.mp3` using JavaScript

> **Note**: Audio only plays on real browser interaction. Not supported in all mobile browsers or incognito mode.

## 📸 Future Improvements

- Add image (photo) upload support
- Dashboard with violation counts
- Multi-camera support
- Add detection logs

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

**Made with ❤️ by Ankush Raut**
