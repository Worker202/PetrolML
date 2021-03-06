
import numpy as np
import pandas as pd
from keras.models import model_from_json
import pickle
def predict_point_by_point(model, number):
    # Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    sc = pickle.load(open("MinMaxScaler.dat", "rb"))
    value = sc.transform([[number]])
    value = np.reshape(value, (len(value), 1, 1))
    predicted = model.predict(value)
    print("Predicted", predicted)
    predicted= sc.inverse_transform(predicted)
    print("transformed",predicted)
    return predicted
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
regressor = loaded_model
df = pd.read_csv('DelhiPrice.csv')
df['date'] = pd.to_datetime(df['Timestamp'], unit='s').dt.date
group = df.groupby('date')
Real_Price = group['Weighted_Price'].mean()
value= Real_Price[-1]
print("Input is",value)
predict_point_by_point(regressor, value)
