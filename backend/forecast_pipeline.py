from prophet import Prophet
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from io import BytesIO
import traceback
import base64

# 1. Prepare data for selected product
def prepare_product_data(df, product_name):
    store_to_product_map = {
        'milk': [1],
        'bread': [2],
        'fruits': [3],
        'snacks': [4],
        'detergent': [5]
    }

    product_name = product_name.lower()
    if product_name not in store_to_product_map:
        raise ValueError(f"Unknown product '{product_name}'. Valid options are: {list(store_to_product_map.keys())}")

    store_ids = store_to_product_map[product_name]
    product_df = df[df['Store'].isin(store_ids)].copy()

    # Convert weekly to daily by forward filling same sales for each weekday (simple assumption)
    product_df['Date'] = pd.to_datetime(product_df['Date'])
    product_df = product_df.set_index('Date').resample('D').ffill().reset_index()

    daily_df = product_df.groupby('Date')['Weekly_Sales'].sum().reset_index()
    daily_df.columns = ['ds', 'y']

    return daily_df.sort_values('ds')

# 2. Prepare holiday DataFrame
def get_holidays(df):
    if 'Holiday_Flag' not in df.columns:
        return None

    df['Date'] = pd.to_datetime(df['Date'])
    holiday_dates = df[df['Holiday_Flag'] == 1]['Date'].unique()
    holidays = pd.DataFrame({
        'holiday': 'holiday',
        'ds': pd.to_datetime(holiday_dates),
        'lower_window': 0,
        'upper_window': 1
    })
    return holidays

# 3. Train Prophet model
def train_prophet_model(df, holidays_df=None):
    model = Prophet(holidays=holidays_df,changepoint_prior_scale=0.3, seasonality_mode='multiplicative' )
    model.fit(df)
    return model

# 4. Forecast function
def forecast_sales(model, n_days):
    future = model.make_future_dataframe(periods=n_days, freq='D')
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# 5. Evaluate forecast accuracy
def evaluate_model(test_df, forecast_df):
    merged = test_df.merge(forecast_df, on='ds')
    if merged.empty:
        raise ValueError("No overlapping dates between test data and forecast. Check date alignment.")
    actual = merged['y']
    predicted = merged['yhat']
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    accuracy = 100 - mape
    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2),
        "ACCURACY":round(accuracy,2)
    }

# 6. Generate both plots
def generate_forecast_plot(forecast_df, product_name, original_df=None, include_history=True):
    plt.figure(figsize=(10, 5))

    if include_history and original_df is not None:
        # Plot historical data
        plt.plot(original_df['ds'], original_df['y'], label='Historical Sales', color='black')

    # Plot forecast
    plt.plot(forecast_df['ds'], forecast_df['yhat'], label='Forecasted Sales', color='blue')
    plt.fill_between(forecast_df['ds'], forecast_df['yhat_lower'], forecast_df['yhat_upper'], alpha=0.2)

    title = f"{product_name.capitalize()} – Forecast {'with History' if include_history else 'Only'}"
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()

    return base64.b64encode(buf.getvalue()).decode("utf-8")

# 7. Inventory recommendation
def recommend_stock_action(forecast_df, current_stock):
    total_demand = forecast_df['yhat'].sum()
    diff = int(total_demand - current_stock)
    if diff > 0:
        return {"status": "reorder", "units": diff, "message": f"You need to reorder {diff} units."}
    elif diff < -30:
        return {"status": "excess", "units": abs(diff), "message": f"You have {abs(diff)} excess units."}
    else:
        return {"status": "balanced", "units": 0, "message": "Stock level is sufficient."}

# 8. Main pipeline
def forecast_for_product(df, product_name, forecast_days, current_stock):
    try:
        holidays_df = get_holidays(df)
        product_df = prepare_product_data(df, product_name)

        if len(product_df) < 30:
            raise ValueError("Not enough historical data. Minimum 30 days required.")
        
        test_days = min(30,forecast_days)
        
        train_df = product_df[:-test_days][['ds', 'y']].copy()
        test_df = product_df[-test_days:][['ds', 'y']].copy()

        
        model_evaluation = train_prophet_model(train_df,holidays_df)
        forecast_evaluation = forecast_sales(model_evaluation,test_days)
        metrics = evaluate_model(test_df,forecast_evaluation)

        final_model = train_prophet_model(product_df, holidays_df)
        full_forecast = forecast_sales(final_model, forecast_days)

        forecast_tail = full_forecast.tail(forecast_days).copy()
        plot_with_history = generate_forecast_plot(full_forecast, product_name, product_df, include_history=True)
        plot_forecast_only = generate_forecast_plot(full_forecast[full_forecast['ds'] > product_df['ds'].max()], product_name, include_history=False)

        recommendation = recommend_stock_action(forecast_tail, current_stock)

        return {
            "forecast": forecast_tail.to_dict(orient='records'),
            "metrics":metrics,
            "plot_with_history": plot_with_history,
            "plot_forecast_only": plot_forecast_only,
            "recommendation": recommendation
        }
    except Exception as e:
        return {
            "error": f"{str(e)}\n{traceback.format_exc()}",
            "forecast": [],
            "plots": {},
            "recommendation": {"message": "Error occurred. Please check inputs."}
        }

# 9. CLI test block
if __name__ == "__main__":
    df = pd.read_csv("data/Walmart_Sales.csv")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    product = "snacks"
    forecast_days = 14
    current_stock = 5000000

    result = forecast_for_product(df, product, forecast_days, current_stock)

    if 'error' in result:
        print("❌ Error occurred:", result['error'])
    else:
        print("📦 Inventory Advice:", result['recommendation']['message'])
        
        print("Evaluatoin metrics:")
        for key,value in result['metrics'].items():
            print(f"{key}:{value}")

        with open("forecast_with_history.png", "wb") as f:
            f.write(base64.b64decode(result['plot_with_history']))

        with open("forecast_only.png", "wb") as f:
            f.write(base64.b64decode(result['plot_forecast_only']))
