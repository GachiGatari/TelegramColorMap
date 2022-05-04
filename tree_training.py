from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn import preprocessing
import pickle
le = preprocessing.LabelEncoder()
# #
# df = pd.read_excel('data.xlsx', index_col=0,sheet_name="Sheet1")
# clf_tree = RandomForestClassifier(n_estimators=10,max_depth=3,min_samples_leaf=14,random_state=45,min_weight_fraction_leaf=0.3)
# df['Color'] = le.fit_transform(df['Color'])
# print(df['Color'])
# #df['Color'] = df['Color'].astype(float, errors = 'raise')
# clf_tree.fit(df['Color'].values.reshape(-1, 1), df['Map'].values,)


loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
print(loaded_model.predict([[9]]))
