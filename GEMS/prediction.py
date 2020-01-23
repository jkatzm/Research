from subject_info import *

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, mean_squared_error

# get data
cfb_dict = load_obj("current_flow_betweenness")
X = np.copy(dict_to_features(cfb_dict, subject_ids))
y = np.copy(list(penn_df['COG_ACC_MEAN']))

# scale the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/7)

# fit model
reg = LinearRegression()
reg.fit(X_train, y_train)

# prediction outcome
y_pred = reg.predict(X_test)

print("R^2: {}".format(reg.score(X_test, y_test)))
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("Root Mean Squared Error: {}".format(rmse))