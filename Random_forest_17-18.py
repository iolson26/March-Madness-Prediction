import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

game_data = pd.read_csv("stats17-18 game data.csv")
game_data.head()
game_data = game_data.drop(columns=["GameID", "Date", "Year", "Home_team", "Away_Team", "Away_Winner?"])


x, y = game_data.loc[:, (game_data.columns != "Home_winner?")], game_data["Home_winner?"]

xtrain, xtest, ytrain, ytest = train_test_split(x,y, test_size=.2, random_state=42)
xtrain, xval, ytrain, yval = train_test_split(xtrain,ytrain, test_size=.25, random_state=42)

label_encoder = LabelEncoder()
ytrain = label_encoder.fit_transform(ytrain)
yval   = label_encoder.transform(yval)
ytest  = label_encoder.transform(ytest)


scaler = StandardScaler()
xtrain = scaler.fit_transform(xtrain)
xval = scaler.transform(xval)
xtest = scaler.transform(xtest)


rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(xtrain,ytrain)

ypred = rf_model.predict(xval)

test_accuracy = accuracy_score(yval, ypred)
print(f"Test_Accuracy: {test_accuracy: .3f}")
print("\nClasification Report:\n", classification_report(yval,ypred))
print("\nConfusion Matrix:\n", confusion_matrix(yval,ypred))


#Feature Importance Graph
'''
feature_importance = rf_model.feature_importances_
feature_names = x.columns

sort_indices = np.argsort(feature_importance)[::-1]
plt.figure(figsize=(10,5))
plt.bar(range(len(feature_importance)), feature_importance[sort_indices], align="center")
plt.xticks(range(len(feature_importance)), np.array(feature_names)[sort_indices], rotation=90)
plt.ylabel("Feature Importance")
plt.title("Random Forest Feature Importance")
plt.show()
'''
#Hyperparameter Tuning Stuff
#Change 'gridsearch' to 'randomsearch'
'''
param_grid = {
    'n_estimators': [10,100,200,300],
    'max_depth': [3,5,10,20,None],
    'max_features': ['sqrt','log2',None],
    'min_samples_leaf': [1,2,4],
    'bootstrap': [True,False]
}
rf_model = RandomForestClassifier(random_state=42)
gridsearch = GridSearchCV(rf_model, param_grid, cv=10, scoring='accuracy', n_jobs=-1, verbose=2)
gridsearch.fit(xtrain,ytrain)

best_rf = gridsearch.best_estimator_


print("Best Parameters", gridsearch.best_params_)
print("Best Score", gridsearch.best_score_)
'''

#Best Parameters {'bootstrap': False, 'max_depth': 20, 'max_features': 'sqrt', 'min_samples_leaf': 2, 'n_estimators': 100}
#Best Score 0.7709200290426306