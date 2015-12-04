# -*- coding: utf-8 -*-

"""This module contains functions for making plots relevant to regressors."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import matplotlib.pyplot as plt
import seaborn.apionly as sns

from regressors import stats
from regressors.regressors import supported_linear_models


def plot_residuals(clf, X, y, r_type='standardized', figsize=(10, 8)):
    """Plot residuals of a linear model.

    Parameters
    ----------
    clf : sklearn.linear_model
        A scikit-learn linear model classifier with a `predict()` method.
    X : numpy.ndarray
        Training data used to fit the classifier.
    y : numpy.ndarray
        Target training values, of shape = [n_samples].
    r_type : str
        Type of residuals to return: ['raw', 'standardized', 'studentized'].
        Defaults to 'standardized'.

        * 'raw' will return the raw residuals.
        * 'standardized' will return the Pearson standardized residuals, also
          known as internally studentized residuals, which is calculated as the
          residuals divided by the square root of MSE (or the STD of the
          residuals).
        * 'studentized' will return the externally studentized residuals, which
          is calculated as the raw residuals divided by sqrt(LOO-MSE * (1 -
          leverage_score)).
    figsize : tuple
        A tuple indicating the size of the plot to be created, with format
        (x-axis, y-axis). Defaults to (10, 10).

    Returns
    -------
    matplotlib.figure.Figure
        The Figure instance.
    """
    # Ensure we only plot residuals using classifiers we have tested
    assert isinstance(clf, supported_linear_models), (
        "Classifiers of type {} not currently supported.".format(type(clf)))
    # Set plot style
    sns.set_style("whitegrid")
    sns.set_context("talk")  # Increase font size on plot
    # Get residuals or standardized residuals
    resids = stats.residuals(clf, X, y, r_type)
    predictions = clf.predict(X)
    # Generate residual plot
    y_label = {'raw': 'Residuals', 'standardized': 'Standardized Residuals',
               'studentized': 'Studentized Residuals'}
    try:
        fig = plt.figure('residuals', figsize=figsize)
        plt.scatter(predictions, resids, s=14, c='gray', alpha=0.7)
        plt.hlines(y=0, xmin=predictions.min(),
                   xmax=predictions.max(), linestyle='dotted')
        plt.title("Residuals Plot")
        plt.xlabel("Predictions")
        plt.ylabel(y_label[r_type])
        plt.show()
    except:
        raise  # Re-raise the exception
    finally:
        sns.reset_orig()  # Always reset back to default matplotlib styles
    return fig