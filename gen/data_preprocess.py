import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def get_data(file): 

    data = pd.read_csv(file)

    feature_raw = data['puzzles']
    label_raw = data['solutions']

    feature = []
    label = []

    for i in feature_raw:
    
        x = np.array([int(j) for j in i]).reshape((9,9,1))
        feature.append(x)
    
    feature = np.array(feature)
    # there are 4 classes
    feature = feature/4
    feature -= .5    
    
    for i in label_raw:
    
        x = np.array([int(j) for j in i]).reshape((81,1)) - 1
        label.append(x)   
    
    label = np.array(label)
    
    del(feature_raw)
    del(label_raw)    

    x_train, x_test, y_train, y_test = train_test_split(feature, label, test_size=0.2, random_state=42)
    
    return x_train, x_test, y_train, y_test
