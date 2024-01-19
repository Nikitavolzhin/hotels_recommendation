# Files
There are 3 .ipynb files in the "model" directory. In study_dataset.ipynb
I explore the dataset to decide how to treat the problem. In problem_solution.ipynb
I train all the essential models for the task and save them(those are .pkl files).
In function.ipynb there is a recommender function which is my solution I will describe later.
The function file is duplicated in the venv directory as function.py. venv directory is
a virtual environment for the project. There are 3 files for the server side of the side.
The client part of the site files (.html/.css files) are located in templates and static directories
NB: due the weight of the dataset I did not upload it on GitHub, but it can be accessed by the link
https://drive.google.com/file/d/1wYW_pLEEFluEejgkg_I2emxLjy9YZ5GG/view?usp=share_link
# About the dataset
Different hotels have completely different representations in the dataset
(some hotels are represented less than 50 times, while others over 15 000 times).
To save this proportionality in the training sets I use Stratified split and split the data into 40 sets
because the dataset is huge (over 500 000 observations). Among all the columns most useful,
which I will use in my solution, are positive review, negative review, and average score.
# Preprocessing
Obviously, no machine learning model takes the raw text and gives meaningful results out of it. So I had
to preprocess both negative and positive reviews (I did it in the same way for both). First I noticed that
the text already lacks commas, dots, etc. so punctuation is already removed. Next, I set all the letters to
lowercase. Next, I remove "stopwords", such as "the", "is" etc., which do not have any meaning. NB: here I
kept "not", because it still can be helpful. Then, I did stemming (PorterStemmer), which is considering same-root words
as the same word (indeed "lovely staff" and "I loved the staff" are similar). Then I apply scikit-learn CountVectorizer, which turns each review into
a vector. So I used, the so-called, "Bag of Words" model, where each position in the vector corresponds to a word, while
the number standing on this position shows the number of times the word is encountered in the review. This model
is simple, but it is sufficient for this task because looking for complicated word relations and the meaning of the sentences is
not required. If a guest likes for instance "large windows, quiet place, and kind staff" the model will get it.
# Solution
After some consideration, I decided to treat this problem as a classification with 1492 labels (i.e. hotels).
Since a positive review is similar to what a user searching for a hotel wants to see, I used a positive review
as an independent variable for hotel prediction. Notice, that I predict not a single but 50 hotels from one prompt because
that is how recommending systems work(suggesting multiple items). To do it, I predict the probabilities of each hotel and select
the 50 most probable. Thus, I selected only among probabilistic models. I chose SGDClassifier. And here is one pleasant bonus, 
it supports batch learning which will allow me to feed a large part of the dataset until the model starts overfitting. I kept
default hyperparameters because they were OK. I trained two models: one for positive, and one for negative reviews. Then I ask the user
what they want to have and what to avoid, applying a positive review model on what they want and negative on what they want to avoid. 
Then I take the 50 most probable hotels and remove the ones that predicted the negative model. On the site, I implemented filtering
by the minimum score.
# Site
I decided to create a simple site as an interface to interact with the model. For this, I used Flask(because I am not a web developer and
apparently Flask was the simplest to use). The site consists of two pages: one with 3 fields asking the user what they want, don't want,
and min. score. After this form is filled out the site redirects the user to the page showing the recommended hotels, their score, and 3
positive reviews below each of them.
