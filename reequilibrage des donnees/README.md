# 🏥 Medical Data Rebalancing & Classification (Smoker Prediction)

This project presents a comprehensive study on data rebalancing and binary classification applied to a medical dataset (`Medical cost.csv`). The main objective is to predict whether an individual is a smoker (`smoker`) based on their characteristics, while addressing class imbalance issues.

## 📓 Notebook: [main.ipynb](main.ipynb)

The notebook provides a structured workflow, from data preparation to advanced model evaluation, including the analysis of problematic folds.

---

## 1. **Data Preprocessing**

- **Loading & Exploration**: Import data, check for duplicates, inspect column types, handle missing values, and generate descriptive statistics.
- **Handling Missing Values**:
  - Replace with median (age), mean (BMI), or mode (children).
- **Outlier Detection & Treatment**:
  - Use the IQR method to identify outliers in numerical columns.
  - Correct extreme outliers for `bmi` and `charges`.
- **Visualizations**: Variable distributions, boxplots, and correlation heatmaps.

---

## 2. **Encoding & ML Preparation**

- **Categorical Variable Encoding**:
  - `sex` and `smoker`: binary encoding.
  - `region`: frequency encoding.
- **Feature/Target Split**: `X` (all columns except `smoker`), `y` (`smoker`).
- **Train/Test Split**: 75% train, 25% test.
- **Standardization**: Using `StandardScaler`.

---

## 3. **Modeling & Training Functions**

- **Random Forest**: Training function with metrics display, confusion matrix, and ROC curve.
- **Naive Bayes**: Same approach, tailored for binary classification.
- **XGBoost**: Training, prediction, and advanced visualization (ROC, confusion matrix).

---

## 4. **Data Rebalancing**

### **Over-sampling**
- Methods tested: `RandomOverSampler`, `SMOTE`, `ADASYN`, `BorderlineSMOTE`, `SVMSMOTE`.
- Comparative visualization before/after (distribution, PCA).
- Evaluation of the impact on model performance.

### **Under-sampling**
- Methods tested: `RandomUnderSampler`, `CondensedNearestNeighbour`, `TomekLinks`.
- Visualization and evaluation as above.

---

## 5. **Model Comparison**

For each rebalancing method:
- **Performance comparison** on the test set for Random Forest, Naive Bayes, and XGBoost.
- **Visualizations**: confusion matrices, classification reports, ROC curves.

---

## 6. **Optimization & Advanced Analysis**

- **Best Model Selection**: Naive Bayes with ADASYN.
- **Detailed Test Set Evaluation**: accuracy, classification report, confusion matrix, ROC curve.
- **Stratified Cross-Validation** (`StratifiedKFold`) to detect problematic folds (accuracy < 90%).
- **Extraction & Analysis of Defective Folds**: PCA visualization, feature exploration.

---

# Example: Data Rebalancing

![alt text](<Capture d’écran du 2025-05-18 10-39-51-1.png>)

# Example: Impact of Rebalancing

![alt text](<Capture d’écran du 2025-05-18 10-42-46.png>)

# Example: Model Results

![alt text](<Capture d’écran du 2025-05-18 10-44-16.png>)

## 🚀 **How to Use This Notebook**

1. Place `Medical cost.csv` in the same folder as [`main.ipynb`](main.ipynb).
2. Install the required dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn xgboost
   ```
3. Open and run the notebook in VS Code or Jupyter.

---

## 📊 **Key Features**

- Automated and robust preprocessing of medical data.
- Intelligent encoding of categorical variables.
- Advanced handling of class imbalance (over/under-sampling).
- Generic functions to train and compare multiple models.
- Clear visualizations for result analysis.
- In-depth analysis of challenging cases via cross-validation.

---

## 🤔 **Further Exploration**

- Test additional models or ensemble techniques.
- Explore the impact of feature engineering.
- Apply feature selection techniques.
- Extend the analysis to other medical datasets.

---

**Author**: Nzogni Omong Yann Arthur [yann_thur]  
**License**: MIT
