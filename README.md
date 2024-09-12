# Speaker Identification

This project focuses on building a machine learning model to identify speakers using the RAVDESS (Ryerson Audio-Visual Database of Emotional Speech and Song) dataset.

## Setup and Dependencies

To run this project, you need the following dependencies:

- `librosa`
- `soundfile`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `seaborn`

## Data Augmentation

The project includes functions to augment audio data by applying time stretching, pitch shifting, and adding noise.

## Feature Extraction

The project extracts various audio features such as MFCCs, chroma, mel spectrogram, zero-crossing rate, spectral contrast, and tonnetz.

## Data Loading and Preprocessing

The dataset is loaded, features are extracted, and the data is split into training and testing sets.

## Model Training and Evaluation

A Multi-Layer Perceptron (MLP) classifier is used for speaker identification. The model is trained, and its accuracy is evaluated using a confusion matrix and classification report.

## Hyperparameter Tuning

Grid search is used for hyperparameter tuning to find the best model parameters.

## Feature Visualization

The project includes functionality to visualize MFCC features.

## Conclusion

This project demonstrates the process of building a speaker identification system using the RAVDESS dataset, covering data augmentation, feature extraction, model training, evaluation, hyperparameter tuning, and feature visualization.

## Usage

1. Mount your Google Drive to access the dataset.
2. Unzip the dataset.
3. Run the Jupyter Notebook to train and evaluate the model.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The RAVDESS dataset creators.
- The open-source community for providing useful libraries and tools.
