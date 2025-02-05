# 🔍 Insurance Fraud Detection Project

<div align="center">

[![GitHub](https://img.shields.io/github/stars/ArpitKadam/data-science-project-on-Wine-Quality?style=social)](https://github.com/ArpitKadam/Insurance-Fraud-Detection)
[![GitHub issues](https://img.shields.io/github/issues/ArpitKadam/Insurance-Fraud-Detection)](https://github.com/ArpitKadam/Insurance-Fraud-Detection/issues)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Flask](https://img.shields.io/badge/Flask-0.85%2B-blue.svg)
![MLflow](https://img.shields.io/badge/MLflow-2.0-orange.svg)
![Dagshub](https://img.shields.io/badge/Dagshub-Enabled-brightgreen.svg)

[License](https://github.com/ArpitKadam/Insurance-Fraud-Detection/blob/main/LICENSE) | [Dashboard](https://snapshots.raintank.io/dashboard/snapshot/z2B1dywVJmx9zMP5Ah0tm3mV2MletB0x) | [Dagshub](https://dagshub.com/ArpitKadam/Insurance-Fraud-Detection)

</div>

---

## 📋 Overview

This project implements a sophisticated machine learning model for detecting automobile insurance fraud. By leveraging modern tools and technologies including Dagshub, DVC, Docker, and AWS, we've created a robust pipeline for data processing, model training, and deployment.

---

## 📑 Table of Contents

- 🚀 Installation
- 🛠️ Environment Setup
- 📊 Dagshub Setup
- 💾 DVC Setup
- 🤖 Model Training and Evaluation
- 🐳 Running Docker

---

## 📁 Project Structure

<details>
<summary>Click to expand/collapse project tree</summary>

```
arpitkadam-insurance-fraud-detection/
├── 📄 README.md
├── 📄 Dockerfile
├── 📄 LICENSE
├── 📄 __init__.py
├── 📄 app.py
├── 📄 dvc.yaml
├── 📄 main.py
├── 📄 params.yaml
├── 📄 requirements.txt
├── 📄 schema.yaml
├── 📄 setup.py
├── 📄 template.py
├── 📄 .dockerignore
├── 📄 .dvcignore
│
├── 📂 artifacts/
│   ├── 📂 data_ingestion/
│   │   ├── 📄 data.zip
│   │   └── 📄 insurance_claims.csv
│   ├── 📂 data_transformation/
│   │   ├── 📄 encoders.pkl
│   │   ├── 📄 test.csv
│   │   └── 📄 train.csv
│   ├── 📂 data_validation/
│   │   └── 📄 STATUS.txt
│   ├── 📂 model_evaluation/
│   │   ├── 📄 classification_report.txt
│   │   ├── 📄 confusion_matrix.txt
│   │   └── 📄 metrics.json
│   └── 📂 model_trainer/
│       └── 📄 GradientBoostingClassifier.joblib
│
├── 📂 config/
│   └── 📄 config.yaml
│
├── 📂 data/
│   ├── 📄 data.zip
│   ├── 📄 insurance_claims.csv
│   └── 📄 insurance_claims.csv.dvc
│
├── 📂 logs/
│
├── 📂 research/
│   ├── 📄 01_data_ingestion.ipynb
│   ├── 📄 02_data_validation.ipynb
│   ├── 📄 03_data_transformation.ipynb
│   ├── 📄 04_model_trainer.ipynb
│   ├── 📄 05_model_evaluation.ipynb
│   ├── 📄 research.ipynb
│   ├── 📂 Automated-EDA/
│   │   └── 📄 Automated-EDA.ipynb
│   ├── 📂 Model_Result/
│   │   ├── 📄 Model_Comparison_Results.csv
│   │   ├── 📄 Model_Training_Log.txt
│   │   └── 📄 insurance_claims_report.txt
│   ├── 📂 Research-Text-Files/
│   │   ├── 📄 Balanced_Data_Info.txt
│   │   ├── 📄 Basic_Statistics.txt
│   │   ├── 📄 Data Stats
│   │   ├── 📄 Missing_Values_After_Handling.txt
│   │   ├── 📄 Numerical_Statistics.txt
│   │   ├── 📄 Scaled_Data_Info.txt
│   │   └── 📄 Unique_Values.txt
│   └── 📂 Visualization-Images/
│
├── 📂 src/
│   ├── 📄 __init__.py
│   └── 📂 Insurance_Fraud/
│       ├── 📄 __init__.py
│       ├── 📂 components/
│       │   ├── 📄 __init__.py
│       │   ├── 📄 data_ingestion.py
│       │   ├── 📄 data_transformation.py
│       │   ├── 📄 data_validation.py
│       │   ├── 📄 model_evaluation.py
│       │   └── 📄 model_trainer.py
│       ├── 📂 config/
│       │   ├── 📄 __init__.py
│       │   └── 📄 configuration.py
│       ├── 📂 constants/
│       │   └── 📄 __init__.py
│       ├── 📂 entity/
│       │   ├── 📄 __init__.py
│       │   └── 📄 config_entity.py
│       ├── 📂 exception/
│       │   ├── 📄 __init__.py
│       │   └── 📄 exception.py
│       ├── 📂 logger/
│       │   ├── 📄 __init__.py
│       │   └── 📄 logger.py
│       ├── 📂 pipeline/
│       │   ├── 📄 __init__.py
│       │   ├── 📄 prediction.py
│       │   ├── 📄 stage_01_data_ingestion.py
│       │   ├── 📄 stage_02_data_validation.py
│       │   ├── 📄 stage_03_data_transformation.py
│       │   ├── 📄 stage_04_model_trainer.py
│       │   └── 📄 stage_05_model_evaluation.py
│       └── 📂 utils/
│           ├── 📄 __init__.py
│           └── 📄 common.py
│
├── 📂 templates/
│   └── 📄 index.html
│
├── 📂 .dvc/
│   ├── 📄 config
│   └── 📄 .gitignore
│
└── 📂 .github/
    └── 📂 workflows/
        ├── 📄 main.yaml
        └── 📄 .gitkeep
```

</details>


---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/ArpitKadam/Insurance-Fraud-Detection.git
cd Insurance-Fraud-Detection
```

### Set Up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📊 Dagshub Setup

1. **Create Account**
   - Sign up at [Dagshub](https://dagshub.com/)
   - Create a new repository or connect to your GitHub repository

2. **Initialize Dagshub**
   ```python
   import dagshub
   dagshub.init(repo_owner='<>', repo_name='<>', mlflow=True)
   ```

3. **Configure MLflow Tracking** 
   ```python
   import os
   os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/<repo_owner>/<repo_name>.mlflow'
   os.environ['MLFLOW_TRACKING_USERNAME'] = '<repo_owner>'
   os.environ['MLFLOW_TRACKING_PASSWORD'] = '<password>'  # From Settings -> Tokens
   ```

4. **Configure a .env File**
   ```python
   ACCOUNT_ADDRESS=<>
   PRIVATE_KEY=<>
   GANACHE_URL=<>
   CONTRACT_ADDRESS=<>
   MLFLOW_TRACKING_URI=<>
   MLFLOW_TRACKING_USERNAME=<>
   MLFLOW_TRACKING_PASSWORD=<>
   ```
---

## 💾 DVC Setup

### Configure Remote Storage

```bash
# Set remote storage URL
dvc remote add origin s3://dvc
dvc remote modify origin endpointurl https://dagshub.com/<repo_owner>/<repo_name>.s3

# Configure credentials
dvc remote modify origin --local access_key_id ACCESS_KEY
dvc remote modify origin --local secret_access_key SECRET_KEY

# Initialize DVC
dvc init
```

---

## 🤖 Model Training and Evaluation

### Train Model

```bash
python main.py
```

### Make Predictions

```bash
python app.py
```

---

## 🐳 Running Docker

### Build and Run

```bash
# Build Docker image
docker build -t insurance-fraud-detection .

# Run container
docker run -p 5000:5000 insurance-fraud-detection
```

### Deploy to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag and push image
docker tag insurance-fraud-detection <your-dockerhub-username>/insurance-fraud-detection
docker push <your-dockerhub-username>/insurance-fraud-detection
```

---

## 🤝 Contributions

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

---

## 📄 License

This project is licensed under the [MIT License](https://github.com/ArpitKadam/Insurance-Fraud-Detection/blob/main/LICENSE).

---

## 📬 Contact

- Email: [arpitkadam922@gmail.com](mailto:arpitkadam922@gmail.com)
- GitHub: [ArpitKadam](https://github.com/ArpitKadam)
- Personal: [ArpitKadam](https://arpit-kadam.netlify.app/)

---

<div align="center">
Made with ❤️ by ArpitKadam
</div>
