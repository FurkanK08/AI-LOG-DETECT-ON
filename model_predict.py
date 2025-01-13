import sys
import re
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from datetime import datetime
import pytz
import os

def process_log_file(log_file_path):
    regex_pattern = r'^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[\w:/]+\s[+\-]\d{4})\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    columns = ['client', 'userid', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'user_agent']

    log_data = []
    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.match(regex_pattern, line)
            if match:
                log_data.append({
                    'client': match.group('client'),
                    'userid': match.group('userid'),
                    'datetime': match.group('datetime'),
                    'method': match.group('method'),
                    'request': match.group('request'),
                    'status': match.group('status'),
                    'size': match.group('size'),
                    'referer': match.group('referer'),
                    'user_agent': match.group('user_agent')
                })
            else:
                print("Error: Line does not match regex pattern:", line)

    logs_df = pd.DataFrame(log_data, columns=columns)
    return logs_df


def parse_datetime(x):
    try:
        dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
        dt_tz = int(x[-6:-3]) * 60 + int(x[-3:-1])
        return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))
    except ValueError:
        return None


log_file_path = sys.argv[1]  
logs_df = process_log_file(log_file_path)


logs_df['status'] = pd.to_numeric(logs_df['status'], errors='coerce')
logs_df['size'] = pd.to_numeric(logs_df['size'], errors='coerce')


logs_df['datetime'] = logs_df['datetime'].apply(parse_datetime)
logs_df = logs_df.dropna(subset=['datetime'])  # Geçersiz tarihleri çıkarıyoruz
logs_df['datetime'] = pd.to_datetime(logs_df['datetime'], errors='coerce')
logs_df['timestamp'] = logs_df['datetime'].astype('int64') // 10**9


logs_df.drop(columns=['userid'], inplace=True)


logs_df = logs_df.drop_duplicates()


le_request = LabelEncoder()
logs_df['request_encoded'] = le_request.fit_transform(logs_df['request'])

le_client = LabelEncoder()
logs_df['client_encoded'] = le_client.fit_transform(logs_df['client'])


input_features = ['timestamp', 'client_encoded', 'status', 'size', 'request_encoded']
X = logs_df[input_features]


model = load_model('E:/MASAÜSTÜ/Sinir Ağları/WEBAPP/Log_Tahmin/Davranistespiti_model.h5')


scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = np.reshape(X_scaled, (X_scaled.shape[0], X_scaled.shape[1], 1))


predictions = model.predict(X_scaled)


pred_df = pd.DataFrame(predictions[:, :, 0], columns=input_features)

X_scaled_for_inverse = pred_df[['timestamp', 'client_encoded', 'status', 'size', 'request_encoded']]
X_original = scaler.inverse_transform(X_scaled_for_inverse)  


pred_df[['timestamp', 'client_encoded', 'status', 'size', 'request_encoded']] = X_original


pred_df['client'] = le_client.inverse_transform(np.clip(pred_df['client_encoded'].astype(int), 0, len(le_client.classes_) - 1))
pred_df['request'] = le_request.inverse_transform(np.clip(pred_df['request_encoded'].astype(int), 0, len(le_request.classes_) - 1))

pred_df['timestamp'] = pd.to_datetime(pred_df['timestamp'], unit='s')


pred_df.drop(columns=['client_encoded', 'request_encoded'], inplace=True)


output_file_name = f'predicted_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
predict_dir = 'predictions'
if not os.path.exists(predict_dir):
    os.makedirs(predict_dir)
output_file_path = os.path.join(predict_dir, output_file_name)
pred_df.to_csv(output_file_path, index=False)

print(f'Tahminler kaydedildi: {output_file_path}')
