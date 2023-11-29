import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedKFold, learning_curve, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV


def createModel():
    model = {
        'DecisionTree': {'accuracy': 0.0,
                         'precision': 0.0,
                         'recall': 0.0
                         },

        'RandomForest': {'accuracy': 0.0,
                         'precision': 0.0,
                         'recall': 0.0
                         },
        'LogisticRegression': {'accuracy': 0.0,
                                        'precision': 0.0,
                                        'recall': 0.0
                                        }
    }

    return model


def saveFoldMetricsInModel(model, y_test, y_pred_dtc, y_pred_rfc, y_pred_reg):
    model['LogisticRegression']['accuracy_list'] = (
        metrics.accuracy_score(y_test, y_pred_reg))
    model['LogisticRegression']['precision_list'] = (
        metrics.precision_score(y_test, y_pred_reg))
    model['LogisticRegression']['recall_list'] = (
        metrics.recall_score(y_test, y_pred_reg))

    model['DecisionTree']['accuracy_list'] = (
        metrics.accuracy_score(y_test, y_pred_dtc))
    model['DecisionTree']['precision_list'] = (
        metrics.precision_score(y_test, y_pred_dtc))
    model['DecisionTree']['recall_list'] = (
        metrics.recall_score(y_test, y_pred_dtc))

    model['RandomForest']['accuracy_list'] = (
        metrics.accuracy_score(y_test, y_pred_rfc))
    model['RandomForest']['precision_list'] = (
        metrics.precision_score(y_test, y_pred_rfc))
    model['RandomForest']['recall_list'] = (
        metrics.recall_score(y_test, y_pred_rfc))

    return model



def plot_learning_curves(model, X, y, differentialColumn, model_name):
    """
    Calcola la deviazione standard degli errori di addestramento e di test per un modello specifico.

    Parameters:
    - model: Modello addestrato
    - X: Matrice delle feature
    - y: Vettore delle etichette
    - differentialColumn: Colonna differenziale da predire
    - model_name: Nome del modello (es. 'DecisionTree', 'RandomForest', 'LogisticRegression')
    """

    train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=10, scoring='accuracy')

    #Calcola gli errori su addestramento e test
    train_errors = 1 - train_scores
    test_errors = 1 - test_scores

    #Calcola la deviazione standard degli errori su addestramento e test
    train_errors_std = np.std(train_errors, axis=1)
    test_errors_std = np.std(test_errors, axis=1)

    #Stampa i valori numerici della deviazione standard
    print(f"{model_name} - Train Error Std: {train_errors_std[-1]}, Test Error Std: {test_errors_std[-1]}")

    #Calcola gli errori medi su addestramento e test
    mean_train_errors = 1 - np.mean(train_scores, axis=1)
    mean_test_errors = 1 - np.mean(test_scores, axis=1)


    #Visualizza la curva di apprendimento
    plt.figure(figsize=(16, 10))
    plt.plot(train_sizes, mean_train_errors, label='Train Error', color='green')
    plt.plot(train_sizes, mean_test_errors, label='Test Error', color='red')
    plt.title(f'Learning Curve for {model_name}')
    plt.xlabel('Training Set Size')
    plt.ylabel('Error')
    plt.legend()
    plt.show()




def returnBestHyperparametres(dataset, differentialColumn):

    X = dataset.drop(differentialColumn, axis=1).to_numpy()
    y = dataset[differentialColumn].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    dtc = DecisionTreeClassifier()
    rfc = RandomForestClassifier()
    reg = LogisticRegression()
    DecisionTreeHyperparameters = {
        'DecisionTree__max_depth': [None, 5, 10],
        'DecisionTree__min_samples_split': [2, 5, 10, 20],
        'DecisionTree__min_samples_leaf': [1, 2, 5, 10, 20],
        'DecisionTree__max_features': [ 'sqrt', 'log2', None]}
    RandomForestHyperparameters = {
        'RandomForest__n_estimators': [10, 20],
        'RandomForest__max_depth': [None, 5, 10],
        'RandomForest__min_samples_split': [2, 5, 10, 20],
        'RandomForest__min_samples_leaf': [1, 2, 5, 10, 20],
        'RandomForest__max_features': ['sqrt', 'log2', None]}
    LogisticRegressionHyperparameters = {
        'LogisticRegression__C': [0.1, 1, 10, 100, 1000],
        'LogisticRegression__penalty': ['l1', 'l2'],
        'LogisticRegression__solver': ['liblinear'],
        'LogisticRegression__max_iter': [1000,10000]}
    gridSearchCV_dtc = GridSearchCV(Pipeline([('DecisionTree', dtc)]), DecisionTreeHyperparameters, cv=5, n_jobs=-1)
    gridSearchCV_rfc = GridSearchCV(Pipeline([('RandomForest', rfc)]), RandomForestHyperparameters, cv=5, n_jobs=-1)
    gridSearchCV_reg = GridSearchCV(Pipeline([('scaler', StandardScaler()),('LogisticRegression', reg)]), LogisticRegressionHyperparameters, cv=5, n_jobs=-1)
    gridSearchCV_dtc.fit(X_train, y_train)
    gridSearchCV_rfc.fit(X_train, y_train)
    gridSearchCV_reg.fit(X_train, y_train)
    bestParameters = {
        'DecisionTree__max_depth': gridSearchCV_dtc.best_params_['DecisionTree__max_depth'],
        'DecisionTree__min_samples_split': gridSearchCV_dtc.best_params_['DecisionTree__min_samples_split'],
        'DecisionTree__min_samples_leaf': gridSearchCV_dtc.best_params_['DecisionTree__min_samples_leaf'],
        'DecisionTree__max_features': gridSearchCV_dtc.best_params_['DecisionTree__max_features'],
        'RandomForest__n_estimators': gridSearchCV_rfc.best_params_['RandomForest__n_estimators'],
        'RandomForest__max_depth': gridSearchCV_rfc.best_params_['RandomForest__max_depth'],
        'RandomForest__min_samples_split': gridSearchCV_rfc.best_params_['RandomForest__min_samples_split'],
        'RandomForest__min_samples_leaf': gridSearchCV_rfc.best_params_['RandomForest__min_samples_leaf'],
        'RandomForest__max_features': gridSearchCV_rfc.best_params_['RandomForest__max_features'],
        'LogisticRegression__C': gridSearchCV_reg.best_params_['LogisticRegression__C'],
        'LogisticRegression__penalty': gridSearchCV_reg.best_params_['LogisticRegression__penalty'],
        'LogisticRegression__solver': gridSearchCV_reg.best_params_['LogisticRegression__solver'],
        'LogisticRegression__max_iter': gridSearchCV_reg.best_params_['LogisticRegression__max_iter']
    }
    return bestParameters




def trainModelKFold(dataSet, differentialColumn):
    model = createModel()
    bestParameters = returnBestHyperparametres(dataSet, differentialColumn)
    #print bestParamestre in blue
    print("\033[94m"+str(bestParameters)+"\033[0m")

    X = dataSet.drop(differentialColumn, axis=1).to_numpy()
    y = dataSet[differentialColumn].to_numpy()
    dtc = DecisionTreeClassifier(max_depth=bestParameters['DecisionTree__max_depth'],
                                 min_samples_split=bestParameters['DecisionTree__min_samples_split'],
                                 min_samples_leaf=bestParameters['DecisionTree__min_samples_leaf'],
                                 max_features=bestParameters['DecisionTree__max_features'])


    rfc = RandomForestClassifier(n_estimators=bestParameters['RandomForest__n_estimators'], max_depth=bestParameters['RandomForest__max_depth'], min_samples_split=bestParameters['RandomForest__min_samples_split'], min_samples_leaf=bestParameters['RandomForest__min_samples_leaf'], max_features=bestParameters['RandomForest__max_features'])
    reg = LogisticRegression(C=bestParameters['LogisticRegression__C'], penalty=bestParameters['LogisticRegression__penalty'], solver=bestParameters['LogisticRegression__solver'], max_iter=bestParameters['LogisticRegression__max_iter'])
    kf = RepeatedKFold(n_splits=10, n_repeats=10)

    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        #Decision Tree
        dtc.fit(X_train, y_train)

        #Random Forest
        rfc.fit(X_train, y_train)

        #Logistic Regression
        reg.fit(X_train, y_train)

        model = saveFoldMetricsInModel(model, y_test, dtc.predict(X_test), rfc.predict(X_test), reg.predict(X_test))

    plot_learning_curves(dtc, X, y, differentialColumn, 'DecisionTree')
    plot_learning_curves(rfc, X, y, differentialColumn, 'RandomForest')
    plot_learning_curves(reg, X, y, differentialColumn, 'LogisticRegression')

    visualizeMetricsGraphs(model)

    return model







def model_report(model):
    dataSet_models = []
    for clf in model:
        dataSet_models.append(pd.DataFrame({'model': [clf],
                                            'accuracy': [np.mean(model[clf]['accuracy_list'])],
                                            'precision': [np.mean(model[clf]['precision_list'])],
                                            'recall': [np.mean(model[clf]['recall_list'])],
                                            }))

    return dataSet_models




def visualizeMetricsGraphs(model):
    dataSet_models_concat = pd.concat(model_report(
        model), axis=0).reset_index()
    dataSet_models_concat = dataSet_models_concat.drop(
        'index', axis=1)

    #Accuracy
    x = dataSet_models_concat.model
    y = dataSet_models_concat.accuracy

    plt.bar(x, y)
    plt.title("Accuracy")
    plt.show()
    plt.clf()

    #Precision
    x = dataSet_models_concat.model
    y = dataSet_models_concat.precision

    plt.bar(x, y)
    plt.title("Precision")
    plt.show()
    plt.clf()

    #Recall
    x = dataSet_models_concat.model
    y = dataSet_models_concat.recall

    plt.bar(x, y)
    plt.title("Recall")
    plt.show()
    plt.clf()

