import re

# Lire le fichier requirements.txt original
with open('requirements.txt', 'r') as file:
    lines = file.readlines()

# Filtrer les lignes qui ne contiennent pas de chemins locaux
cleaned_lines = [line for line in lines if not re.search(r'file://', line)]

# Écrire les lignes filtrées dans un nouveau fichier requirements_cleaned.txt
with open('requirements_cleaned.txt', 'w') as file:
    file.writelines(cleaned_lines)