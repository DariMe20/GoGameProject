import datetime
import json
import os


def generate_filename(agent1_key, agent2_key, output_folder, episode_count):
    agent1_key_no_spaces = agent1_key.replace(" ", "")
    agent2_key_no_spaces = agent2_key.replace(" ", "")
    # Obținem data și ora curentă în formatul dorit
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Construim numele fișierului folosind numărul episoadelor, data și ora
    filename = f'{episode_count}_{agent1_key_no_spaces}_{agent2_key_no_spaces}_{date_time_str}.json'
    return os.path.join(output_folder, filename)


def save_all_games_info(game_results, summary_info, agent1_key, agent2_key, output_folder, episode_count):
    # Asumăm că funcția generate_filename a fost deja ajustată pentru a elimina spațiile și a include output_folder
    filename = generate_filename(agent1_key, agent2_key, output_folder, episode_count)
    # Organizează datele într-un dicționar
    data_to_save = {
        "summary_info": summary_info,
        "game_details": game_results
    }
    with open(filename, 'w') as f:
        json.dump(data_to_save, f, indent=4)
    print("Saved record at ", filename)


def save_summary_info(summary_info, filename, experience_filename):
    # Verifică dacă fișierul de summary există și încarcă conținutul actual
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                existing_content = json.load(f)
            except json.JSONDecodeError:  # Dacă fișierul este gol sau corupt
                existing_content = []
    else:
        existing_content = []

        # Determină numărul următorului antrenament pe baza numărului de intrări existente
    evaluation_no = len(existing_content) + 1
    summary_info["SUMMARY_NUMBER"] = evaluation_no
    summary_info["Generated Experience File"] = experience_filename

    # Adaugă noile informații de summary la conținutul existent
    existing_content.append(summary_info)

    # Salvează înapoi tot conținutul actualizat în fișierul de summary
    with open(filename, 'w') as f:
        json.dump(existing_content, f, indent=4)
    print("Saved summary at ", filename)


def save_training_details(training_details, filename):
    # Verifică dacă fișierul există pentru a încărca detalii existente
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                existing_details = json.load(f)
                # Asigură-te că existing_details este o listă
                if not isinstance(existing_details, list):
                    existing_details = []
            except json.JSONDecodeError:  # Dacă fișierul este gol sau corupt
                existing_details = []
    else:
        existing_details = []

    # Determină numărul următorului antrenament pe baza numărului de intrări existente
    training_no = len(existing_details) + 1
    training_details["Training_number"] = training_no

    # Adaugă noile detalii de antrenament la lista de detalii existente
    existing_details.append(training_details)

    # Salvează toate detaliile (vechi + nouă) înapoi în fișier
    with open(filename, 'w') as f:
        json.dump(existing_details, f, indent=4)
    print(f"Added Training no: {training_no} to {filename}")


def generate_experience_filename(output_folder, agent1_key, agent2_key, base_name="AgentExperience"):
    agent1_key_no_spaces = agent1_key.replace(" ", "")
    agent2_key_no_spaces = agent2_key.replace(" ", "")
    files = os.listdir(output_folder)
    matching_files = [f for f in files if f.startswith(base_name) and f.endswith(".h5")]

    numbers = [int(f[len(base_name):f.rfind(".")]) for f in matching_files if f[len(base_name):f.rfind(".")].isdigit()]
    next_number = max(numbers) + 1 if numbers else 1

    new_filename = f"{base_name}{next_number}_{agent1_key_no_spaces}_{agent2_key_no_spaces}.h5"

    return os.path.join(output_folder, new_filename)


def save_all_episodes_info(new_episodes_info, output_folder, base_filename="all_episodes_info"):
    # Generează numele fișierului bazat pe un nume de bază constant
    filename = f'{base_filename}.json'
    filepath = os.path.join(output_folder, filename)

    # Verifică dacă fișierul există deja
    if os.path.exists(filepath):
        # Încarcă conținutul existent
        with open(filepath, 'r') as f:
            try:
                existing_content = json.load(f)
            except json.JSONDecodeError:
                # Dacă fișierul este corupt sau gol, inițializează un nou dicționar
                existing_content = {"all_episodes_info": []}
    else:
        existing_content = {"all_episodes_info": []}

    # Calculează numărul de start pentru noile episoade
    start_episode_number = len(existing_content["all_episodes_info"]) + 1

    # Actualizează numărul fiecărui episod nou și adaugă-l la lista existentă
    updated_episodes_info = []
    for index, episode_info in enumerate(new_episodes_info, start=start_episode_number):
        episode_info[
            'episode_number'] = index  # Presupunând că fiecare element din `new_episodes_info` este un dicționar
        updated_episodes_info.append(episode_info)

    # Adaugă noile episoade actualizate la conținutul existent
    existing_content["all_episodes_info"].extend(updated_episodes_info)

    # Scrie înapoi tot conținutul (existent + nou) în fișier
    with open(filepath, 'w') as f:
        json.dump(existing_content, f, indent=4)

    print(f"All episodes info saved or updated at {filepath}")
