from data_preprocessing import create_data_generators
from model_building import build_model
import matplotlib.pyplot as plt

def main():
    # Skapa datageneratorer
    train_generator, validation_generator = create_data_generators('trainingdata')

    # Bygg och träna modellen
    model = build_model()

    # Träna modellen
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        epochs=25,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size
    )

    # Utvärdera modellen
    test_loss, test_acc = model.evaluate(validation_generator)
    print(f'Test accuracy: {test_acc}')

    # Visualisera träningshistoriken
    plot_training_history(history)


def plot_training_history(history):
    # Visualisera träningskurvor
    plt.figure(figsize=(12, 6))

    # Tränings- och valideringskurvor för förlust
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Träningsförlust')
    plt.plot(history.history['val_loss'], label='Valideringsförlust')
    plt.title('Förlust per epok')
    plt.xlabel('Epok')
    plt.ylabel('Förlust')
    plt.legend()

    # Tränings- och valideringskurvor för noggrannhet
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Träningsnoggrannhet')
    plt.plot(history.history['val_accuracy'], label='Valideringsnoggrannhet')
    plt.title('Noggrannhet per epok')
    plt.xlabel('Epok')
    plt.ylabel('Noggrannhet')
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()