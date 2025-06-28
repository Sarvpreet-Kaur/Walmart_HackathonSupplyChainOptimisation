import streamlit as st
import requests
import pandas as pd
import base64

st.set_page_config(page_title="Supply Chain Forecasting",layout="wide")
st.title("Supply-Chain Demand Forecasting")
st.markdown("Upload your Walmart-format CSV, choose product, and get forecast + inventory advice.")


@st.cache_data
def get_products():
    try:
        response = requests.get("http://127.0.0.1:8000/products/")
        if response.status_code == 200:
            return response.json().get("products",[])
    except Exception as e:
        st.warning("Using fallback product list due to error fetching from backend.")
    return ["snacks","fruits","bread","milk","detergent"]
        


csv_file = st.file_uploader("Upload your sales data CSV",type=["csv"])

col1,col2,col3 = st.columns(3)
with col1:
    product_list = get_products()
    product_name = st.selectbox("Select Product", product_list)
with col2:
    forecast_days = st.number_input("Forecast Days",min_value = 1, max_value=367,value=14)
with col3:
    current_stock = st.number_input("Current Stock Available",min_value=0,max_value=1000000000000000)
    

if st.button("Run Forecast") and csv_file:
    with st.spinner("Forecasting...... Please Wait"):
        try:
            files = {'file':csv_file}
            data = {
                "product_name":product_name,
                "forecast_days":str(forecast_days),
                "current_stock":str(current_stock)
            }
            response = requests.post("http://127.0.0.1:8000/forecast/", data=data, files=files)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed :{e}")
            st.stop()
        
        result = response.json()
        
        if "error" in result:
            st.error(f"ERROR!!!: {result['error']}")
        else:
            st.subheader("Inventory Recommendation")
            st.success(result["recommendation"]["message"])
            
            st.subheader("Model Evaluation")
            metrics = result["metrics"]
            col1, col2, col3 = st.columns(3)
            col1.metric("MAE", f'{metrics["MAE"]:.2f}')
            col2.metric("RMSE", f'{metrics["RMSE"]:.2f}')
            col3.metric("MAPE", f'{metrics["MAPE"]:.2f}%')
            if "Accuracy" in metrics:
                accuracy = metrics["Accuracy"]
            else:
                accuracy = 100 - metrics["MAPE"]
            col4, _, _ = st.columns(3)
            col4.metric("Accuracy", f'{accuracy:.2f}%')

            
            st.subheader('Forecast-Table')
            forecast_df = pd.DataFrame(result["forecast"])
            st.dataframe(forecast_df,use_container_width=True)

            
            csv = forecast_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="forecast_{product_name}.csv">📥 Download Forecast CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

            st.subheader("Forecast with History")
            st.image(base64.b64decode(result["plot_with_history"]))


            st.subheader("Forecast-Only Plot")
            st.image(base64.b64decode(result["plot_forecast_only"]))