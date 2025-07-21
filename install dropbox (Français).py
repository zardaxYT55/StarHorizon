import os
import webbrowser # Gardé au cas où d'autres fonctionnalités l'utiliseraient à l'avenir, mais non utilisé directement pour l'installation ici.
import json # Gardé au cas où d'autres fonctionnalités l'utiliseraient à l'avenir, mais non utilisé directement pour l'installation ici.

def create_python_installer_file():
    """
    Permet à l'utilisateur de créer un fichier .py qui contient un script
    pour télécharger un fichier depuis une URL (ex: Dropbox) avec une barre de progression.
    Le lien et le nom du fichier sont intégrés directement dans le script généré.
    """
    print("\n--- Créer un fichier Python d'installation (Simple) ---")
    file_name = input("Entrez le nom du fichier Python d'installation (ex: installer_mon_app.py): ").strip()
    if not file_name.endswith(".py"):
        file_name += ".py"

    # Demande l'URL et le nom du fichier de destination à l'utilisateur de l'application Gamma
    download_url = input("Entrez l'URL directe du fichier à télécharger (ex: un lien Dropbox direct): ").strip()
    destination_filename = input("Entrez le nom du fichier de destination (ex: mon_logiciel.zip): ").strip()

    if not download_url or not destination_filename:
        print("L'URL et le nom du fichier de destination ne peuvent pas être vides. Annulation de la création du fichier.")
        return # Quitte la fonction si les entrées sont vides

    # Pour les liens Dropbox, assurez-vous que c'est un lien de téléchargement direct.
    # Souvent, cela signifie remplacer '?dl=0' par '?dl=1' ou similaire.
    if "dropbox.com" in download_url and "?dl=0" in download_url:
        download_url = download_url.replace("?dl=0", "?dl=1")
        print(f"URL Dropbox ajustée pour le téléchargement direct: {download_url}")
    elif "dropbox.com" in download_url and not ("?dl=1" in download_url or "&dl=1" in download_url):
        # Tente d'ajouter ?dl=1 si ce n'est pas déjà un lien direct
        if "?" in download_url:
            download_url += "&dl=1"
        else:
            download_url += "?dl=1"
        print(f"URL Dropbox ajustée pour le téléchargement direct: {download_url}")


    # Le code du script d'installation qui sera écrit dans le nouveau fichier .py
    # Les variables download_url et destination_filename sont maintenant intégrées directement.
    installer_code_content = f"""
import requests
import os
from tqdm import tqdm # Importe tqdm pour la barre de progression

def download_file_with_progress(url, destination_path):
    \"\"\"
    Télécharge un fichier depuis une URL donnée avec une barre de progression.
    Nécessite les bibliothèques 'requests' et 'tqdm'.
    \"\"\"
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Lève une exception pour les codes d'état HTTP d'erreur

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024 # 1 Kibibyte

        print(f"Téléchargement de: {{url}}")
        print(f"Vers: {{destination_path}}")

        # Initialise la barre de progression
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(destination_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("AVERTISSEMENT: La taille du téléchargement ne correspond pas à la taille attendue.")
        print("Téléchargement terminé avec succès!")

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion ou de requête: {{e}}")
    except IOError as e:
        print(f"Erreur d'écriture du fichier: {{e}}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {{e}}")

if __name__ == "__main__":
    installer_url = "{download_url}"
    installer_destination_filename = "{destination_filename}"

    if not installer_url or not installer_destination_filename:
        print("Erreur: L'URL ou le nom du fichier de destination est manquant dans le script.")
    else:
        download_file_with_progress(installer_url, installer_destination_filename)

    # Ajouté pour que la fenêtre se ferme seulement si l'utilisateur appuie sur une touche
    input("\\nAppuyez sur Entrée pour fermer cette fenêtre...")
"""

    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(installer_code_content)
        print(f"\nFichier d'installation '{file_name}' créé avec succès par l'application Gamma.")
    except IOError as e:
        print(f"Erreur lors de la création du fichier: {e}")

def create_python_multi_installer_file():
    """
    Permet à l'utilisateur de créer un fichier .py qui contient un script
    pour télécharger plusieurs fichiers depuis des URLs avec une barre de progression.
    Les liens et les noms des fichiers sont intégrés directement dans le script généré.
    """
    print("\n--- Créer un fichier Python d'installation (Multi-fichiers) ---")
    file_name = input("Entrez le nom du fichier Python d'installation (ex: installer_multi_app.py): ").strip()
    if not file_name.endswith(".py"):
        file_name += ".py"

    files_to_download_list = []
    while True:
        print(f"\n--- Fichier {len(files_to_download_list) + 1} à télécharger ---")
        file_url = input("Entrez l'URL directe du fichier (ex: un lien Dropbox direct; laissez vide pour terminer): ").strip()
        if not file_url:
            break

        destination_filename = input("Entrez le nom du fichier de destination: ").strip()
        if not destination_filename:
            print("Le nom du fichier de destination ne peut pas être vide. Veuillez réessayer.")
            continue

        # Applique les ajustements de lien Dropbox si cela ressemble à un
        if "dropbox.com" in file_url and "?dl=0" in file_url:
            file_url = file_url.replace("?dl=0", "?dl=1")
            print(f"URL Dropbox ajustée pour le téléchargement direct: {file_url}")
        elif "dropbox.com" in file_url and not ("?dl=1" in file_url or "&dl=1" in file_url):
            if "?" in file_url:
                file_url += "&dl=1"
            else:
                file_url += "?dl=1"
            print(f"URL Dropbox ajustée pour le téléchargement direct: {file_url}")
        print("Lien détecté comme lien direct (Dropbox ou autre).")

        files_to_download_list.append({'url': file_url, 'dest': destination_filename})

    if not files_to_download_list:
        print("Aucun fichier spécifié. Annulation de la création du fichier Multi-fichiers.")
        return

    # Convertir la liste en une chaîne JSON pour l'intégrer dans le script généré
    files_list_str = json.dumps(files_to_download_list, indent=4)

    # Le code du script d'installation Multi-fichiers qui sera écrit dans le nouveau fichier .py
    installer_code_content_multi = f"""
import requests
import os
import json
from tqdm import tqdm # Importe tqdm pour la barre de progression

def download_file_with_progress(url, destination_path):
    \"\"\"
    Nécessite les bibliothèques 'requests' et 'tqdm'.
    \"\"\"
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Lève une exception pour les codes d'état HTTP d'erreur

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024 # 1 Kibibyte

        print(f"Téléchargement de: {{url}}")
        print(f"Vers: {{destination_path}}")

        # Initialise la barre de progression
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(destination_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("AVERTISSEMENT: La taille du téléchargement ne correspond pas à la taille attendue.")
        print("Téléchargement terminé avec succès!")

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion ou de requête: {{e}}")
    except IOError as e:
        print(f"Erreur d'écriture du fichier: {{e}}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {{e}}")

if __name__ == "__main__":
    files_to_download = json.loads('''{files_list_str}''')

    if not files_to_download:
        print("Erreur: Aucune liste de fichiers à télécharger n'est présente dans le script.")
    else:
        for file_info in files_to_download:
            installer_url = file_info['url']
            installer_destination_filename = file_info['dest']

            if not installer_url or not installer_destination_filename:
                print(f"AVERTISSEMENT: URL ou nom de fichier de destination manquant pour l'entrée: {{file_info}}")
                continue
            download_file_with_progress(installer_url, installer_destination_filename)

    # Ajouté pour que la fenêtre se ferme seulement si l'utilisateur appuie sur une touche
    input("\\nAppuyez sur Entrée pour fermer cette fenêtre...")
"""
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(installer_code_content_multi)
        print(f"\nFichier d'installation '{file_name}' créé avec succès par l'application Gamma.")
    except IOError as e:
        print(f"Erreur lors de la création du fichier: {e}")

def main():
    """Fonction principale de l'application Gamma."""
    print("Bienvenue dans l'application GammA1a!")
    while True:
        print("\n--- Menu Principal ---")
        print("1. Créer un fichier Python d'installation (Simple)")
        print("2. Quitter")

        choice = input("Votre choix: ").strip()

        if choice == '1':
            create_python_installer_file()
        elif choice == '9999999999':
            create_python_multi_installer_file()
        elif choice == '2':
            print("Merci d'avoir utilisé Gamma. Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
