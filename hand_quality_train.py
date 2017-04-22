import csv
import numpy as np
from sklearn.cross_validation import train_test_split
import random

import keras
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Flatten, Dense, Dropout, Activation
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import Nadam
from keras.preprocessing import image

def get_rank(rank):
    return ['2','3','4','5','6','7','8','9','10','J','Q','K','A'].index(rank)
    
def get_suit(suit):
    return ['diamonds','spades','hearts','clubs'].index(suit)

def get_card_id(hand,i):
    return (get_rank(hand[2*i]), get_suit(hand[2*i+1]))

def get_cards(hand):
    cards = np.zeros((13,4))
    for i in range(random.randint(3,5)):
        cards[get_card_id(hand,i)] = 1
    for i in range(5,7):
        cards[get_card_id(hand,i)] = 1
    return cards

def get_hand(hand):
    return (get_cards(hand), int(hand[14]))


hands = []
results = []
with open('/data/poker/winner_cards.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None) 
    for hand in reader:
        if len(hand)==15:
            h = get_hand(hand)
            if int(h[1]) == 1 or random.randint(0,4) == 0:
                hands.append(h[0])
                results.append(h[1])
        
raw = np.asarray(hands).reshape((len(hands),13,4,1))

X_train, X_test, y_train, y_test = train_test_split(raw, results, test_size = 0.2)

model = Sequential([
    ZeroPadding2D(padding=(2, 0), input_shape=(13, 4, 1)),
    Convolution2D(10,5,4, border_mode='valid', activation='relu'),
    Flatten(),
    Dense(20, activation='relu'),
    Dense(1),
    Activation('sigmoid')
])

opt = Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.006)
model.compile(optimizer=opt,loss='binary_crossentropy', metrics=['accuracy'])

train_generator = image.ImageDataGenerator().flow(X_train, y_train)
test_generator = image.ImageDataGenerator().flow(X_test, y_test)

model.fit_generator(
       train_generator, 
       samples_per_epoch=len(y_train),
       nb_epoch=2, 
       validation_data=test_generator, 
       nb_val_samples=len(y_test)
   )

model.save_weights('/data/trained_models/poker/lean_poker_hand_quality_v1.h5')