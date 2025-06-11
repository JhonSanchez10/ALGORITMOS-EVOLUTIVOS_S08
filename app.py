from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Cargar el archivo CSV
file_path = 'data/notas_1u.csv'  # Asegúrate de tener el archivo CSV en la ruta correcta
df = pd.read_csv(file_path)

@app.route('/')
def index():
    # Generar estadísticas generales
    stats = generate_statistics()
    return render_template('index.html', stats=stats)

@app.route('/analysis', methods=['POST'])
def analysis():
    analysis_type = request.form.get('analysis_type')
    
    # Generar estadísticas generales
    stats = generate_statistics()
    
    if analysis_type == 'histogram':
        # Histograma de notas
        img = generate_histogram()
        return render_template('analysis.html', analysis_type='Histograma', img=img, stats=None, interpretation="El histograma muestra cómo se distribuyen las notas a lo largo del rango.")
    
    elif analysis_type == 'boxplot':
        # Boxplot por tipo de examen
        img = generate_boxplot()
        return render_template('analysis.html', analysis_type='Boxplot', img=img, stats=None, interpretation="El boxplot ilustra la dispersión de las notas por tipo de examen, mostrando los cuartiles y valores atípicos.")
    
    elif analysis_type == 'mean':
        # Promedio de notas por tipo de examen
        img = generate_mean_plot()
        return render_template('analysis.html', analysis_type='Promedio de Notas', img=img, stats=None, interpretation="Este gráfico muestra el promedio de las notas por tipo de examen.")

def generate_statistics():
    min_note = df['Nota'].min()
    max_note = df['Nota'].max()
    mean_note = df['Nota'].mean()
    std_dev = df['Nota'].std()
    q1 = df['Nota'].quantile(0.25)
    q3 = df['Nota'].quantile(0.75)
    
    return {
        'min': min_note,
        'max': max_note,
        'mean': mean_note,
        'std_dev': std_dev,
        'q1': q1,
        'q3': q3
    }

def generate_histogram():
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Nota'], bins=10, kde=True, color='skyblue')

    # Añadir anotaciones para los cuartiles y el promedio
    mean = df['Nota'].mean()
    q1 = df['Nota'].quantile(0.25)
    q3 = df['Nota'].quantile(0.75)
    min_note = df['Nota'].min()
    max_note = df['Nota'].max()

    # Anotaciones en el gráfico
    plt.axvline(mean, color='red', linestyle='--')
    plt.text(mean + 0.5, 10, f'Mean: {mean:.2f}', color='red', fontsize=12)

    plt.axvline(q1, color='green', linestyle='--')
    plt.text(q1 + 0.5, 10, f'Q1: {q1:.2f}', color='green', fontsize=12)

    plt.axvline(q3, color='blue', linestyle='--')
    plt.text(q3 + 0.5, 10, f'Q3: {q3:.2f}', color='blue', fontsize=12)

    plt.axvline(min_note, color='orange', linestyle='--')
    plt.text(min_note + 0.5, 10, f'Min: {min_note}', color='orange', fontsize=12)

    plt.axvline(max_note, color='purple', linestyle='--')
    plt.text(max_note + 0.5, 10, f'Max: {max_note}', color='purple', fontsize=12)

    plt.title("Distribución de Notas", fontsize=16)
    plt.xlabel("Nota", fontsize=14)
    plt.ylabel("Frecuencia", fontsize=14)
    plt.tight_layout()

    # Guardar la imagen en un buffer y convertirla a base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.read()).decode('utf-8')
    return img_base64

def generate_boxplot():
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Tipo_Examen', y='Nota', data=df, palette="Set2")

    # Añadir anotaciones para los cuartiles y el promedio
    mean = df['Nota'].mean()
    q1 = df['Nota'].quantile(0.25)
    q3 = df['Nota'].quantile(0.75)
    min_note = df['Nota'].min()
    max_note = df['Nota'].max()

    # Anotaciones
    plt.text(0, q1 + 0.5, f'Q1: {q1:.2f}', color='green', fontsize=12)
    plt.text(0, q3 - 0.5, f'Q3: {q3:.2f}', color='blue', fontsize=12)
    plt.text(0, mean + 1, f'Mean: {mean:.2f}', color='red', fontsize=12)

    plt.title("Distribución de Notas por Tipo de Examen", fontsize=16)
    plt.xlabel("Tipo de Examen", fontsize=14)
    plt.ylabel("Nota", fontsize=14)
    plt.tight_layout()

    # Guardar la imagen en un buffer y convertirla a base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.read()).decode('utf-8')
    return img_base64

def generate_mean_plot():
    mean_by_exam = df.groupby('Tipo_Examen')['Nota'].mean().reset_index()
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Tipo_Examen', y='Nota', data=mean_by_exam, palette="Set1")

    # Añadir anotaciones del promedio
    for index, row in mean_by_exam.iterrows():
        plt.text(row.name, row['Nota'] + 0.5, f'{row["Nota"]:.2f}', color='black', ha='center')

    plt.title("Promedio de Notas por Tipo de Examen", fontsize=16)
    plt.xlabel("Tipo de Examen", fontsize=14)
    plt.ylabel("Nota Promedio", fontsize=14)
    plt.tight_layout()

    # Guardar la imagen en un buffer y convertirla a base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.read()).decode('utf-8')
    return img_base64

if __name__ == '__main__':
    app.run(debug=True)
