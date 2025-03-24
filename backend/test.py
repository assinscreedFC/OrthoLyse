import json


def extraire_mapping_depuis_json(json_data):
    """
    Construit (texte_global, mapping_data)
    mapping_data = [(start_time, end_time, start_idx, end_idx), ...]

    - Ajuste correctement les timestamps `start` et `end` sur une échelle globale.
    - Calcule correctement les indices de début et de fin (`start_idx` et `end_idx`).
    """
    texte_global = ""
    mapping = []
    current_index = 0  # Index actuel dans le texte final
    offset_time = 0.0  # Décalage temporel global

    for bloc in json_data:
        segments = bloc.get("segments", [])

        for seg in segments:
            segment_text = seg.get("text", "").strip()  # Nettoie les espaces inutiles
            start_time = seg.get("start", 0.0) + offset_time  # Ajoute l'offset global
            end_time = seg.get("end", 0.0) + offset_time

            start_idx = current_index
            end_idx = current_index + len(segment_text)

            # Ajouter au mapping
            mapping.append((start_time, end_time, start_idx, end_idx))

            # Concaténer le texte
            texte_global += segment_text + " "  # Ajout d'un espace pour la lisibilité
            current_index = end_idx + 1

        # Mettre à jour l'offset avec le dernier `end` rencontré
        if segments:
            offset_time = mapping[-1][1]  # Dernier `end_time` utilisé

    return texte_global.strip(), mapping  # Enlever l’espace final

with open('videoplayback_transcription.json', 'r', encoding='utf-8') as fichier:
    # Charger le contenu du fichier JSON
    suffixes = json.load(fichier)

print(extraire_mapping_depuis_json(suffixes))