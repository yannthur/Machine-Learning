# FraudGuard – Intelligent Bank Fraud Detection

FraudGuard is an advanced web application for real-time detection of fraudulent banking transactions using machine learning. Built with Streamlit, it provides an intuitive interface for users to analyze, visualize, and predict the risk of fraud in financial operations.

## Features

- **Real-time Fraud Detection:** Instantly analyze transactions and receive alerts for suspicious activity.
- **Machine Learning Pipeline:** Uses SVM (Support Vector Machine) with robust preprocessing (Label Encoding, Box-Cox Transformation, RobustScaler, KernelPCA).
- **Interactive Dashboard:** Visualize data, model performance, and transaction statistics.
- **User-friendly Interface:** Clean, modern UI with animations and responsive design.
- **Customizable Prediction:** Enter transaction details and get immediate fraud risk assessment.

## Project Structure

```
.
├── Analyse.ipynb           # Data analysis and model development notebook
├── streamlit/
│   ├── app.py              # Main Streamlit application
│   ├── acceuil1.json       # Lottie animation for homepage
│   └── requirements.txt    # Python dependencies
├── data/
│   └── data.csv            # Preprocessed transaction dataset
├── model/
│   └── model.pkl           # Trained SVM model
└── README.md               # Project documentation
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd streamlit/Detection\ de\ fraude\ bancaire/streamlit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare data and model:**
   - Ensure `data/data.csv` and `model/model.pkl` are present. You can generate them by running the notebook `Analyse.ipynb`.

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the app:**
   - Open your browser at [http://localhost:8501](http://localhost:8501)

## Usage

- **Home:** Overview of the solution and its advantages.
- **Solution:** Technical details about the machine learning pipeline.
- **Prediction:** Enter transaction details to check for fraud risk.

## Data & Model

- The dataset contains anonymized banking transactions with features such as amount, balances, transaction type, and a fraud label.
- The model is trained using SVM with robust preprocessing to handle outliers and non-linearities.

## Customization

- You can retrain the model or adjust preprocessing steps by modifying `Analyse.ipynb`.
- Update the UI and animations in `app.py` and `acceuil1.json`.

## License

This project is for educational and demonstration purposes.

---

*Powered by AI and Streamlit – 2024*
