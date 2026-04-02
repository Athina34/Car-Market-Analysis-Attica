# Car Market Analysis in Attica (2021–2026) & Price Prediction

## Overview

This repository contains the implementation of a thesis project focused on the **used car market in Attica, Greece**, covering the period **2021–2026**. The main objective is to analyze the factors that influence used car prices and to develop a **machine learning model for price prediction**.

The project follows a reproducible data science workflow in Python, combining:

- data cleaning and validation
- exploratory data analysis (EDA)
- feature engineering
- predictive modeling
- model evaluation and interpretation

---

## Thesis Objective

The central goal of the study is to investigate the determinants of used car prices in Attica and to build a reliable predictive model based on vehicle and market characteristics.

More specifically, the project examines the role of variables such as:

- **Technical characteristics**: engine displacement, horsepower, fuel type, transmission
- **Usage-related variables**: mileage, age, registration year
- **Market characteristics**: manufacturer, model, body type, listing features
- **Geographical information**: regional variation within Attica

---

## Project Status

The project currently includes the following completed stages:

- **Notebook 1:** data cleaning review and exploratory data analysis
- **Notebook 2:** predictive modeling and model comparison
- creation of cleaned and model-ready datasets
- export of model evaluation outputs in `data/processed/`

The next planned stage is:

- **Notebook 3:** model evaluation, hyperparameter tuning, error analysis, and interpretability

---

## Research Goals

The project is structured around the following goals:

1. Create and organize a structured dataset of car listings in Attica.
2. Clean and preprocess the raw data for analytical use.
3. Explore market patterns through descriptive statistics and visualizations.
4. Identify the variables most strongly associated with price.
5. Develop and evaluate machine learning models for price prediction.
6. Document the full workflow in a reproducible and academically structured way.

---

## Dataset

The project is based on vehicle listings from the Attica region.

- The **initial raw dataset** contained more than **12,000 listings**.
- After cleaning and preparation, the **cleaned analytical dataset** contains **8,933 observations**.
- A separate **model-ready dataset** was created for the predictive modeling stage.

### Main Variables

Key variables used in the analysis include:

- `Κατασκευαστής` / Make
- `Τύπος` / Model
- `Εγγραφή` / Registration year
- `Καύσιμο` / Fuel type
- `Χιλιόμετρα` / Mileage
- `Κυβικά` / Engine displacement
- `Ιπποδύναμη` / Horsepower
- `Μετάδοση` / Transmission
- `Περιοχή` / Region
- `Τιμή` / Price (**target variable**)

### Data Preparation

The initial version of the dataset was organized in spreadsheet form and then processed through Python scripts and notebooks for:

- standardization of column names
- missing value inspection
- duplicate checks
- data type correction
- category normalization
- creation of cleaned and model-ready datasets

---

## Methodology

The methodological workflow of the project consists of the following stages:

### 1. Data Collection and Organization
- Collection and structuring of raw vehicle listing data
- Creation of the initial raw dataset in spreadsheet format

### 2. Data Cleaning and Preprocessing
- Handling missing values and inconsistent records
- Duplicate detection and review
- Standardization of categories and formats
- Data quality checks
- Preparation of cleaned datasets for analysis and modeling

### 3. Exploratory Data Analysis (EDA)
- Descriptive statistics
- Distribution analysis of price, mileage, and technical features
- Market segmentation by fuel type, manufacturer, registration year, and region
- Visualization of relationships between vehicle characteristics and price

### 4. Feature Engineering
- Selection of relevant predictors
- Transformation of variables where needed
- Encoding of categorical variables
- Construction of model-ready input tables

### 5. Predictive Modeling
The project evaluates machine learning models for used car price estimation, including:

- Dummy Regressor
- Linear Regression
- Ridge Regression
- Random Forest
- XGBoost

### 6. Model Evaluation
Models are assessed using standard regression metrics:

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**

Residual analysis and model comparison are also used to support the final model selection.

---

## Current Modeling Results

In the first completed modeling stage, multiple regression models were compared on the test set.

The best overall performance was achieved by **XGBoost**, while **Random Forest** also showed strong predictive performance.

Exported results currently include:

- `data/processed/model_comparison_results.csv`
- `data/processed/best_model_test_predictions.csv`

These files support the reproducibility of the modeling stage and can be used in subsequent analysis and reporting.

---

## Technologies and Tools

The project is implemented in **Python 3.x** using the following libraries:

- **Pandas** – data manipulation
- **NumPy** – numerical computation
- **Matplotlib** – visualization
- **Seaborn** – statistical plotting
- **Scikit-learn** – preprocessing, modeling, and evaluation
- **XGBoost** – gradient boosting regression
- **SHAP** – model interpretability
- **Streamlit** *(optional)* – future dashboard or presentation layer

---

## Repository Structure

```text
Car-Market-Analysis-Attica/
│
├── .github/
│   └── workflows/                      # GitHub Actions workflow
│
├── data/
│   ├── raw/                            # Raw input files (kept locally / not necessarily tracked)
│   └── processed/                      # Cleaned datasets and modeling exports
│       ├── cleaned_car_data.csv
│       ├── ml_ready_car_data.csv
│       ├── model_comparison_results.csv
│       └── best_model_test_predictions.csv
│
├── logs/                               # Research logs and activity notes
│
├── notebooks/
│   ├── 01_Data_Cleaning_EDA.ipynb
│   └── 02_Modeling_Price_Prediction.ipynb
│
├── plots/                              # Exported figures and charts
│
├── src/                                # Python scripts and utilities
│   ├── data_cleaning.py
│   └── peek_data.py
│
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
├── .gitignore
└── LICENSE