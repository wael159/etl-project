# ETL Project

A modern ETL (Extract, Transform, Load) application that provides a user-friendly interface for data processing and transformation.

## Overview

This project implements an ETL pipeline with the following components:
- Data extraction from source databases
- Data transformation and cleaning
- Data loading into target databases
- Web interface for configuration
- REST API for automation

## Features

- **Web Interface**: Easy-to-use UI for database configuration
- **API Endpoints**: RESTful API for ETL operations
- **Database Support**: PostgreSQL integration
- **Docker Support**: Containerized deployment
- **Cloud Ready**: Deployable on Hugging Face Spaces

## Getting Started

1. Clone the repository
2. Install dependencies
3. Configure your database connections
4. Run the application

## API Usage

### ETL Endpoint

**URL**: `/api/etl`  
**Method**: `POST`  
**Content-Type**: `application/json`

#### Request Body

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

#### Response Format

Success (200 OK):
```json
{
    "status": "success",
    "message": "ETL process completed successfully"
}
```

Error (400 Bad Request):
```json
{
    "status": "failed",
    "message": "Missing required field: source_host"
}
```

Error (500 Internal Server Error):
```json
{
    "status": "failed",
    "message": "Database connection failed"
}
```

### Example Usage

#### Using cURL
```bash
curl -X POST https://your-domain.com/api/etl \
  -H "Content-Type: application/json" \
  -d '{
    "source_host": "localhost",
    "source_port": "5432",
    "source_user": "postgres",
    "source_password": "password123",
    "source_database": "source_db",
    "source_table": "raw_data",
    "target_host": "localhost",
    "target_port": "5432",
    "target_user": "postgres",
    "target_password": "password123",
    "target_database": "target_db",
    "target_table": "cleaned_data"
  }'
```

#### Using Python
```python
import requests
import json

url = "https://your-domain.com/api/etl"
data = {
    "source_host": "localhost",
    "source_port": "5432",
    "source_user": "postgres",
    "source_password": "password123",
    "source_database": "source_db",
    "source_table": "raw_data",
    "target_host": "localhost",
    "target_port": "5432",
    "target_user": "postgres",
    "target_password": "password123",
    "target_database": "target_db",
    "target_table": "cleaned_data"
}

response = requests.post(url, json=data)
print(response.json())
```

#### Using Postman
1. Create a new POST request
2. Set URL to `https://your-domain.com/api/etl`
3. Set Headers:
   - Key: `Content-Type`
   - Value: `application/json`
4. Set Body (raw JSON):
```json
{
    "source_host": "localhost",
    "source_port": "5432",
    "source_user": "postgres",
    "source_password": "password123",
    "source_database": "source_db",
    "source_table": "raw_data",
    "target_host": "localhost",
    "target_port": "5432",
    "target_user": "postgres",
    "target_password": "password123",
    "target_database": "target_db",
    "target_table": "cleaned_data"
}
```

### Common Use Cases

1. **Data Migration**
   - Move data from one database to another
   - Transform data during migration
   - Clean and validate data

2. **Data Cleaning**
   - Remove duplicates
   - Standardize formats
   - Handle missing values

3. **Data Integration**
   - Combine data from multiple sources
   - Transform data to match target schema
   - Load into target database

4. **Automated ETL**
   - Schedule regular data updates
   - Monitor ETL process
   - Handle errors and retries

## License

MIT License

## Author

Wael159 