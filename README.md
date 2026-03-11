# AI Image Detector

A web application that detects whether an image is AI-generated or real using an AI detection API.

## 🌐 Live Demo

Frontend (Website)  
https://ai-detector-krishp69.vercel.app

Backend API  
https://ai-detector-api-q80d.onrender.com

GitHub Repository  
https://github.com/KrishP69/Ai-Detector

---

## 🚀 Features

- Upload image or drag & drop
- AI-generated image detection
- Confidence score with progress bar
- Image preview before analysis
- Loading animation while analyzing
- Scan history
- Dark / light mode toggle
- Responsive modern UI
- Deployed full-stack application

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Deployment
- Vercel (Frontend hosting)
- Render (Backend hosting)

### AI Detection API
- Sightengine API

---

## 📂 Project Structure

Ai-Detector
│
├── index.html
├── style.css
├── script.js
│
└── Backend
    ├── app.py
    ├── detector.py
    ├── requirements.txt
    └── .env

---

## ⚙️ How It Works

1. User uploads an image  
2. Frontend sends the image to the backend API  
3. Backend sends the image to the AI detection API  
4. API analyzes whether the image is AI-generated  
5. Backend returns the result with confidence score  
6. Frontend displays the result and confidence bar  

---

## 💻 Installation (Run Locally)

Clone the repository

git clone https://github.com/KrishP69/Ai-Detector.git

Go into project directory

cd Ai-Detector

Install backend dependencies

pip install -r Backend/requirements.txt

Run the backend

python Backend/app.py

Open the frontend

index.html

---

## 📊 Example Result

AI Generated (92% confidence)

or

Likely Human (14% AI probability)

---

## 🎯 Future Improvements

- Support video deepfake detection
- Add AI model locally (TensorFlow / PyTorch)
- Image analysis history database
- User authentication
- Batch image detection

---

## 👨‍💻 Author

Krish Patil

BTech IT Student  
Passionate about AI, Robotics, and Full Stack Development

GitHub  
https://github.com/KrishP69

---

## 📜 License

This project is open-source and available under the MIT License.
