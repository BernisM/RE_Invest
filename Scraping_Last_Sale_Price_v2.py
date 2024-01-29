import os
import requests

url = "https://www.meilleursagents.com/prix-immobilier/dvf/grenoble-38000/avenue-rhin-et-danube-1131337117/26/"
output_directory = r"C:\Users\massw\OneDrive\Bureau\Programmation\RE_Invest\RE_Invest"
output_filename = "page.html"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    output_path = os.path.join(output_directory, output_filename)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Enregistrée sous : {output_path}")
else:
    print(f"Error --> Code d'état HTTP : {response.status_code}")
