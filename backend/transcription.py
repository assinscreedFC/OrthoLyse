import whisper
import os
import shutil
import torch
from backend.operation_fichier import extract_audio_fmp4, file_size_Mo, file_size_sec, reel_file_format, split_audio

modele_dispo = ["base", "small", "medium", "turbo"]
def extraire_mapping_depuis_segments(segments):
    """
    Fonction qui retourne le texte global et le mapping des mots avec les indices.

    Arguments :
        segments (list): Liste de segments contenant les données "start", "end" et "text".

    Retourne :
        tuple: (texte_global, mapping_data)
            texte_global (str): Le texte complet extrait des segments.
            mapping_data (list): Liste de tuples (start_time, end_time, start_idx, end_idx) pour chaque mot.
    """
    texte_global = ""
    mapping = []
    current_index = 0  # Index actuel dans le texte global

    for seg in segments:
        segment_text = seg.get("text", "").strip()  # Nettoie les espaces inutiles
        start_time = seg.get("start", 0.0)  # Temps de début du segment
        end_time = seg.get("end", 0.0)  # Temps de fin du segment

        words = segment_text.split()  # Diviser le texte en mots

        # Calculer la durée totale de l'audio de ce segment
        duration = end_time - start_time

        # Diviser la durée par le nombre de mots pour obtenir la durée par mot
        word_duration = duration / len(words) if words else 0

        for i, word in enumerate(words):
            word_start_time = start_time + word_duration * i
            word_end_time = word_start_time + word_duration

            start_idx = current_index
            end_idx = current_index + len(word)

            # Ajouter au mapping
            mapping.append((word_start_time, word_end_time, start_idx, end_idx))

            # Concaténer le texte
            texte_global += word + " "  # Ajout d'un espace pour la lisibilité
            current_index = end_idx + 1

    return texte_global.strip(), mapping


def transcription(file_path, mdl):
    """
    Fonction qui retourne un dictionnaire avec le texte complet et le mapping des mots.

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

    # Si le fichier est trop volumineux ( >25Mo ou >10min), le diviser en morceaux
    if file_size_Mo(file_path) > 25 or file_size_sec(file_path) > 600:
        fileNb, outDir = split_audio(file_path)
        useSplit = True

    # Vérifier si un GPU compatible est disponible
    if torch.cuda.is_available():
        dc = "cuda"
    elif torch.backends.mps.is_available():
        dc = "mps"

    # Charger le modèle Whisper demandé par l'utilisateur
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

    # Si on a extrait l'audio d'un fichier mp4, supprimer le fichier temporaire
    if useExtract:
        os.remove(file_path)
        file_path = temp_file_name

    # Combiner tous les segments en un seul tableau
    combined_segments = []
    for res in results:
        for seg in res.get("segments", []):
            combined_segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip()
            })

    # Obtenir le texte complet et le mapping des mots
    texte_global, mapping_data = extraire_mapping_depuis_segments(combined_segments)

    return {
        "text": texte_global,
        "mapping": mapping_data
    }

# Exemple d'utilisation
if __name__ == "__main__":
    result = transcription("./videoplayback.mp4", 0)
    print(result["text"])  # Texte complet
    print(result["mapping"])  # Mapping des mots
