from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_data_generators(base_dir, target_size=(150, 150), batch_size=32, validation_split=0.2):
    """
    Skapar tränings- och valideringsdatageneratorer.
    """
    # Skapa en ImageDataGenerator för att förbehandla bilder
    datagen = ImageDataGenerator(rescale=1./255, validation_split=validation_split)

    # Träningsgenerator
    train_generator = datagen.flow_from_directory(
        base_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary',
        subset='training'
    )

    # Valideringsgenerator
    validation_generator = datagen.flow_from_directory(
        base_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary',
        subset='validation'
    )

    return train_generator, validation_generator
