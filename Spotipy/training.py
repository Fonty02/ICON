import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedKFold
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve


def createModel():
    model = {
        'DecisionTree': {'accuracy': 0.0,
                         'precision': 0.0,
                         'recall': 0.0,
                         'train_errors': [],
                         'test_errors': []
                         },

        'RandomForest': {'accuracy': 0.0,
                         'precision': 0.0,
                         'recall': 0.0,
                         'train_errors': [],
                         'test_errors': []
                         },
        'LogistRegressionMultinomial': {'accuracy': 0.0,
                                        'precision': 0.0,
                                        'recall': 0.0,
                                        'train_errors': [],
                                        'test_errors': []
                                        }
    }

    return model




def trainModelKFold(dataSet, differentialColumn):
    X = dataSet.drop(differentialColumn, axis=1).to_numpy()
    y = dataSet[differentialColumn].to_numpy()
    dtc = DecisionTreeClassifier(splitter='best')
    rfc = RandomForestClassifier()
    reg = LogisticRegression(penalty='l2', multi_class='ovr', solver='lbfgs', max_iter=10000)
    kf = RepeatedKFold(n_splits=10, n_repeats=10)
    train_sizes_list = []

    train_errors = {'DecisionTree': [], 'RandomForest': [], 'LogisticRegression': []}
    test_errors = {'DecisionTree': [], 'RandomForest': [], 'LogisticRegression': []}

    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Decision Tree
        dtc.fit(X_train, y_train)
        train_errors['DecisionTree'].append(metrics.mean_squared_error(y_train, dtc.predict(X_train)))
        test_errors['DecisionTree'].append(metrics.mean_squared_error(y_test, dtc.predict(X_test)))

        # Random Forest
        rfc.fit(X_train, y_train)
        train_errors['RandomForest'].append(metrics.mean_squared_error(y_train, rfc.predict(X_train)))
        test_errors['RandomForest'].append(metrics.mean_squared_error(y_test, rfc.predict(X_test)))

        # Logistic Regression
        reg.fit(X_train, y_train)
        train_errors['LogisticRegression'].append(metrics.mean_squared_error(y_train, reg.predict(X_train)))
        test_errors['LogisticRegression'].append(metrics.mean_squared_error(y_test, reg.predict(X_test)))

        train_sizes_list.append(len(train_sizes_list) + 1)

    visualizeAverageLearningCurves(train_sizes_list, train_errors, test_errors)


# Funzione per visualizzare la curva di apprendimento media
def plot_average_learning_curve(train_sizes, train_scores_mean, test_scores_mean, title):
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_scores_mean, label='Training error')
    plt.plot(train_sizes, test_scores_mean, label='Validation error')
    plt.title(f'Average Learning Curve - {title}')
    plt.xlabel('Training Examples')
    plt.ylabel('Error')
    plt.legend()
    plt.show()

def visualizeAverageLearningCurves(train_sizes, train_errors, test_errors):
    models = ['DecisionTree', 'RandomForest', 'LogisticRegression']
    for model in models:
        train_sizes_array = np.array(train_sizes)
        train_scores_mean = np.mean(train_errors[model], axis=0)
        test_scores_mean = np.mean(test_errors[model], axis=0)

        plot_average_learning_curve(train_sizes_array, train_scores_mean, test_scores_mean, model)


def model_report(model):
    dataSet_models = []

    for clf in model:
        dataSet_models.append(pd.DataFrame({'model': [clf],
                                            'accuracy': [np.mean(model[clf]['accuracy'])],
                                            'precision': [np.mean(model[clf]['precision'])],
                                            'recall': [np.mean(model[clf]['recall'])]
                                            }))

    return dataSet_models

def visualizeMetricsGraphs(model):
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

    plt.show()