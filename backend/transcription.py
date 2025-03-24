import whisper
import os
import shutil
import torch
from backend.operation_fichier import extract_audio_fmp4, file_size_Mo, file_size_sec, reel_file_format, split_audio

import whisper
import os
import shutil
import torch
import json
from backend.operation_fichier import (
    extract_audio_fmp4,
    file_size_Mo,
    file_size_sec,
    reel_file_format,
    split_audio
)

modele_dispo = ["base", "small", "medium", "turbo"]


def extraire_mapping_depuis_results(results):
    """
    Combine les segments de transcription provenant de plusieurs résultats (blocs)
    en un seul texte global et calcule le mapping avec gestion du décalage temporel.

    Retourne:
        tuple: (texte_global, mapping_data)
            texte_global (str): Le texte complet extrait de tous les blocs.
            mapping_data (list): Liste de tuples (adjusted_start, adjusted_end, start_idx, end_idx)
    """
    texte_global = ""
    mapping = []
    current_index = 0
    offset_time = 0.0

    # Pour chaque résultat de transcription (chaque bloc)
    for res in results:
        segments = res.get("segments", [])
        for seg in segments:
            segment_text = seg.get("text", "").strip()
            relative_start = seg.get("start", 0.0)
            relative_end = seg.get("end", 0.0)

            # Calculer les timestamps ajustés en ajoutant l'offset du bloc courant
            adjusted_start = relative_start + offset_time
            adjusted_end = relative_end + offset_time

            start_idx = current_index
            end_idx = current_index + len(segment_text)

            mapping.append((adjusted_start, adjusted_end, start_idx, end_idx))
            texte_global += segment_text + " "
            current_index = end_idx + 1  # +1 pour l'espace ajouté

        # Mettre à jour l'offset temporel pour le prochain bloc,
        # en ajoutant la durée totale du bloc actuel (le temps de fin du dernier segment)
        if segments:
            last_seg_end = segments[-1].get("end", 0.0)
            offset_time += last_seg_end

    return texte_global.strip(), mapping


def transcription(file_path, mdl):
    """
    Fonction qui retourne un dictionnaire avec le texte complet et le mapping des mots,
    en tenant compte du décalage temporel entre les différents blocs de transcription.

    Arguments :
        file_path (str): chemin du fichier
        mdl (int): indice du modèle dans ["base", "small", "medium", "turbo"]

    Retourne:
        dict: {"text": texte complet, "mapping": [(start_time, end_time, start_idx, end_idx), ...]}
    """
    useSplit = False
    useExtract = False
    fileNb = 0
    outDir = ""
    temp_file_name = ""
    dc = "cpu"  # par défaut sur CPU

    # Si le fichier est au format mp4, extraire l'audio pour alléger le fichier
    if reel_file_format(file_path) == "mp4":
        temp_file_name = file_path
        temp = extract_audio_fmp4(file_path)
        file_path = os.path.join(os.getcwd(), temp)
        useExtract = True

    # Si le fichier est trop volumineux (>25Mo ou >10min), le diviser en morceaux
    if file_size_Mo(file_path) > 25 or file_size_sec(file_path) > 600:
        fileNb, outDir = split_audio(file_path)
        useSplit = True

    # Vérifier si un GPU compatible est disponible
    if torch.cuda.is_available():
        dc = "cuda"
    elif torch.backends.mps.is_available():
        dc = "mps"

    # Charger le modèle Whisper demandé
    modele = whisper.load_model(modele_dispo[mdl], device=dc)

    results = []
    if useSplit:
        for i in range(1, fileNb + 1):
            temp_file_path = os.path.join(os.path.abspath(outDir), f'{i}.mp3')
            transcription_result = modele.transcribe(temp_file_path)
            results.append(transcription_result)
        shutil.rmtree(outDir)  # Nettoyer les fichiers temporaires
    else:
        transcription_result = modele.transcribe(file_path)
        results.append(transcription_result)

    # Si on a extrait l'audio d'un mp4, supprimer le fichier temporaire
    if useExtract:
        os.remove(file_path)
        file_path = temp_file_name

    # Combiner les résultats et gérer le décalage temporel
    texte_global, mapping_data = extraire_mapping_depuis_results(results)

    return {
        "text": texte_global,
        "mapping": mapping_data
    }


# Exemple d'utilisation
if __name__ == "__main__":
    result = transcription("./videoplayback.mp4", 0)
    print(json.dumps(result, ensure_ascii=False, indent=4))