# NaiveBayesClassifier
<b>Language:</b> Python<br/>
<b>Description:</b> A Naive Baye's classifier in Python that classifies the hotel reviews as either (deceptive or truthful) and (positive/negative)<br/>
<b>Details:-</b><br/>
Data<br/>
A set of training data will be made available as a compressed ZIP archive. The uncompressed archive will have the following format<br/>
A top-level directory with two sub-directories, one for positive reviews and another for negative reviews (plus license and readme files which we won’t need for the exercise).
Each of the subdirectories contains two sub-directories, one with truthful reviews and one with deceptive reviews.
Each of these subdirectories contains four subdirectories, called “folds”.
Each of the folds contains 80 text files with English text (one review per file).
<br/>
Programs:<br/>
Two programs are written: nblearn.py will learn a naive Bayes model from the training data and nbclassify.py will use the model to classify new data. The learning program will be invoked in the following way:
<br/>
python nblearn.py /path/to/input
<br/>
The argument is the directory of the training data; the program will learn a naive Bayes model, and write the model parameters to a file called nbmodel.txt.<br/>
The classification program will be invoked in the following way:
<br/>
python nbclassify.py /path/to/input
<br/>
The argument is the directory of the test data; the program will read the parameters of a naive Bayes model from the file nbmodel.txt, classify each file in the test data, and write the results to a text file called nboutput.txt in the following format:
<br/>
label_a label_b path1<br/>
label_a label_b path2<br/>
⋮<br/>

In the above format, label_a is either “truthful” or “deceptive”, label_b is either “positive” or “negative”, and pathn is the path of the text file being classified.
