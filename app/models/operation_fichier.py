# =============================================================================
# Auteur  : GUIDJOU Danil
# Email   : danil.guidjou@etu.u-paris.fr
# Version : 1.0
# =============================================================================
import os
from pathlib import Path

from pydub import AudioSegment
from pydub.silence import detect_silence


def file_size_Mo(file_path):
    """Retourne la taille du fichier en Mo"""
    #getsize retourne la taille en octect 
    # 1Mo = 2^20 octet 
    return os.path.getsize(file_path) / pow(2, 20)

def reel_file_format(file_path):
    """"
    Retourne le vrai format d'un fichier
    """
    return Path(file_path).suffix.lstrip(".")


def file_size_ms(file_path):
    """Retroune le duree de l'audio en ms"""
    frmt = reel_file_format(file_path)
    return len(AudioSegment.from_file(file_path , format=frmt))

def file_size_sec(file_path):
    """Retourne la duree de l'audio en seconde"""
    #on charge l'audio dans AudioSegment ...
    #puis on obtient la durée en ms -> / 1000 pour l'obtenir en sec
    frmt = reel_file_format(file_path) 
    return ( len(AudioSegment.from_file(file_path , format=frmt)) / 1000)

def extract_audio_fmp4(file_pth):
    """"
    Extration d'un audio d'un fichier mp4
    je prends l'intiative de faire cette extration car un fichier mp3 est moins lourd qu'un fichier mp4 
    -> plus optimiser pour la transcription
    --> ca renvoit le nom du fichier dans le quel est stocker l'audio de cette mp4
    ---> il faut supprimer la convertion a la fin du traitement
    """
    output_name = "convertion.mp3"
    frmt = reel_file_format(file_pth)
    audio = AudioSegment.from_file(file_pth , format=frmt)
    audio.export(output_name, format="mp3")
    return  output_name

def detect_silnce_inInterval(audio):
    
    # on passe en parametre une segment dans les allentour ou on veut decouper l'audio
    # exemple si je veux decouper un audio chaque 5min -> 3000000ms 
    # donc on chereche le silence entre audio[29900 : 301000] 1s de reflection ou peutetre plus a voir avec les testes
    """
    cette fonction prend comme argument un segment d'un audio et retourne une liste de couple (debut, fin)
    de moment de silence dans le segment passer en parametre
    """
    #detection du silence
    # min_silence_len le temps minimale de silence 
    # silence_thresh le volume en db pour detecter le silence 
    # la durée min du silence est a 900ms et on defini -40db comme le seuil du silence
    # la durée du silence est a configurer par rapport aux tests a venir 
    # plus la durée est longue plus on est sur que la coupure est plus correcte !!! mais et si il ne ya pas de silence aussi long dans tout l'audio ? 
    return detect_silence(audio, min_silence_len=900, silence_thresh=-40)

    


def split_audio(file_path):
    """
    Decouper un fichier en plusieurs sous-fichiers de durée inferieurs a stocker dans le repertoir filleSpliter
    """
    #creation d'un  repertoire temporaire (on le suprime a fin de la transcrption ) pour stocker les fichier génerer
    output_dir = os.path.join(os.getcwd(), "fileSpliter")
    if not os.path.exists(output_dir):
        os.makedirs("fileSpliter")
    
    frmt = reel_file_format(file_path)
    audio = AudioSegment.from_file(file_path, format=frmt)
    
    duration = file_size_ms(file_path)  
    start = 0
    file_number = 0

    while start < duration:
        t1 = 290000 # init
        t2 = 310000 # init
        file_number += 1
        listSilence = []
        while(not listSilence):
            
            s1 = min(duration , start+t1) #debut de l'intarvalle ou on charche le silence
            s2 = min(duration , start+t2) #fin avec un intervalle de 20 seconde
            if(s1 == duration or s2 == duration): #si on atteint la fin de l'audio on a plus besoin de decouper on recupere juste la derniere partie 
                stop = 0
                break #puisque on est dans cette patie la listSilence =[] ==> TRUE ce qui provoque une boucle infini 
            else:
                listSilence = detect_silnce_inInterval(audio[s1: s2]) 
                temp1, temp2 = listSilence[0] #on recupere le premier moment de silence qui existe dans l'intervale [s1,S2]
                stop = ((temp1+temp2)//2) #on coup au millieu du silence 
                t2 += 10000 # si dans l'intervalle ou on cherche a decouper y a pas un moment de silence on augmente cette intervalle de 10sec

        end = min(duration , start+290000+ stop) #on decoupe l'audio en morceau de 5min -> 300sec -> 30000ms
        segement = audio[start:end]
        #enregitrement dans le repertoir fileSpliter
        file_dir = os.path.join(output_dir,f'{file_number}.mp3')
        print(file_dir)
        segement.export(file_dir, format=reel_file_format(file_path))
        start = end #actualise le debut pour la prochaine decoupe && condition de sortie de while
    
    #on retourne le nbr de fichier pour pouvoir les parcourir afin de faire de la transcription
    return file_number, output_dir