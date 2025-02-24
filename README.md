Minor Project
---

### **📌 README.md for GitHub**  

```md
# ♟️ Chess Reinforcement Learning - AI-Powered Chess Engine  

## 🚀 Overview  
This project implements a **Chess AI** using **Reinforcement Learning (RL)** to predict optimal moves and provide an intelligent opponent for users. The system leverages **Deep Neural Networks (DNNs)** trained using **Deep Q-Learning (DQN)** to evaluate board positions and make decisions.  

The project consists of a **Flask-based backend**, a **React.js frontend**, and an AI model trained with **TensorFlow/Keras**. The chess board is rendered using **Chessboard.js**, and game logic is managed with **python-chess**.  

---

## 📌 Features  
✅ **AI-Powered Chess Opponent** (Learns & adapts to gameplay)  
✅ **Deep Q-Learning for Move Prediction**  
✅ **Interactive Chessboard with React & Chessboard.js**  
✅ **Backend API using Flask**  
✅ **Game State Representation using FEN (Forsyth-Edwards Notation)**  
✅ **Optimized Reinforcement Learning Model**  
✅ **Scalable & Extendable for Future Enhancements**  

---

## 📂 Project Structure  

```
📂 src
 ┣ 📂 backend  (Flask-based API for AI Model)
 ┃ ┣ 📜 app.py  (Main backend logic)
 ┃ ┣ 📜 model.py  (Reinforcement Learning model for move prediction)
 ┃ ┣ 📜 requirements.txt  (Dependencies for Flask & AI)
 ┣ 📂 frontend  (React-based UI for Chess)
 ┃ ┣ 📜 App.js  (Main React app)
 ┃ ┣ 📜 Board.js  (Chessboard UI using Chessboard.js)
 ┃ ┣ 📜 api.js  (Handles communication with backend)
 ┣ 📜 train.py  (Script to train the AI model using Deep Q-Learning)
 ┣ 📜 README.md  (Project documentation)
```

---

## 🏗️ **Technologies Used**  

### **Frontend:**  
- ⚛️ **React.js** – For interactive chessboard UI  
- ♟️ **Chessboard.js** – To render & control chess movements  
- 🎨 **Styled Components** – For a modern UI  

### **Backend:**  
- 🐍 **Flask** – To serve AI-powered move prediction  
- 🏗️ **Python-Chess** – For game logic and rule validation  
- 🔍 **TensorFlow/Keras** – For training & running the AI model  

### **AI Model:**  
- 🤖 **Deep Q-Learning (DQN)** – For move prediction  
- 📊 **Neural Networks** – Trained using past chess games  

---

## 🎯 **How It Works**  

1️⃣ **Game Start** → React UI displays chessboard (Chessboard.js)  
2️⃣ **Player Move** → User makes a move; game state is updated  
3️⃣ **AI Move Prediction** → Flask backend uses trained RL model to predict the best move  
4️⃣ **Move Execution** → The AI move is sent back & displayed on the UI  
5️⃣ **Learning & Improvement** → AI continuously improves through self-play  

---

## 📌 **Setup & Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Harsha-2604/Minor-Project.git
cd chess-rl
```

### **2️⃣ Install Dependencies**  

#### **Backend (Flask API)**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### **Frontend (React UI)**
```bash
cd frontend
npm install
npm start
```

---

## 📊 **Training the AI Model**  
To train the AI model with reinforcement learning:  
```bash
python train.py --games=1000 --learning_rate=0.001
```
This will run **1000 simulated chess games** for training the AI.

---

## 🎮 **Live Demo & Usage**  
Once the backend and frontend are running, open:  
📌 **`http://localhost:3000/`** → Play chess against the AI  

---

## 🔮 **Future Enhancements**  
📌 **Dynamic Difficulty Adjustment** – AI adapts to player skill level  
📌 **Multiplayer Mode** – Play against other human players  
📌 **AI Move Explanation** – Explain why the AI chooses a move  
📌 **Online Deployment** – Host on a cloud platform  

---

## 🤝 **Contributors**  
📌 **N. Deekshith Reddy** (21BD1A1241)  
📌 **G. Nihanth** (21BD1A1240)  
📌 **V. Harsha Vardhan Reddy** (21BD1A1261)  
📌 **K. Shiva Sai** (21BD1A1227)  

Under the guidance of **Ms. Nidhi** (Assistant Professor, IT Department)  

---

## 📄 **License**  
This project is open-source and available under the **MIT License**.  

---

🚀 **Ready to Play Chess with AI? Start Now!** ♟️  

```md
