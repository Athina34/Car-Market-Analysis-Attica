# Car Market Analysis in Attica (2021–2026) & Price Prediction

## Overview

This repository contains the implementation of a thesis project focused on the **used car market in Attica, Greece**, covering the period **2021–2026**. The main objective is to analyze the factors that influence used car prices and to develop a **machine learning model for price prediction**.

The project follows a **reproducible data science workflow** in Python, combining:

- data collection and organization
- data cleaning and validation
- exploratory data analysis (EDA)
- feature engineering
- predictive modeling
- model evaluation and interpretability

---

## Thesis Objective

The central goal of this study is to investigate the determinants of used car prices in Attica and to build a reliable predictive model based on vehicle and market characteristics.

More specifically, the project examines the effect of variables such as:

- **Technical characteristics**: engine displacement, horsepower, fuel type, transmission
- **Usage-related variables**: mileage, age, registration year
- **Market characteristics**: manufacturer, model, listing structure
- **Geographical information**: regional variation within Attica

---

## Project Status

The repository currently includes the following completed stages:

- **Notebook 1:** Data Cleaning & Exploratory Data Analysis
- **Notebook 2:** Modeling & Price Prediction
- **Notebook 3:** Model Evaluation, Hyperparameter Tuning, Error Analysis & Interpretability
- creation of cleaned and model-ready datasets
- export of processed analytical outputs in `data/processed/`

At the current stage, the project includes:

- a cleaned analytical dataset
- a structured ML-ready dataset
- baseline and tree-based model comparison
- final-model prediction exports
- post-model evaluation outputs
- SHAP-based interpretability outputs

---

## Research Goals

The project is structured around the following goals:

1. Create and organize a structured dataset of car listings in Attica.
2. Clean and preprocess the raw data for analytical use.
3. Explore market patterns through descriptive statistics and visualizations.
4. Identify the variables most strongly associated with price.
5. Develop and evaluate machine learning models for price prediction.
6. Interpret the final model in an academically meaningful way.
7. Document the full workflow in a reproducible and well-structured repository.

---

## Dataset

The project is based on vehicle listings from the Attica region.

- The **initial raw dataset** contained more than **12,000 listings**.
- After cleaning and preparation, the **cleaned analytical dataset** contains **8,933 observations**.
- A separate **ML-ready dataset** was created for predictive modeling.
- The main modeling stage focuses on the **used-car subset**, which contains **8,296 observations**.

### Main Variables

Key variables used in the analysis include:

- `Κατασκευαστής` / Make
- `Τύπος` / Model
- `Εγγραφή` / Registration year
- `Ηλικία` / Vehicle age
- `Καύσιμο` / Fuel type
- `Μετάδοση` / Transmission
- `Κυβικά` / Engine displacement
- `Ιπποδύναμη` / Horsepower
- `Χιλιόμετρα` / Mileage
- `Περιοχή` / Region
- `Τιμή` / Price (**target variable**)

### Data Preparation

The initial version of the dataset was organized in spreadsheet form and then processed through Python scripts and notebooks for:

- standardization of column names
- missing value inspection
- duplicate checks
- numeric parsing and type correction
- category normalization
- derived feature creation
- creation of cleaned and ML-ready datasets

---

## Methodology

The methodological workflow of the project consists of the following stages:

### 1. Data Collection and Organization
- Collection and structuring of raw vehicle listing data
- Creation of the initial raw dataset in spreadsheet format

### 2. Data Cleaning and Preprocessing
- Handling missing values and inconsistent records
- Duplicate detection and conservative duplicate removal
- Standardization of categories and formats
- Numeric value parsing and cleaning
- Data quality checks
- Preparation of cleaned datasets for analysis and modeling

### 3. Exploratory Data Analysis (EDA)
- Descriptive statistics
- Distribution analysis of price, mileage, and technical features
- Market segmentation by fuel type, manufacturer, registration year, and region
- Visualization of relationships between vehicle characteristics and price

### 4. Feature Engineering
- Selection of relevant predictors
- Creation of derived variables such as vehicle age
- Encoding of categorical variables
- Construction of model-ready input tables

### 5. Predictive Modeling
The project evaluates machine learning models for used car price estimation, including:

- Dummy Regressor
- Linear Regression
- Ridge Regression
- Random Forest
- XGBoost

### 6. Model Evaluation and Interpretability
Models are assessed using standard regression metrics such as:

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**

In the final evaluation stage, the analysis also includes:

- hyperparameter tuning
- tuned vs untuned comparison
- detailed error analysis
- residual diagnostics
- grouped error analysis by market segment
- SHAP-based interpretability

---

## Current Modeling Summary

In the main modeling stage, multiple regression models were compared on the test set.

The strongest overall predictive performance was achieved by **XGBoost**, while **Random Forest** also showed strong results. The repository now includes both the original modeling outputs and the extended evaluation outputs produced in the third notebook.

Core exported files include:

- `data/processed/cleaned_car_data.csv`
- `data/processed/ml_ready_car_data.csv`
- `data/processed/model_comparison_results.csv`
- `data/processed/best_model_test_predictions.csv`

Additional evaluation outputs from Notebook 3 include:

- `data/processed/notebook3_search_summary.csv`
- `data/processed/notebook3_model_test_results.csv`
- `data/processed/notebook3_tuned_vs_untuned_comparison.csv`
- `data/processed/notebook3_final_model_predictions.csv`
- `data/processed/notebook3_error_by_fuel_type.csv`
- `data/processed/notebook3_error_by_make.csv`
- `data/processed/notebook3_error_by_registration_year.csv`
- `data/processed/notebook3_error_by_price_segment.csv`
- `data/processed/notebook3_transformed_shap_importance.csv`
- `data/processed/notebook3_grouped_shap_importance.csv`

These files support the reproducibility of the analysis and can be used directly in thesis writing, tables, appendices, and presentation material.

---

## Reproducibility

The repository is structured to support a reproducible workflow.

### Recommended execution order

1. Run the raw-data audit script
2. Run the cleaning pipeline
3. Open and execute the notebooks in order:
   - `01_Data_Cleaning_EDA.ipynb`
   - `02_Modeling_Price_Prediction.ipynb`
   - `03_Model_Evaluation_Interpretability.ipynb`

### Scripts

- `src/peek_data.py`  
  Performs a quick audit of the raw dataset, including structure, missing values, duplicates, and descriptive previews.

- `src/data_cleaning.py`  
  Loads the raw Excel file, cleans and normalizes the dataset, creates derived features, and exports:
  - `cleaned_car_data.csv`
  - `ml_ready_car_data.csv`

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Athina34/Car-Market-Analysis-Attica.git
cd Car-Market-Analysis-Attica