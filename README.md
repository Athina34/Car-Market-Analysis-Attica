# Car Market Analysis in Attica (2021–2026) & Price Prediction

## Overview
This thesis project focuses on the analysis of the **used car market in Attica, Greece**, for the period **2021–2026**, with the aim of identifying the main factors that affect vehicle prices and developing a **machine learning model for price prediction**.

The project combines **data cleaning**, **exploratory data analysis (EDA)**, **feature engineering**, and **predictive modeling** in a reproducible data science workflow implemented in Python.

---

## Thesis Objective
The main objective of this study is to investigate the determinants of used car prices in Attica and to build a reliable predictive model based on vehicle and market characteristics.

More specifically, the project examines the effect of variables such as:

- **Technical characteristics**: engine displacement (CC), horsepower (HP), fuel type, transmission
- **Usage-related variables**: mileage and registration year
- **Market information**: manufacturer, model, body type, listing characteristics
- **Geographical dimension**: price differences across areas within Attica

---

## Research Goals
The project is structured around the following goals:

1. **Create and organize a structured dataset** of used car listings in Attica.
2. **Clean and preprocess** the raw data for analytical use.
3. **Explore market patterns and trends** through descriptive statistics and visualizations.
4. **Identify the variables that most strongly affect price**.
5. **Develop and evaluate machine learning models** for used car price prediction.
6. **Document the full workflow** in a reproducible and academically structured way.

---

## Dataset
The dataset includes **more than 12,000 observations** from the used car market in Attica.

### Main variables
Some of the key variables used in the analysis include:

- `Make/Model` – vehicle manufacturer and model
- `Registration` – first registration year
- `Fuel Type` – petrol, diesel, hybrid, electric, etc.
- `Mileage` – total kilometers driven
- `Price` – selling price (**target variable**)

Additional variables may include:

- `Engine Disp.` – engine displacement
- `Horsepower` – vehicle power
- `Transmission` – manual / automatic
- `Region` or `Location` – geographical information within Attica
- Other listing-specific or technical attributes depending on data availability

### Data source and preparation
The initial version of the dataset was organized in Excel format and then processed through Python scripts and notebooks for:

- standardization of column names
- missing value checks
- duplicate handling
- data type correction
- category normalization
- preparation of cleaned and model-ready datasets

---

## Methodology
The methodological workflow of the project consists of the following stages:

### 1. Data Collection and Organization
- Collection and structuring of raw vehicle listing data
- Creation of the initial raw dataset in spreadsheet format

### 2. Data Cleaning and Preprocessing
- Handling missing values and inconsistent records
- Removing duplicates
- Standardizing categories and formats
- Detecting and treating outliers
- Preparing cleaned datasets for analysis and modeling

### 3. Exploratory Data Analysis (EDA)
- Descriptive statistics
- Distribution analysis of prices, mileage, and technical features
- Market segmentation by fuel type, manufacturer, registration year, and region
- Visualization of relationships between vehicle characteristics and price

### 4. Feature Engineering
- Selection of relevant predictors
- Transformation of variables where needed
- Encoding categorical variables
- Construction of model-ready input tables

### 5. Predictive Modeling
The project evaluates machine learning models for used car price estimation, such as:

- Linear Regression
- Regularized Regression (Ridge / Lasso)
- Tree-based models
- Random Forest
- XGBoost

### 6. Model Evaluation
Models are assessed using suitable regression metrics, such as:

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**

Residual analysis and comparison across models are also used to support the final model selection.

---

## Technologies and Tools
The project is implemented in **Python 3.x** using the following libraries:

- **Pandas** – data manipulation
- **NumPy** – numerical computations
- **Matplotlib / Seaborn / Plotly** – data visualization
- **Scikit-learn** – preprocessing, modeling, and evaluation
- **XGBoost** – gradient boosting regression
- **SHAP** – model interpretability
- **Streamlit** *(optional)* – interactive dashboard or presentation layer

---

## Repository Structure
```text
Car-Market-Analysis-Attica/
│
├── data/
│   ├── raw/                # Raw input files (kept locally / not necessarily tracked)
│   └── processed/          # Cleaned and export-ready datasets
│
├── logs/                   # Research logs, activity notes, process documentation
│
├── notebooks/              # Jupyter notebooks for cleaning, EDA, and experiments
│
├── plots/                  # Exported figures and charts used in the thesis
│
├── src/                    # Python scripts for data cleaning and utilities
│   ├── data_cleaning.py
│   └── peek_data.py
│
├── requirements.txt        # Project dependencies
├── README.md               # Project description
├── LICENSE                 # License information
└── .gitignore              # Files ignored by Git


## Installation

### Option 1: Clone the repository
```bash
git clone https://github.com/Athina34/Car-Market-Analysis-Attica.git
cd Car-Market-Analysis-Attica
pip install -r requirements.txt