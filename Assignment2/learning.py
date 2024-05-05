
import duckdb
import xgboost as xgb


con = duckdb.connect(database='/data/taxi_rides.db')


data = con.execute("SELECT * FROM taxi_rides").fetchdf()


train_data = data.iloc[:10000]
val_data = data.iloc[10000:11000]


params = {
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse'
}


incremental_model = None
batch_model = None


for i in range(10):
    
    incremental_model = xgb.train(params, xgb.DMatrix(train_data), xgb_model=incremental_model)
    
    batch_model = xgb.train(params, xgb.DMatrix(train_data[:10000*(i+1)]))

    
    incremental_preds = incremental_model.predict(xgb.DMatrix(val_data))
    batch_preds = batch_model.predict(xgb.DMatrix(val_data))

    
    incremental_mse = ((val_data['fare_amount'] - incremental_preds) ** 2).mean()
    batch_mse = ((val_data['fare_amount'] - batch_preds) ** 2).mean()

    print(f"Iteration {i+1} - Incremental MSE: {incremental_mse}, Batch MSE: {batch_mse}")
