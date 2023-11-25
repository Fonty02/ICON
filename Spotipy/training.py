import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def createModel():
    model = {
        'KNN': {'accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0
                },

        'DecisionTree': {'accuracy': 0.0,
                         'precision': 0.0,
                         'recall': 0.0
                         },

        'RandomForest': {'accuracy': 0.0,
                         'precision': 0.0,
                         'recall': 0.0
                         },
        'LogistRegressionMultinomial': {'accuracy': 0.0,
                                        'precision': 0.0,
                                        'recall': 0.0
                                        }
    }

    return model


def saveFoldMetricsInModel(model, y_test, y_pred_knn, y_pred_dtc, y_pred_rfc, y_reg):
    classifiers = ['KNN', 'DecisionTree', 'RandomForest', 'LogistRegressionMultinomial']
    for clf, y_pred in zip(classifiers, [y_pred_knn, y_pred_dtc, y_pred_rfc, y_reg]):
        model[clf]['accuracy'] += metrics.accuracy_score(y_test, y_pred)
        model[clf]['precision'] += metrics.precision_score(y_test, y_pred, average='weighted', zero_division=1)
        model[clf]['recall'] += metrics.recall_score(y_test, y_pred, average='weighted', zero_division=1)
    return model


def trainModelKFold(dataSet, differentialColumn):
    X = dataSet.drop(differentialColumn, axis=1).to_numpy()
    y = dataSet[differentialColumn].to_numpy()
    model = createModel()

    knn = KNeighborsClassifier(n_neighbors=9,algorithm='brute')
    dtc = DecisionTreeClassifier(splitter='best')
    rfc = RandomForestClassifier()
    reg = LogisticRegression(penalty='l2', multi_class='ovr', solver='lbfgs', max_iter=10000)
    kf = RepeatedKFold(n_splits=10, n_repeats=10)
    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        knn.fit(X_train, y_train)
        dtc.fit(X_train, y_train)
        rfc.fit(X_train, y_train)
        reg.fit(X_train, y_train)

        model = saveFoldMetricsInModel(model,
                                       y_test,
                                       knn.predict(X_test),
                                       dtc.predict(X_test),
                                       rfc.predict(X_test),
                                       reg.predict(X_test))

    return model, X_test, y_test, knn, dtc, rfc, reg


def model_report(model):
    dataSet_models = []

    for clf in model:
        dataSet_models.append(pd.DataFrame({'model': [clf],
                                            'accuracy': [np.mean(model[clf]['accuracy'])],
                                            'precision': [np.mean(model[clf]['precision'])],
                                            'recall': [np.mean(model[clf]['recall'])]
                                            }))

    return dataSet_models


def visualizeMetricsGraphs(model, X_test, y_test, knn, dtc, rfc, reg):
    dataSet_models_concat = pd.concat(model_report(
        model), axis=0).reset_index()
    dataSet_models_concat = dataSet_models_concat.drop(
        'index', axis=1)
    print("\n", dataSet_models_concat)

    # Setta la dimensione dell'immagine a 1920x1080 pixel
    plt.figure(figsize=(16, 10))


    # Accuracy
    x = dataSet_models_concat.model
    y = dataSet_models_concat.accuracy

    plt.bar(x, y)
    plt.title("Accuracy")
    plt.show()
    plt.clf()

    plt.figure(figsize=(16, 10))

    # Precision
    x = dataSet_models_concat.model
    y = dataSet_models_concat.precision

    plt.bar(x, y)
    plt.title("Precision")
    plt.show()
    plt.clf()

    plt.figure(figsize=(16, 10))
    # Recall
    x = dataSet_models_concat.model
    y = dataSet_models_concat.recall

    plt.bar(x, y)
    plt.title("Recall")
    plt.show()
    plt.clf()
