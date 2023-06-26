import tensorflow as tf
import pandas
import json
import numpy as np
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, auc
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.regularizers import l2
from tensorflow.keras.layers import Concatenate
from tensorflow.keras import layers, Model, backend as K
model= None
def loadModel():
    # Recreate the exact same model, including its weights and the optimizer
    global model


    #  create model
    def create_base_network(input_shape):
        input = layers.Input(shape=(input_shape,))
        x = layers.Dense(128, activation='relu')(input)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(64, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(64, activation='relu')(x)
        return Model(input, x)

    def euclidean_distance(vects):
        x, y = vects
        sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
        return K.sqrt(K.maximum(sum_square, K.epsilon()))

    def create_siamese_network(input_shape):
        # Define the tensors for the two input images
        input_1 = layers.Input(shape=(input_shape,))
        input_2 = layers.Input(shape=(input_shape,))

        # Create the base network
        base_network = create_base_network(input_shape)

        # Use the base network to process the inputs
        processed_1 = base_network(input_1)
        processed_2 = base_network(input_2)

        # Compute the Euclidean distance between the two vector outputs
        dist = layers.Lambda(euclidean_distance)([processed_1, processed_2])

        # Add a dense layer with a sigmoid unit to generate the similarity score
        outputs = layers.Dense(1, activation='sigmoid')(dist)

        # Instantiate the model
        siamese_net = Model([input_1, input_2], outputs)
        
        return siamese_net

    model = create_siamese_network(16)
    # load weights into new model
    model.load_weights("/home/anonymous/PycharmProjects/thesisPractical/models/siamese_model.h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
    global history
    with open('/home/anonymous/PycharmProjects/thesisPractical/models/siamese_history.json', 'r') as f:
        history = json.load(f)
def loadTestData():
    data = pandas.read_csv("./codes/semantic.csv")
    data.head()
    data.dropna()
    global x
    global y
    x = data.iloc[0:, 0:32].values.astype("float64")
    y = data.iloc[0:, 32].values.astype("bool")

    from sklearn.model_selection import train_test_split
    global y_test
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=23)
    global x_test_0
    x_test_0 = np.array([x[0:16] for x in x_test])
    global x_test_1
    x_test_1 = np.array([x[16:32] for x in x_test])
def evaluate():


    # Assuming that 'model' is your trained model and 'X_test', 'y_test' are your test data.

    # Predict the probabilities for the test data
    y_pred_prob = model.predict([x_test_0, x_test_1]).ravel()

    # Predict the classes for the test data
    y_pred = np.round(y_pred_prob)

    # Print precision, recall, and F1-score
    print(classification_report(y_test, y_pred))

    # Calculate AUC-ROC
    roc_auc = roc_auc_score(y_test, y_pred_prob)
    print("AUC-ROC:", roc_auc)

    # Calculate ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)

    # Plot ROC curve
    plt.figure()
    lw = 2  # Line width
    plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()
    # Assuming that 'model' is your trained model, and 'history' is the returned History object from model.fit
    # e.g., history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=20)

    # Plot training & validation accuracy values
    plt.figure(figsize=(12,6))
    plt.subplot(1, 2, 1)
    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    # Plot training & validation loss values
    plt.subplot(1, 2, 2)
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.tight_layout()
    plt.show()
def main():
    loadTestData()
    loadModel()
    evaluate()
main()