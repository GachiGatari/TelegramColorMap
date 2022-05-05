from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn import preprocessing
import pickle
le = preprocessing.LabelEncoder()

df = pd.read_excel('data.xlsx', index_col=0,sheet_name="Sheet1")
clf_tree = RandomForestClassifier(n_estimators=10,max_depth=3,min_samples_leaf=10,random_state=78,min_weight_fraction_leaf=0.3)
tree = DecisionTreeClassifier(random_state=67,max_depth=3)
df['Color'] = le.fit_transform(df['Color'])
print(df['Color'])
#df['Color'] = df['Color'].astype(float, errors = 'raise')
clf_tree.fit(df['Color'].values.reshape(-1, 1), df['Map'].values,)
tree.fit(df['Color'].values.reshape(-1, 1), df['Map'].values,)
print(df.columns)
pickle.dump(tree, open('finalized_model.sav', 'wb'))

loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
# print(clf_tree.predict([[1]]))
# print(tree.predict([[7]]))
print(loaded_model.predict([[7]]))