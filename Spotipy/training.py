import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedKFold, learning_curve, train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier




#Funzione che mostra la curva di apprendimento per ogni modello
def plot_learning_curves(model, X, y, differentialColumn, model_name):
    train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=10, scoring='accuracy')

    # Calcola gli errori su addestramento e test
    train_errors = 1 - train_scores
    test_errors = 1 - test_scores

    # Calcola la deviazione standard e la varianza degli errori su addestramento e test
    train_errors_std = np.std(train_errors, axis=1)
    test_errors_std = np.std(test_errors, axis=1)
    train_errors_var = np.var(train_errors, axis=1)
    test_errors_var = np.var(test_errors, axis=1)

    # Stampa i valori numerici della deviazione standard e della varianza
    print(
        f"\033[95m{model_name} - Train Error Std: {train_errors_std[-1]}, Test Error Std: {test_errors_std[-1]}, Train Error Var: {train_errors_var[-1]}, Test Error Var: {test_errors_var[-1]}\033[0m")

    # Calcola gli errori medi su addestramento e test
    mean_train_errors = 1 - np.mean(train_scores, axis=1)
    mean_test_errors = 1 - np.mean(test_scores, axis=1)

    #Visualizza la curva di apprendimento
    plt.figure(figsize=(16, 10))
    plt.plot(train_sizes, mean_train_errors, label='Errore di training', color='green')
    plt.plot(train_sizes, mean_test_errors, label='Errore di testing', color='red')
    plt.title(f'Curva di apprendimento per {model_name}')
    plt.xlabel('Dimensione del training set')
    plt.ylabel('Errore')
    plt.legend()
    plt.show()



#Funzione che restituisce i migliori iperparametri per ogni modello
def returnBestHyperparametres(dataset, differentialColumn):
    X = dataset.drop(differentialColumn, axis=1).to_numpy()
    y = dataset[differentialColumn].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    dtc = DecisionTreeClassifier()
    rfc = RandomForestClassifier()
    reg = LogisticRegression()
    DecisionTreeHyperparameters = {
        'DecisionTree__criterion': ['gini', 'entropy','log_loss'],
        'DecisionTree__max_depth': [None, 5, 10],
        'DecisionTree__min_samples_split': [2, 5, 10, 20],
        'DecisionTree__min_samples_leaf': [1, 2, 5, 10, 20],
        'DecisionTree__splitter': ['best']}
    RandomForestHyperparameters = {
        'RandomForest__criterion': ['gini', 'entropy','log_loss'],
        'RandomForest__n_estimators': [10, 20,50],
        'RandomForest__max_depth': [None, 5, 10],
        'RandomForest__min_samples_split': [2, 5, 10, 20],
        'RandomForest__min_samples_leaf': [1, 2, 5, 10, 20]}
    LogisticRegressionHyperparameters = {
        'LogisticRegression__C': [0.001, 0.01, 0.1, 1, 10, 100],
        'LogisticRegression__penalty': ['l2'],
        'LogisticRegression__solver': ['liblinear', 'lbfgs'],
        'LogisticRegression__max_iter': [100000,150000]}
    gridSearchCV_dtc = GridSearchCV(Pipeline([('DecisionTree', dtc)]), DecisionTreeHyperparameters, cv=5)
    gridSearchCV_rfc = GridSearchCV(Pipeline([('RandomForest', rfc)]), RandomForestHyperparameters, cv=5)
    gridSearchCV_reg = GridSearchCV(Pipeline([('LogisticRegression', reg)]), LogisticRegressionHyperparameters, cv=5)
    gridSearchCV_dtc.fit(X_train, y_train)
    gridSearchCV_rfc.fit(X_train, y_train)
    gridSearchCV_reg.fit(X_train, y_train)
    bestParameters = {
        'DecisionTree__criterion': gridSearchCV_dtc.best_params_['DecisionTree__criterion'],
        'DecisionTree__max_depth': gridSearchCV_dtc.best_params_['DecisionTree__max_depth'],
        'DecisionTree__min_samples_split': gridSearchCV_dtc.best_params_['DecisionTree__min_samples_split'],
        'DecisionTree__min_samples_leaf': gridSearchCV_dtc.best_params_['DecisionTree__min_samples_leaf'],
        'RandomForest__n_estimators': gridSearchCV_rfc.best_params_['RandomForest__n_estimators'],
        'RandomForest__max_depth': gridSearchCV_rfc.best_params_['RandomForest__max_depth'],
        'RandomForest__min_samples_split': gridSearchCV_rfc.best_params_['RandomForest__min_samples_split'],
        'RandomForest__min_samples_leaf': gridSearchCV_rfc.best_params_['RandomForest__min_samples_leaf'],
        'RandomForest__criterion': gridSearchCV_rfc.best_params_['RandomForest__criterion'],
        'LogisticRegression__C': gridSearchCV_reg.best_params_['LogisticRegression__C'],
        'LogisticRegression__penalty': gridSearchCV_reg.best_params_['LogisticRegression__penalty'],
        'LogisticRegression__solver': gridSearchCV_reg.best_params_['LogisticRegression__solver'],
        'LogisticRegression__max_iter': gridSearchCV_reg.best_params_['LogisticRegression__max_iter']
    }
    return bestParameters



#Funzione che esegue il training del modello mediante cross validation
def trainModelKFold(dataSet, differentialColumn):
    model={
        'DecisionTree':{
            'accuracy_list':[],
            'precision_list':[],
            'recall_list':[],
            'f1':[]
        },
        'RandomForest':{
            'accuracy_list':[],
            'precision_list':[],
            'recall_list':[],
            'f1':[]
        },
        'LogisticRegression':{
            'accuracy_list':[],
            'precision_list':[],
            'recall_list':[],
            'f1':[]
        }
    }
    bestParameters = returnBestHyperparametres(dataSet, differentialColumn)
    #print bestParamestre in blue
    print("\033[94m"+str(bestParameters)+"\033[0m")
    X = dataSet.drop(differentialColumn, axis=1).to_numpy()
    y = dataSet[differentialColumn].to_numpy()
    dtc = DecisionTreeClassifier(criterion=bestParameters['DecisionTree__criterion'],
                                 splitter='best',
                                 max_depth=bestParameters['DecisionTree__max_depth'],
                                 min_samples_split=bestParameters['DecisionTree__min_samples_split'],
                                 min_samples_leaf=bestParameters['DecisionTree__min_samples_leaf'])
    rfc = RandomForestClassifier(n_estimators=bestParameters['RandomForest__n_estimators'],
                                 max_depth=bestParameters['RandomForest__max_depth'],
                                 min_samples_split=bestParameters['RandomForest__min_samples_split'],
                                 min_samples_leaf=bestParameters['RandomForest__min_samples_leaf'],
                                criterion=bestParameters['RandomForest__criterion'])
    reg = LogisticRegression(C=bestParameters['LogisticRegression__C'],
                             penalty=bestParameters['LogisticRegression__penalty'],
                             solver=bestParameters['LogisticRegression__solver'],
                             max_iter=bestParameters['LogisticRegression__max_iter'])
    cv = RepeatedKFold(n_splits=5, n_repeats=5)
    scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
    results_dtc = {}
    results_rfc = {}
    results_reg = {}
    for metric in scoring_metrics:
        scores_dtc = cross_val_score(dtc, X, y, scoring=metric, cv=cv)
        scores_rfc = cross_val_score(rfc, X, y, scoring=metric, cv=cv)
        scores_reg = cross_val_score(reg, X, y, scoring=metric, cv=cv)
        results_dtc[metric] = scores_dtc
        results_rfc[metric] = scores_rfc
        results_reg[metric] = scores_reg
    model['LogisticRegression']['accuracy_list'] = (results_reg['accuracy'])
    model['LogisticRegression']['precision_list'] = (results_reg['precision_macro'])
    model['LogisticRegression']['recall_list'] = (results_reg['recall_macro'])
    model['LogisticRegression']['f1'] = (results_reg['f1_macro'])
    model['DecisionTree']['accuracy_list'] = (results_dtc['accuracy'])
    model['DecisionTree']['precision_list'] = (results_dtc['precision_macro'])
    model['DecisionTree']['recall_list'] = (results_dtc['recall_macro'])
    model['DecisionTree']['f1'] = (results_dtc['f1_macro'])
    model['RandomForest']['accuracy_list'] = (results_rfc['accuracy'])
    model['RandomForest']['precision_list'] = (results_rfc['precision_macro'])
    model['RandomForest']['recall_list'] = (results_rfc['recall_macro'])
    model['RandomForest']['f1'] = (results_rfc['f1_macro'])
    plot_learning_curves(dtc, X, y, differentialColumn, 'DecisionTree')
    plot_learning_curves(rfc, X, y, differentialColumn, 'RandomForest')
    plot_learning_curves(reg, X, y, differentialColumn, 'LogisticRegression')
    visualizeMetricsGraphs(model)
    return model

#Funzione che visualizza i grafici delle metriche per ogni modello
def visualizeMetricsGraphs(model):
    models = list(model.keys())

    # Creazione di un array numpy per ogni metrica
    accuracy = np.array([model[clf]['accuracy_list'] for clf in models])
    precision = np.array([model[clf]['precision_list'] for clf in models])
    recall = np.array([model[clf]['recall_list'] for clf in models])
    f1 = np.array([model[clf]['f1'] for clf in models])

    # Calcolo delle medie per ogni modello e metrica
    mean_accuracy = np.mean(accuracy, axis=1)
    mean_precision = np.mean(precision, axis=1)
    mean_recall = np.mean(recall, axis=1)
    mean_f1 = np.mean(f1, axis=1)

    # Creazione del grafico a barre
    bar_width = 0.2
    index = np.arange(len(models))
    plt.bar(index, mean_accuracy, bar_width, label='Accuracy')
    plt.bar(index + bar_width, mean_precision, bar_width, label='Precision')
    plt.bar(index + 2 * bar_width, mean_recall, bar_width, label='Recall')
    plt.bar(index + 3 * bar_width, mean_f1, bar_width, label='F1')
    # Aggiunta di etichette e legenda
    plt.xlabel('Modelli')
    plt.ylabel('Punteggi medi')
    plt.title('Punteggio medio per ogni modello')
    plt.xticks(index + 1.5 * bar_width, models)
    plt.legend()

    # Visualizzazione del grafico
    plt.show()