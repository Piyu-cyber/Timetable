from flask import Flask, render_template, jsonify, request
import json
import pandas as pd
import os

app = Flask(__name__, template_folder='.')

# Load timetable data from CSV file
def load_data():
    try:
        # Print the current directory for debugging
        print(f"Current directory: {os.getcwd()}")
        # List files in the current directory
        print(f"Files in directory: {os.listdir('.')}")
        
        # Check if the file exists
        csv_file = 'combined timetable  .csv'
        if not os.path.exists(csv_file):
            print(f"CSV file not found: {csv_file}")
            return get_sample_data()
            
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Print column names for debugging
        print(f"CSV columns: {df.columns.tolist()}")
        print(f"Data shape: {df.shape}")
        
        # Define explicit column mapping from CSV to expected names
        column_mapping = {
            'Day': 'day',
            'Time': 'time',
            'Room': 'room',
            'Course Code': 'courseCode',
            'Course Title': 'courseTitle',
            'Faculty': 'faculty',
            'Session Type': 'sessionType',
            'Branch': 'branch'
        }
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Verify all necessary columns exist
        required_columns = ['day', 'time', 'room', 'courseCode', 'courseTitle', 'faculty', 'sessionType', 'branch']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Still missing columns after mapping: {missing_columns}")
            # If critical columns are missing, use sample data
            return get_sample_data()
        
        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        
        # Clean up any NaN values
        for item in data:
            for key, value in item.items():
                if pd.isna(value):
                    item[key] = ""
                    
        print(f"Successfully loaded {len(data)} records from CSV")
        # Print a sample record for debugging
        if data:
            print(f"Sample record: {data[0]}")
            
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        # Return sample data as fallback
        return get_sample_data()

# Sample data as fallback in case CSV loading fails
def get_sample_data():
    print("Using sample data fallback")
    data = [
        # Lectures
        {"day": "Monday", "time": "09:00-10:00", "room": "C002", "courseCode": "CSE101", "courseTitle": "LangGraph", "faculty": "Dr. Smith", "sessionType": "Lecture", "branch": "CSE"},
        {"day": "Monday", "time": "10:00-11:00", "room": "C003", "courseCode": "ECE201", "courseTitle": "Circuit Theory", "faculty": "Dr. Johnson", "sessionType": "Lecture", "branch": "ECE"},
        {"day": "Monday", "time": "11:00-12:00", "room": "C004", "courseCode": "DSAI301", "courseTitle": "Machine Learning", "faculty": "Dr. Williams", "sessionType": "Lecture", "branch": "DSAI"},
        {"day": "Monday", "time": "12:00-13:00", "room": "C204", "courseCode": "B1_001", "courseTitle": "Web Development", "faculty": "Dr. Davis", "sessionType": "Lecture", "branch": "B1"},
        
        # Breaks
        {"day": "Monday", "time": "13:00-14:00", "room": "", "courseCode": "", "courseTitle": "Lunch Break", "faculty": "", "sessionType": "Break", "branch": ""},
        {"day": "Monday", "time": "17:00-17:30", "room": "", "courseCode": "", "courseTitle": "Snack Break", "faculty": "", "sessionType": "Break", "branch": ""},
        
        # Tutorials
        {"day": "Monday", "time": "14:00-15:00", "room": "C304", "courseCode": "CSE101", "courseTitle": "Introduction to Computer Science", "faculty": "Dr. Smith", "sessionType": "Tutorial", "branch": "CSE"},
        {"day": "Monday", "time": "15:00-16:00", "room": "C305", "courseCode": "ECE201", "courseTitle": "Circuit Theory", "faculty": "Dr. Johnson", "sessionType": "Tutorial", "branch": "ECE"},
        
        # Practicals
        {"day": "Monday", "time": "16:00-17:00", "room": "L207", "courseCode": "DSAI301", "courseTitle": "Machine Learning", "faculty": "Dr. Williams", "sessionType": "Practical", "branch": "DSAI"},
        
        # Tuesday
        {"day": "Tuesday", "time": "09:00-10:00", "room": "C002", "courseCode": "CSE102", "courseTitle": "Data Structures", "faculty": "Dr. Brown", "sessionType": "Lecture", "branch": "CSE"},
        {"day": "Tuesday", "time": "10:00-11:00", "room": "C003", "courseCode": "ECE202", "courseTitle": "Digital Electronics", "faculty": "Dr. Taylor", "sessionType": "Lecture", "branch": "ECE"},
        {"day": "Tuesday", "time": "11:00-12:00", "room": "C004", "courseCode": "DSAI302", "courseTitle": "Deep Learning", "faculty": "Dr. Wilson", "sessionType": "Lecture", "branch": "DSAI"},
        {"day": "Tuesday", "time": "12:00-13:00", "room": "C204", "courseCode": "B2_001", "courseTitle": "Mobile App Development", "faculty": "Dr. Clark", "sessionType": "Lecture", "branch": "B2"},
        
        # Breaks
        {"day": "Tuesday", "time": "13:00-14:00", "room": "", "courseCode": "", "courseTitle": "Lunch Break", "faculty": "", "sessionType": "Break", "branch": ""},
        {"day": "Tuesday", "time": "17:00-17:30", "room": "", "courseCode": "", "courseTitle": "Snack Break", "faculty": "", "sessionType": "Break", "branch": ""},
        
        # More classes for other days...
        {"day": "Wednesday", "time": "09:00-10:00", "room": "C002", "courseCode": "CSE103", "courseTitle": "Algorithms", "faculty": "Dr. White", "sessionType": "Lecture", "branch": "CSE"},
        {"day": "Wednesday", "time": "10:00-11:00", "room": "L207", "courseCode": "CSE101", "courseTitle": "Introduction to Computer Science", "faculty": "Dr. Padhy", "sessionType": "Practical", "branch": "CSE"},
        
        {"day": "Thursday", "time": "09:00-10:00", "room": "C002", "courseCode": "B3_001", "courseTitle": "Cloud Computing", "faculty": "Dr. Lee", "sessionType": "Lecture", "branch": "B3"},
        {"day": "Thursday", "time": "14:00-15:00", "room": "C204", "courseCode": "ECE202", "courseTitle": "Digital Electronics", "faculty": "Dr. Taylor", "sessionType": "Tutorial", "branch": "ECE"},
        
        {"day": "Friday", "time": "09:00-10:00", "room": "C003", "courseCode": "DSAI303", "courseTitle": "Natural Language Processing", "faculty": "Dr. Moore", "sessionType": "Lecture", "branch": "DSAI"},
        {"day": "Friday", "time": "15:00-16:00", "room": "L208", "courseCode": "DSAI302", "courseTitle": "Deep Learning", "faculty": "Dr. Wilson", "sessionType": "Practical", "branch": "DSAI"}
    ]
    return data

@app.route('/')
def index():
    return render_template('timetable-visualization.html')

@app.route('/data')
def get_data():
    """API endpoint to get timetable data"""
    data = load_data()
    print(f"Sending {len(data)} records to client")
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)