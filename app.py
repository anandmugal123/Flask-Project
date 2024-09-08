from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            return "No file part", 400
        
        file = request.files['csv_file']
        
        if file.filename == '':
            return "No selected file", 400
        
        if file and file.filename.endswith('.csv'):
            try:
                filename = secure_filename(file.filename.strip())
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                df = pd.read_csv(filepath)
                columns = df.columns.tolist()
                
                return render_template('configure_dashboard.html', columns=columns, filepath=filepath)
            except Exception as e:
                return f"An error occurred: {e}", 500

    return render_template('upload.html')


@app.route('/configure_dashboard', methods=['POST'])
def configure_dashboard():
    num_charts = int(request.form['num_charts'])
    file_path = request.form['csv_file_path']
    df = pd.read_csv(file_path)
    charts = []

    for i in range(1, num_charts + 1):
        chart_type = request.form.get(f'chart_type_{i}')
        x_column = request.form.get(f'x_column_{i}')
        y_column = request.form.get(f'y_column_{i}')

        if chart_type == 'pie':
            fig = px.pie(df, names=x_column, values=y_column, title=f'Pie Chart {i}')
        elif chart_type == 'bar':
            fig = px.bar(df, x=x_column, y=y_column, title=f'Bar Chart {i}')
        elif chart_type == 'scatter':
            fig = px.scatter(df, x=x_column, y=y_column, title=f'Scatter Plot {i}')
        elif chart_type == 'line':
            fig = px.line(df, x=x_column, y=y_column, title=f'Line Chart {i}')
        elif chart_type == 'histogram':
            fig = px.histogram(df, x=x_column, title=f'Histogram {i}')
        elif chart_type == 'box':
            fig = px.box(df, x=x_column, y=y_column, title=f'Box Plot {i}')
        elif chart_type == 'heatmap':
            fig = px.imshow(df.corr(), title=f'Heatmap {i}')
        elif chart_type == 'area':
            fig = px.area(df, x=x_column, y=y_column, title=f'Area Chart {i}')
        elif chart_type == 'bubble':
            fig = px.scatter(df, x=x_column, y=y_column, size=y_column, title=f'Bubble Chart {i}')

        charts.append(fig.to_html(full_html=False))

    return render_template('charts.html', charts=charts)

if __name__ == '__main__':
    app.run(debug=True)
