# Car Market Analysis in Attica (2021–2026): Price Prediction and Market Segmentation

## Overview

This repository contains the analytical implementation of a thesis project on the **used car market in Attica, Greece**, covering the period **2021–2026**. The study combines **price prediction** with **market segmentation**, with the aim of examining both vehicle-level price determinants and broader market-level patterns.

The project follows a **reproducible Python-based workflow** that includes:

- data collection and organization
- data cleaning and validation
- exploratory data analysis (EDA)
- feature engineering
- predictive modeling
- model evaluation and interpretability
- final thesis-oriented reporting
- market segmentation and market-level insight generation

The repository is designed to support **academic writing**, **reproducible analysis**, and the systematic export of processed tables and figures for thesis use, appendices, and presentation material.

## Thesis Objective

The thesis has two complementary objectives.

First, it investigates the determinants of used car prices in Attica and develops predictive models for price estimation based on vehicle and listing characteristics.

Second, it examines the internal structure of the market through segmentation-oriented analysis, in order to identify meaningful submarkets and produce market-level insights that go beyond point prediction.

More specifically, the study evaluates the role of:

- **Technical characteristics**: engine displacement, horsepower, fuel type, transmission
- **Usage-related variables**: mileage, age, registration year
- **Market characteristics**: manufacturer, model, listing composition
- **Geographical information**: variation within the Attica region
- **Segment-level patterns**: differences across price-based market segments in terms of technical profile and market composition

## Project Status

The repository currently contains a completed end-to-end analytical workflow across five notebooks:

- **Notebook 1:** Data Cleaning & Exploratory Data Analysis
- **Notebook 2:** Modeling & Price Prediction
- **Notebook 3:** Model Evaluation, Hyperparameter Tuning, Error Analysis & Interpretability
- **Notebook 4:** Final Results & Thesis Reporting
- **Notebook 5:** Market Segmentation & Market-Level Insights

At the current stage, the repository includes:

- a cleaned analytical dataset
- a structured ML-ready dataset
- baseline and tree-based model comparison
- final-model prediction exports
- extended model evaluation outputs
- SHAP-based interpretability results
- thesis-ready summary tables and figures
- market segmentation outputs and segment profiling tables
- export-ready visual material in `plots/`

In its current form, the project should be understood not only as a predictive modeling study, but as a broader analytical framework for understanding the used car market in Attica.

## Research Goals

The project is structured around the following research goals:

1. Create and organize a structured dataset of used car listings in Attica.
2. Clean and preprocess the raw data for reliable analytical use.
3. Explore market patterns through descriptive statistics and visualizations.
4. Identify the variables most strongly associated with vehicle price.
5. Develop and evaluate machine learning models for price prediction.
6. Interpret the final predictive model in an academically meaningful way.
7. Synthesize the main predictive findings into thesis-ready tables, figures, and conclusions.
8. Extend the analysis from price prediction to market segmentation and market-level insight generation.
9. Document the full workflow in a reproducible and well-structured repository.

## Dataset

The project is based on vehicle listings from the Attica region and supports both **predictive modeling** and **market segmentation analysis**.

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
- `price_segment` / Derived price-based market segment

### Data Preparation

The initial version of the dataset was organized in spreadsheet form and then processed through Python scripts and notebooks for:

- standardization of column names
- missing value inspection
- duplicate checks
- numeric parsing and type correction
- category normalization
- derived feature creation
- creation of cleaned and ML-ready datasets
- preparation of segment-oriented analytical variables for market profiling

The cleaned analytical dataset supports descriptive analysis, final reporting, and market segmentation, while the ML-ready dataset is used for predictive modeling.

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
- Exploration of market patterns by fuel type, manufacturer, registration year, and region
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

### 6. Model Evaluation, Interpretability, and Final Reporting
Models are assessed using standard regression metrics such as:

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**

The extended evaluation and reporting stage also includes:

- hyperparameter tuning
- tuned vs untuned comparison
- detailed error analysis
- residual diagnostics
- grouped error analysis by market segment and vehicle characteristics
- SHAP-based interpretability
- synthesis of thesis-ready findings, conclusions, limitations, and future research directions

### 7. Market Segmentation and Market-Level Insights
The final analytical stage extends the project beyond prediction and investigates the structure of the market itself through:

- price distribution analysis
- quantile-based market segmentation
- segment profiling by price, mileage, age, horsepower, and engine size
- categorical comparisons by fuel type, transmission, and manufacturer
- interpretation of segment-level submarkets within the used car market of Attica

## Current Analytical Outputs and Findings

The repository currently documents two complementary analytical streams: **predictive modeling** and **market segmentation**.

### Price Prediction and Model Evaluation

In the main modeling stage, multiple regression models were compared on the test set. The strongest overall predictive performance was achieved by **XGBoost**, while **Random Forest** also showed strong results. The repository includes both the original modeling outputs and the extended evaluation outputs produced during the model assessment stage.

Core exported files include:

- `data/processed/cleaned_car_data.csv`
- `data/processed/ml_ready_car_data.csv`
- `data/processed/model_comparison_results.csv`
- `data/processed/best_model_test_predictions.csv`

Additional evaluation outputs include:

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

### Final Thesis Reporting

The fourth notebook consolidates the main predictive findings into thesis-oriented outputs. It supports academic reporting through summary tables, model comparison material, tuned-versus-untuned comparisons, grouped performance analysis, SHAP summaries, and interpretive conclusions suitable for thesis chapters, appendices, and presentation material.

Representative thesis-reporting outputs are organized in:

- `data/processed/notebook4_outputs/`
- `plots/` (export-ready figures from the final reporting stage)

### Market Segmentation and Market-Level Insights

The fifth notebook extends the project beyond price prediction by examining the structure of the market itself. A quantile-based approach is used to create four balanced price segments, which are then profiled using both numerical and categorical variables.

Representative segmentation outputs include:

- `data/processed/notebook5_market_overview.csv`
- `data/processed/notebook5_descriptive_statistics.csv`
- `data/processed/notebook5_price_segment_counts.csv`
- `data/processed/notebook5_price_segment_cutoffs.csv`
- `data/processed/notebook5_segment_profile_summary.csv`
- `data/processed/notebook5_fuel_type_by_segment_counts.csv`
- `data/processed/notebook5_fuel_type_by_segment_shares.csv`
- `data/processed/notebook5_transmission_by_segment_counts.csv`
- `data/processed/notebook5_transmission_by_segment_shares.csv`
- `data/processed/notebook5_top10_make_by_segment_counts.csv`
- `data/processed/notebook5_top10_make_by_segment_shares.csv`

Together, these outputs support a broader interpretation of the used car market in Attica by connecting predictive accuracy with interpretable market structure.

## Key Repository Artifacts

The repository is organized around a small set of core analytical artifacts:

- **Jupyter notebooks** documenting the full workflow from cleaning to final reporting and market segmentation
- **`src/peek_data.py`** for raw-data inspection and preliminary auditing
- **`src/data_cleaning.py`** for dataset cleaning, normalization, and export preparation
- **`data/processed/`** for version-controlled processed tables and analytical CSV outputs
- **`plots/`** for export-ready figures used in thesis writing and presentation material
- **`activity.log`** for chronological documentation of the project workflow and research progress
- **`requirements.txt`** for the Python dependency set required to reproduce the analysis

## Reproducibility

The repository is structured to support a reproducible research workflow.

### Recommended execution order

1. Prepare the Python environment from `requirements.txt`.
2. Run the raw-data audit script:
   - `src/peek_data.py`
3. Run the cleaning pipeline:
   - `src/data_cleaning.py`
4. Open and execute the notebooks in order:
   - `01_Data_Cleaning_EDA.ipynb`
   - `02_Modeling_Price_Prediction.ipynb`
   - `03_Model_Evaluation_Interpretability.ipynb`
   - `04_Final_Results_Thesis_Reporting.ipynb`
   - `05_Market_Segmentation_Insights.ipynb`
5. Review the exported tables in `data/processed/`, the figures in `plots/`, and the documented workflow in `activity.log`.

### Reproducibility Notes

- The repository is intended to keep the analytical workflow transparent, structured, and academically traceable.
- Version-controlled tabular outputs are concentrated in `data/processed/`.
- Export-ready figures are stored in `plots/` for direct use in reporting and presentation workflows.
- The project combines scripts, notebooks, processed outputs, and research logging in a way that supports both replication and thesis writing.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Athina34/Car-Market-Analysis-Attica.git
cd Car-Market-Analysis-Attica
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On **Windows (PowerShell)**:

```bash
.venv\Scripts\Activate.ps1
```

On **Windows (Command Prompt)**:

```bash
.venv\Scripts\activate.bat
```

On **macOS / Linux**:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Execute the workflow

After installing the dependencies, run the project in the following order:

1. Execute the raw-data audit script:
   - `src/peek_data.py`

2. Execute the cleaning pipeline:
   - `src/data_cleaning.py`

3. Open and run the notebooks in sequence:
   - `01_Data_Cleaning_EDA.ipynb`
   - `02_Modeling_Price_Prediction.ipynb`
   - `03_Model_Evaluation_Interpretability.ipynb`
   - `04_Final_Results_Thesis_Reporting.ipynb`
   - `05_Market_Segmentation_Insights.ipynb`

### 6. Review exported outputs

After execution, review the following repository outputs:

- `data/processed/` for processed analytical tables and exported CSV files
- `plots/` for export-ready figures
- `activity.log` for documented project progress and workflow history

## Data Availability

The repository is structured to support reproducibility while keeping data management controlled.

- Raw source files are not fully tracked in the repository.
- Processed analytical CSV outputs are maintained in `data/processed/` for reproducible downstream analysis.
- Export-ready figures are stored in `plots/`.
- The documented analytical workflow is summarized in `activity.log`.

This structure allows the repository to remain academically documented, reproducible, and maintainable for thesis-oriented analytical work.