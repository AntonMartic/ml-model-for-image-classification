from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


def build_model(input_shape=(150, 150, 3)):
    """
    Bygger en CNN-modell för binär klassificering.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # Sigmoid för binär klassificering
    ])

    # Kompilera modellen
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model
