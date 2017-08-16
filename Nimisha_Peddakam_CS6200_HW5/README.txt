Steps to compile and run the code
---------------------------------

-Code for training the data set is present in train.py
-It expects two command line arguments: the absolute path to textcat directory(Ex: F:\textcat\textcat) and the name of the model file with .json extension(model.json).
-After running train.py, it generated model file in the path which was provided by the first command line argument.(F:\textcat\textcat).

-Code for classifying is present in test.py
-It expects 3 command line arguments: path to the model file(Ex: F:\textcat\textcat\model.json), path to the location where files to be classified are present(Ex: F:\textcat\textcat\dev\neg) and path where the predictions file should be generated along with the name of the predictions file with .txt extension(Ex: F:\textcat\textcat\predictions.txt).

-Two files 'NegativeTo_Positive_Weight.txt' and 'Positive_To_Negative_Weight.txt' are generated, in the same directory where the code is placed and run, which have top 20 terms with highest negative to positive and positive to negative ratio respectively. 

Percentage of positive and negative reviews in the development data classified correctly:
dev/neg
Accuracy-- Negative: 75 Positive: 25
dev/pos
Accuracy-- Negative: 25 Positive: 75