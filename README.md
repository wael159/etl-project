# ETL Application

A Flask-based ETL (Extract, Transform, Load) application with a web interface and API endpoints.

## Features
- Web interface for configuration
- REST API for ETL operations
- PostgreSQL database support
- Docker support

## API Usage
Send a POST request to `/api/etl` with the following JSON structure:
```json
{
    "source_host": "your_source_host",
    "source_port": "5432",
    "source_user": "your_source_user",
    "source_password": "your_source_password",
    "source_database": "your_source_database",
    "source_table": "your_source_table",
    "target_host": "your_target_host",
    "target_port": "5432",
    "target_user": "your_target_user",
    "target_password": "your_target_password",
    "target_database": "your_target_database",
    "target_table": "your_target_table"
}
```

## Response Format
Success:
```json
{
    "status": "success",
    "message": "ETL process completed successfully"
}
```

Error:
```json
{
    "status": "failed",
    "message": "Error message"
}
```

Now, let's deploy to Hugging Face Spaces:

1. First, initialize a Git repository and push your code to GitHub:
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/etl-project.git

# Push to GitHub
git push -u origin main
```

2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)

3. Click "Create new Space"

4. Fill in the Space details:
   - Name: etl-project
   - SDK: Docker
   - Repository: yourusername/etl-project
   - Branch: main

5. Click "Create Space"

6. In your Space settings, add these environment variables:
   - `SECRET_KEY`: (generate a random secret key)
   - `POSTGRES_USER`: your_db_user
   - `POSTGRES_PASSWORD`: your_db_password
   - `POSTGRES_DB`: your_db_name

7. Update your `app.py` to use environment variables:

```python:app.py
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
```

After deploying, you can test your API using curl or Postman:

```bash
curl -X POST https://huggingface.co/spaces/yourusername/etl-project/api/etl \
  -H "Content-Type: application/json" \
  -d '{
    "source_host": "your_source_host",
    "source_port": "5432",
    "source_user": "your_source_user",
    "source_password": "your_source_password",
    "source_database": "your_source_database",
    "source_table": "your_source_table",
    "target_host": "your_target_host",
    "target_port": "5432",
    "target_user": "your_target_user",
    "target_password": "your_target_password",
    "target_database": "your_target_database",
    "target_table": "your_target_table"
  }'
```

Important notes:
1. Make sure to replace `yourusername` with your actual Hugging Face username
2. The Space will automatically build and deploy your application
3. You can monitor the build and deployment process in the Space's "Logs" tab
4. The application will be available at `https://huggingface.co/spaces/yourusername/etl-project`

Would you like me to help you with any specific part of the deployment process or explain anything in more detail? 