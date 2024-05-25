from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/fetch-csv-data', methods=['GET'])
def fetchCsvData():
    csvFilePath = 'emails.csv'
    
    try:
        df = pd.read_csv(csvFilePath)
        
        data = df.to_dict(orient="records",)
        
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error":str(e)}), 500
   
   
    
if __name__ == '__main__':
    app.run(port=8000, debug=True)