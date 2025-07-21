import os
import json

def create_python_installer_file():
    """
    Permet de créer un fichier .py
    pour télécharger un fichier depuis une URL (ex: Dropbox)
    Le lien et le nom du fichier sont intégrés directement dans le script généré.
    """
    print("\n--- Créer un fichier d'installation ---")
    file_name = input("Entrez le nom du fichier d'installation (ex: installer_mon_app.py): ").strip()
    if not file_name.endswith(".py"):
        file_name += ".py"

    # Demande l'URL et le nom du fichier de destination à l'utilisateur de l'application Gamma
    download_url = input("Entrez l'URL directe du fichier à télécharger un lien Dropbox : ").strip()
    destination_filename = input("Entrez le nom du fichier dropbox (ex: app.py/app.exe/app.zip): ").strip()

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
        print(f"\nFichier d'installation '{file_name}' créé avec succès")
    except IOError as e:
        print(f"Erreur lors de la création du fichier: {e}")

def main():
    """Fonction principale de l'application"""
    print("Bienvenue")
    while True:
        print("\n--- Menu Principal ---")
        print("1. Créer un fichier d'installation")
        print("2. Quitter")

        choice = input("Votre choix: ").strip()

        if choice == '1':
            create_python_installer_file()
        elif choice == '2':
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
