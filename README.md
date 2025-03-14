# Image Classification: Cats vs Dogs

This project is aimed at classifying images of cats and dogs using machine learning. The goal is to predict whether a new uploaded image is a cat or a dog.

## Table of Contents

- [Project Overview](#project-overview)
- [Tools and Libraries](#tools-and-libraries)
- [Dataset](#dataset)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The project involves using machine learning techniques to classify images of cats and dogs. We use the Histogram of Oriented Gradients (HOG) feature descriptor along with a classifier to make predictions.

## Tools and Libraries

- **Python**: The primary programming language used.
- **skimage**: For image processing tasks.
- **HOG**: For feature extraction.

## Dataset

The dataset used for this project is the [Cats-vs-Dogs Dataset from Kaggle](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-catclassification-dataset).

## Installation

1. **Install Anaconda Environment**:

   - Download and install Miniconda from [here](https://www.anaconda.com/docs/getting-started/miniconda/install).

2. **Set Up PyCharm Interpreter**:
   - Open PyCharm.
   - Press on the interpreter in the bottom right corner.
   - Select `Add New Interpreter` -> `Local Interpreter` -> `Conda`.

## Dependencies

To install the required libraries, run the following commands in your terminal:

```bash
conda install numpy -y
conda install anaconda::matplotlib -y
conda install anaconda::scikit-image -y
```

## Flask & Next JS

### Next JS

> ```
> npm install
> npm run dev
> ```

### Python

Se till så att konsolen står i server mappen kör sedan följande

#### **Mac**

> ```console
> // vet inte vad kommandona är för mac
> py -m venv venv
> py -m pip install flask
> py -m pip install flask-cors
>
> source venv/bin/activate
> py server.py
>
> // Avsluta
> deactivate
> ```

#### **Windows**

> ```console
> py -m venv venv
> py -m pip install flask
> py -m pip install flask-cors
>
> // Kan behöva köras men osäkert, så skippa helst
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
>
> .\venv\Scripts\Activate
> py server.py
>
> // Avsluta
> deactivate
> ```

#### Kommer hostas på den första fria porten _(http://localhost:3000 som standard)_ medan api requesten kommer kunna göras till _http://localhost:8080/api/home_ just nu

### Videos

> - [Intro video](https://www.youtube.com/watch?v=OwxxCibSFKk&t=548s&ab_channel=ArpanNeupane)
> - [Hosting video](https://www.youtube.com/watch?v=LaMVBDbUtMA)
