import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout, Lambda
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
import pandas
import numpy as np
import pickle as pk
import sklearn as sk
data = None
x = None
y = None
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

def loadtrainingdata():
    global data
    data = pandas.read_csv("./codes/semantic.csv")
    data.head()
    data.dropna()
    global x
    global y
    x = data.iloc[0:, 0:32].values.astype("float64")
    y = data.iloc[0:, 32].values.astype("bool")
def trainSiamese(l=0.0001, e=60):
    tf.random.set_seed(1210)
    tf.keras.backend.clear_session()
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=23)
    x_train_0 = np.array([x[0:16] for x in x_train])
    x_train_1 = np.array([x[16:32] for x in x_train])
    x_test_0 = np.array([x[0:16] for x in x_test])
    x_test_1 = np.array([x[16:32] for x in x_test])

    print(x_train_0.shape)
    from tensorflow.keras.regularizers import l2
    from tensorflow.keras.layers import Concatenate
    from tensorflow.keras import layers, Model, backend as K

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
    model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=l), metrics=['accuracy'])
    history = model.fit([x_train_0,x_train_1], y_train,validation_data=([x_test_0,x_test_1],y_test), epochs=e)

    model.save_weights('/home/anonymous/PycharmProjects/thesisPractical/models/siamese_model.h5') 
    import json
    # The history object has a dictionary in its history attribute
    history_dict = history.history

    # You can save this dictionary as a json object
    with open('/home/anonymous/PycharmProjects/thesisPractical/models/siamese_history.json', 'w') as f:
        json.dump(history_dict, f)

def trainmodel(l=0.001, e=60):
    trainSiamese(l,e)
def main():
    loadtrainingdata()
    trainmodel()

main()