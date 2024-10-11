# Chapter 16: Evaluation, monitoring and feedback loop

import numpy as np
from sklearn.neural_network import MLPClassifier

import mlflow
import mlflow.sklearn
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

if __name__ == "__main__":
    X, y = make_classification(random_state=42, n_classes=2)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    experiment = "MyExperimentMLFlow"
    mlflow.create_experiment(experiment)
    mlflow.set_experiment(experiment)

    my_clf = MLPClassifier(max_iter=1000).fit(X_train, y_train)

    with mlflow.start_run():
        my_clf.fit(X, y)
        mlflow.log_param("mlflow_hidden_layer_sizes", my_clf.hidden_layer_sizes)
        mlflow.log_param("mflow_activation", my_clf.activation)
        mlflow.log_artifacts("./model")

        fig, ax = plt.subplots()
        ax.plot(my_clf.loss_curve_)
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Training loss")

        mlflow.log_figure(fig, "plot_loss_curve.png")
        mlflow.log_metric("score", my_clf.score(X_test, y_test))


