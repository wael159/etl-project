from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from configparser import ConfigParser
import pandas as pd
import json
from sqlalchemy import create_engine
import transform_components

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

def save_config(config_data):
    config = ConfigParser()
    config['Database'] = {
        'source_db_type': 'postgresql',
        'source_db_host': config_data['source_host'],
        'source_db_port': config_data['source_port'],
        'source_db_user': config_data['source_user'],
        'source_db_password': config_data['source_password'],
        'source_db_database': config_data['source_database'],
        'target_db_type': 'postgresql',
        'target_db_host': config_data['target_host'],
        'target_db_port': config_data['target_port'],
        'target_db_user': config_data['target_user'],
        'target_db_password': config_data['target_password'],
        'target_db_database': config_data['target_database'],
        'source_table': config_data['source_table'],
        'target_table': config_data['target_table']
    }
    
    with open('app.properties', 'w') as f:
        config.write(f)

def run_etl(config_data):
    try:
        # Extract
        conn_str = f"postgresql://{config_data['source_user']}:{config_data['source_password']}@{config_data['source_host']}:{config_data['source_port']}/{config_data['source_database']}"
        engine = create_engine(conn_str)
        
        # Read SQL query from extract_config.json
        with open('extract_config.json') as f:
            extract_conf = json.load(f)
        query = extract_conf['query']
        
        # Execute query and fetch data
        df = pd.read_sql_query(query, engine)
        
        # Transform
        with open('config.json') as f:
            transform_config = json.load(f)
        
        # Apply transformations
        for step in transform_config['transformations']:
            condition = step.get('condition')
            if condition:
                if not eval(condition, {}, {'df': df}):
                    continue
            func = getattr(transform_components, step['name'])
            params = step.get('params', {})
            df = func(df, **params)
        
        # Save the transformed data
        df.to_csv('cleaned_data.csv', index=False)
        return True
    except Exception as e:
        raise Exception(f"ETL process failed: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            config_data = {
                'source_host': request.form['source_host'],
                'source_port': request.form['source_port'],
                'source_user': request.form['source_user'],
                'source_password': request.form['source_password'],
                'source_database': request.form['source_database'],
                'target_host': request.form['target_host'],
                'target_port': request.form['target_port'],
                'target_user': request.form['target_user'],
                'target_password': request.form['target_password'],
                'target_database': request.form['target_database'],
                'source_table': request.form['source_table'],
                'target_table': request.form['target_table']
            }
            save_config(config_data)
            flash('Configuration saved successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error saving configuration: {str(e)}', 'error')
    
    return render_template('index.html')

@app.route('/api/etl', methods=['POST'])
def etl_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'failed',
                'message': 'No data provided'
            }), 400
        
        required_fields = [
            'source_host', 'source_port', 'source_user', 'source_password', 
            'source_database', 'source_table', 'target_host', 'target_port', 
            'target_user', 'target_password', 'target_database', 'target_table'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'failed',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Run ETL process
        run_etl(data)
        
        return jsonify({
            'status': 'success',
            'message': 'ETL process completed successfully'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'failed',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Use the PORT environment variable provided by Hugging Face Spaces
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 