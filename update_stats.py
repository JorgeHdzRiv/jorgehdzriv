import requests
import pandas as pd
import re

def main():
    # 1. Extracción de datos de la API pública de GitHub
    url = "https://api.github.com/users/JorgeHdzRiv/repos"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error al consultar la API")
        return
        
    data = response.json()

    # 2. Transformación con Pandas
    df = pd.DataFrame(data)
    
    # Filtramos para quedarnos solo con repositorios que tengan un lenguaje definido
    df = df.dropna(subset=['language']) 
    
    # Contamos la frecuencia de cada lenguaje
    lang_counts = df['language'].value_counts()

    # Formateamos los datos en una lista de Markdown
    stats_md = "\n"
    for lang, count in lang_counts.items():
        stats_md += f"- **{lang}**: {count} repositorios\n"
    stats_md += "\n"

    # 3. Carga: Leer y reescribir el README.md
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    # Expresión regular para encontrar las etiquetas y reemplazar lo que hay en medio
    pattern = r"().*?()"
    new_readme = re.sub(pattern, rf"\g<1>{stats_md}\g<2>", readme_content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_readme)
        
    print("README.md actualizado correctamente con las nuevas estadísticas.")

if __name__ == "__main__":
    main()