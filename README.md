# End-to-End Customer Churn Prediction & Retention Analytics

A production-style analytics and machine learning pipeline engineered to diagnose customer churn drivers, identify revenue exposure, and flag at-risk accounts using MySQL, Python (scikit-learn, SQLAlchemy), and Power BI.

---

## 1. Project Architecture

* **Database Layer (MySQL):** Normalized staging and production tables (`prod_churn`), analytical views (`vw_churn_data`, `vw_join_data`), and scored output tables (`prod_churn_predictions`).
* **Modeling Layer (Python / scikit-learn):** Random Forest classifier trained on behavioral, contractual, and demographic features.
* **Inference Pipeline:** Batch-scoring module reading unseen records from MySQL, calculating churn probabilities, assigning dynamic Risk Tiers, and writing back predictions.

---

## 2. Key Business Insights

* **Add-On Support Sensitivity:** Customers lacking *Online Security* and *Premium Support* exhibit churn rates approaching **49.53%**, making support bundle interventions a critical lever.
* **Contract Risk:** Month-to-month contracts generate the highest churn exposure, with competitive service offerings driving the vast majority of exits.
* **New Cohort Exposure:** Batch scoring on 411 newly onboarded accounts flagged **328 customers in the High-Risk Tier** (mean churn probability: **87.04%**), representing **$14,170.90 in monthly revenue exposure**.

---

## 3. Model Performance

* **Algorithm:** Random Forest Classifier (`n_estimators=100`, `max_depth=10`, stratified split)
* **ROC-AUC:** `0.8920`
* **Overall Accuracy:** `84%`
* **Precision (Churn Class):** `0.87` (High confidence in retention alerts)

---

## 4. Repository Structure

```text
├── data/                    # Raw source extracts
├── models/                  # Serialized model artifacts (.pkl)
├── sql/                     # DDL, transformation views, and KPI queries
│   ├── 01_schema.sql
│   ├── 02_views.sql
│   └── 03_analytical_queries.sql
├── src/                     # Execution pipelines
│   ├── load_staging.py      # Database ingestion script
│   ├── train_model.py       # Model training and artifact serialization
│   └── predict.py           # Batch scoring and MySQL export
├── .gitignore
└── README.md
```

---

## 5. Execution Workflow

1. **Database Setup:** Run SQL scripts in `sql/` to construct views and schemas.
2. **Train Model:** Run `python src/train_model.py` to evaluate the classifier and save artifacts to `models/`.
3. **Generate Predictions:** Run `python src/predict.py` to score new accounts and populate `prod_churn_predictions`.