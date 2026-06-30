import requests
import pandas as pd
import re

def main():
    # 1. Extracción (Agregamos ?per_page=100 para asegurar que traiga todos tus repos)
    url = "https://api.github.com/users/JorgeHdzRiv/repos?per_page=100"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error al consultar la API")
        return
        
    data = response.json()
    df = pd.DataFrame(data)
    
    # 2. Transformación y Limpieza
    # Filtramos para quedarnos SOLO con tus proyectos originales (no forks)
    df = df[df['fork'] == False]
    # Filtramos para quedarnos solo con los que tienen un lenguaje definido
    df = df.dropna(subset=['language']) 
    
    lang_counts = df['language'].value_counts()

    stats_md = "\n"
    for lang, count in lang_counts.items():
        stats_md += f"- **{lang}**: {count} repositorios\n"
    stats_md += "\n"

    # 3. Carga segura
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    pattern = r"().*?()"
    new_readme = re.sub(pattern, rf"\g<1>{stats_md}\g<2>", readme_content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_readme)
        
    print("Estadísticas actualizadas y limpias.")

if __name__ == "__main__":
    main()