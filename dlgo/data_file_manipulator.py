import json
import os
import uuid


def generate_filename(agent1_key, agent2_key, output_folder):
    agent1_key_no_spaces = agent1_key.replace(" ", "")
    agent2_key_no_spaces = agent2_key.replace(" ", "")
    unique_id = uuid.uuid4().hex[:3]
    filename = f'{agent1_key_no_spaces}_{agent2_key_no_spaces}_{unique_id}.json'
    return os.path.join(output_folder, filename)


def save_all_games_info(game_results, summary_info, agent1_key, agent2_key, output_folder):
    # Asumăm că funcția generate_filename a fost deja ajustată pentru a elimina spațiile și a include output_folder
    filename = generate_filename(agent1_key, agent2_key, output_folder)
    # Organizează datele într-un dicționar
    data_to_save = {
        "summary_info": summary_info,
        "game_details": game_results
    }
    with open(filename, 'w') as f:
        json.dump(data_to_save, f, indent=4)
    print("Saved record at ", filename)


def save_summary_info(summary_info, filename):
    # Verifică dacă fișierul de summary există și încarcă conținutul actual
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                existing_content = json.load(f)
            except json.JSONDecodeError:  # Dacă fișierul este gol sau corupt
                existing_content = []
    else:
        existing_content = []

    # Adaugă noile informații de summary la conținutul existent
    existing_content.append(summary_info)

    # Salvează înapoi tot conținutul actualizat în fișierul de summary
    with open(filename, 'w') as f:
        json.dump(existing_content, f, indent=4)
    print("Saved summary at ", filename)