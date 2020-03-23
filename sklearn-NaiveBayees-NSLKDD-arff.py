from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from scipy.io.arff import loadarff
import numpy as np


KDDTrain, train_metadata = loadarff("KDDTrain+.arff")
KDDTest, test_metadata = loadarff("KDDTest+.arff")

# Preprocess
enc = preprocessing.OrdinalEncoder()
training_nparray = np.asarray(KDDTrain.tolist())  # This is necessary to correctly shape the array
encoded_dataset = enc.fit_transform(training_nparray)  # All categorical features are now numerical

X_train = encoded_dataset[:, :-1]  # All rows, omit last column
y_train = np.ravel(encoded_dataset[:, -1:])  # All rows, only the last column


testing_nparray = np.asarray(KDDTest.tolist())
encoded_dataset = enc.fit_transform(testing_nparray)
X_test = encoded_dataset[:, :-1]
y_test = np.ravel(encoded_dataset[:, -1:])


gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)

total_datapoints = X_test.shape[0]
mislabeled_datapoints = (y_test != y_pred).sum()
correct_datapoints = total_datapoints-mislabeled_datapoints
percent_correct = (correct_datapoints / total_datapoints) * 100

print("Total datapoints: %d\nCorrect datapoints: %d\nMislabeled datapoints: %d\nPercent correct: %.2f%%"
      % (total_datapoints, correct_datapoints, mislabeled_datapoints, percent_correct))
