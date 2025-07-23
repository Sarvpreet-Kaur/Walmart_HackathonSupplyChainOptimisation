### 🛒 AI-Powered Inventory Forecasting for Sustainable Retail
Reducing Overstock and Waste with Intelligent Demand Prediction

## 📌 Problem Statement
Retailers like Walmart face challenges in managing inventory across thousands of products. Overstocking leads to waste, markdowns, and higher carbon emissions, while understocking results in lost sales and customer dissatisfaction.
We aim to build a solution that helps forecast demand accurately, minimize excess inventory, and optimize replenishment — creating a more sustainable and responsible retail future.

## 🎯 Solution Overview
We built an AI-powered web tool that forecasts future sales for individual products and recommends inventory actions, helping reduce waste and improve availability.

## Key Features:
📈 Forecasts daily demand using Prophet (97% accuracy)
📦 Takes user input for product type, sales file, forecast range, and current stock
📊 Displays clear charts, reorder/excess suggestions, and model accuracy
🌱 Tracks potential waste reduction to align with sustainability goals

## 🧠 Tech Stack
Layer	Tech Used
⚙️ Backend	FastAPI
🌐 Frontend	Streamlit
📊 ML Model	Facebook Prophet
📁 Data	Simulated product-level sales (Milk, Bread, Snacks, etc.)
☁️ Hosting	(Streamlit Cloud, Render)

## 📦 Architecture
[ User Input (CSV + Product Info) ]
              ↓
     [ FastAPI Backend ]
              ↓
   [ Prophet Forecasting Model ]
              ↓
[ Inventory Recommendation Engine ]
              ↓
     [ Streamlit Frontend UI ]

     
## 🧠 Example Use Case
1. ser uploads sales data for Milk (daily units sold).
2. Selects forecast window, e.g., 7 days and enters current stock.
3. Model predicts demand for the next 7 days.
4. System recommends:
    “Reorder 42 units” or
    “Surplus of 18 units”
5. Forecast accuracy and visual trends are also shown

## ⚙️ Output:
✅ Predicted daily sales
📉 Units overstocked or 📈 Reorder suggestion
📊 Forecast chart + model accuracy
🎯 Sustainability metric: Wasted units avoided

## 📦 Sample Products
We tested our solution on the following simulated datasets:

🥛 Milk
🍞 Bread
🍎 Fruits
🧼 Detergent
🍪 Snacks

Each product’s dataset follows a realistic trend with seasonality and noise.

## 🚀 How to Run the Project
Run this link directly to see the working:
https://walmarthackathonsupplychainoptimisation-ahoa5v5yxzgktsujmxpe2r.streamlit.app/

Clone the repo:
git clone https://github.com/your-username/Walmart-HackathonSupplyChainOptimisation.git
cd Walmart-HackathonSupplyChainOptimisation

Install dependencies:
pip install -r requirements.txt

Run the backend (FastAPI):
uvicorn app.main:app --reload

Run the Streamlit frontend:
streamlit run frontend/app.py

📊 Sample Input Format
ds,y
2024-01-01,120
2024-01-02,135
2024-01-03,90
...
ds: date
y: number of units sold

## 🌍 Impact
Benefit	Description
🎯 Less Overstock	Reduces markdowns, spoilage, and waste
✅ Right-Time Replenishment	Helps stores avoid out-of-stock situations
🌱 Sustainability Aligned	Supports Walmart’s goal of responsible retail
💰 Cost Efficiency	Reduces holding and transportation costs

## 👥 Team
Sarvpreet Kaur — AI Developer
Rishabh Srivastava — Backend + UI Developer

## 🏁 Future Scope
🔄 Integration with real-time inventory APIs
📦 Multi-store, multi-warehouse inventory sync
🤖 Advanced ML model options (XGBoost, LSTM)
📊 Dashboard with KPIs & sustainability metrics

###📽️ Demo Video 
https://drive.google.com/file/d/1wde-6muSvpLM-aDMtLQ7C1Ya7Gz4MjG1/view?usp=drive_link<br>
YouTube demo link
https://youtu.be/efOHcBKlLiI

##💡 Inspiration
Inspired by Walmart’s commitment to zero waste, this project shows how AI can be used to reduce overstock and create a smarter, more responsible supply chain.

