from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
import numpy as np
import pandas as pd


def trainModel():
    # initializing of embedding & recognizer
    embeddingFile = "output/embeddings.pickle"
    # New & Empty at initial
    recognizerFile = "output/recognizer.pickle"
    labelEncFile = "output/le.pickle"

    print("Loading face embeddings...")
    data = pickle.loads(open(embeddingFile, "rb").read())
    # print(data['names'])
    # print(data['embeddings'])
    print("Encoding labels...")
    labelEnc = LabelEncoder()
    labels = labelEnc.fit_transform(data["names"])

    print("Training model...")
    # data["embeddings"]=[int(x) for x in data["embeddings"]]
    # data["embeddings"]=np.array(data["embeddings"])
    # data["embeddings"]=data['embeddings'].astype(int)
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["embeddings"], labels)

    f = open(recognizerFile, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    f = open(labelEncFile, "wb")
    f.write(pickle.dumps(labelEnc))
    f.close()
    print('process completed')
