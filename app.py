from flask import Flask, render_template, request, jsonify
import pandas as pd
from src.Insurance_Fraud.pipeline.prediction import PredictionPipeline

app = Flask(__name__)
prediction_pipeline = PredictionPipeline()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data and convert to DataFrame
        form_data = request.form.to_dict()
        print("Form Data:", form_data)
       
        # Convert numeric fields
        fields = ['months_as_customer', 'age', 'policy_state', 'policy_deductable',
                    'policy_annual_premium', 'umbrella_limit', 'insured_sex',
                    'insured_education_level', 'insured_occupation', 'insured_relationship',
                    'capital-gains', 'capital-loss', 'incident_state', 'incident_city',
                    'incident_hour_of_the_day', 'number_of_vehicles_involved',
                    'property_damage', 'bodily_injuries', 'witnesses',
                    'police_report_available', 'total_claim_amount', 'injury_claim',
                    'property_claim', 'vehicle_claim', 'auto_make', 'auto_model',
                    'loss_ratio', 'profitability', 'vehicle_age', 'incident_year',
                    'incident_month', 'incident_day', 'policy_bind_year',
                    'policy_bind_month', 'policy_bind_day', 'Parked Car',
                    'Single Vehicle Collision', 'Vehicle Theft', 'Rear Collision',
                    'Side Collision', 'Fire', 'None', 'Other', 'Police', 'Minor Damage',
                    'Total Loss', 'Trivial Damage', '250/500', '500/1000', 'age_group']
        
        if 'policy_bind_date' in form_data:
            form_data['policy_bind_date'] = str(form_data['policy_bind_date'])  # Convert to string to avoid float conversion

        if 'incident_date' in form_data:
            form_data['incident_date'] = str(form_data['incident_date'])  # Convert to string to avoid float conversion

        # Convert numeric fields
        for field in fields:
            if field in form_data:
                # Convert auto_year separately to integer
                if field == 'policy_bind_date' or 'ncident_date':
                    pass  # Convert auto_year to integer
                else:
                    form_data[field] = float(form_data[field])  # Convert all other fields to float

        # Create DataFrame with single row
        input_df = pd.DataFrame([form_data])
        
        # Get prediction
        prediction_result = prediction_pipeline.predict(input_df)
        print("Prediction Result:", prediction_result)
        
        return render_template('index.html', prediction=prediction_result)
        
    except Exception as e:
        print("Error:", str(e))
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)