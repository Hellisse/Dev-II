import pandas as pd
import re

excel_file = 'TITRES.xlsx'
df = pd.read_excel(excel_file)

for index, row in df.iterrows():
    if pd.notna(row['DIPLÔME COMPLEMENTAIRE']):
        # Utilisation d'une expression régulière pour identifier et déplacer "module DI" ou "module fondamental"
        matches = re.findall(r'[+(]?\s*(module DI|module fondamental)\s*[)+]?',
                             row['DIPLÔME COMPLEMENTAIRE'],
                             flags=re.IGNORECASE)
        cleaned_value = re.sub(r'[+(]?\s*(module DI|module fondamental)\s*[)+]?',
                               '', row['DIPLÔME COMPLEMENTAIRE'],
                               flags=re.IGNORECASE).strip()
        module_text = ' '.join(match for match in matches)
        if pd.notna(df.at[index, 'MODULE F ou MODULE DI']):
            df.at[index, 'MODULE F ou MODULE DI'] = df.at[index, 'MODULE F ou MODULE DI'] + ' ' + module_text
        else:
            df.at[index, 'MODULE F ou MODULE DI'] = module_text
        df.at[index, 'DIPLÔME COMPLEMENTAIRE'] = cleaned_value.strip()

        # Utilisation d'une expression régulière pour extraire le nombre après les termes "Ancienneté de service" ou "Ancienneté de fonctions"
        match = re.search(r'Ancienneté de service dans l\'enseignement d\'au moins \s*(\d+)', cleaned_value,
                          flags=re.IGNORECASE)
        if match:
            number = match.group(1)
            df.at[index, 'SERVICE'] = number

        match = re.search(r'Ancienneté de fonction d\'au moins \s*(\d+)', cleaned_value, flags=re.IGNORECASE)
        if match:
            number = match.group(1)
            df.at[index, 'FONCTION'] = number

        # Utilisation d'une expression régulière pour supprimer les phrases commençant par "Ancienneté" et se terminant par "statuts"
        match = re.search(r'Ancienneté[^.]*?statuts', cleaned_value, flags=re.IGNORECASE)
        if match:
            cleaned_value = re.sub(match.group(), '', cleaned_value, flags=re.IGNORECASE)
            cleaned_value = cleaned_value.strip()

        df.at[index, 'DIPLÔME COMPLEMENTAIRE'] = cleaned_value

modified_excel_file = 'TITRE_FINAL.xlsx'
df.to_excel(modified_excel_file, index=True)
