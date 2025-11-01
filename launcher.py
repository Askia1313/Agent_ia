"""
Script de lancement complet du système RAG
Lance le backend Django, le frontend Vue.js et charge les données
"""

import subprocess
import sys
import os
import time
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Affiche un en-tête"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_info(text):
    """Affiche un message d'information"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def print_warning(text):
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    """Affiche une erreur"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def check_file_exists(filepath, name):
    """Vérifie qu'un fichier existe"""
    if not os.path.exists(filepath):
        print_error(f"{name} non trouvé: {filepath}")
        return False
    print_success(f"{name} trouvé")
    return True

def check_directory_exists(dirpath, name):
    """Vérifie qu'un répertoire existe"""
    if not os.path.isdir(dirpath):
        print_error(f"Répertoire {name} non trouvé: {dirpath}")
        return False
    print_success(f"Répertoire {name} trouvé")
    return True

def main():
    print_header("🚀 SYSTÈME RAG - LAUNCHER")
    
    # Obtenir le répertoire courant
    base_dir = Path(__file__).parent
    print_info(f"Répertoire de base: {base_dir}")
    
    # ============ VÉRIFICATIONS ============
    print_header("📋 VÉRIFICATION DES FICHIERS")
    
    all_good = True
    
    # Vérifier les fichiers essentiels
    files_to_check = [
        (base_dir / "agent_ia.py", "Script agent_ia.py"),
        (base_dir / "urls.txt", "Fichier urls.txt"),
        (base_dir / "Backend_ia" / "manage.py", "Django manage.py"),
        (base_dir / "Frontend" / "package.json", "Frontend package.json"),
    ]
    
    for filepath, name in files_to_check:
        if not check_file_exists(filepath, name):
            all_good = False
    
    # Vérifier les répertoires
    dirs_to_check = [
        (base_dir / "pdf", "Dossier PDF"),
        (base_dir / "Backend_ia", "Dossier Backend"),
        (base_dir / "Frontend", "Dossier Frontend"),
    ]
    
    for dirpath, name in dirs_to_check:
        if not check_directory_exists(dirpath, name):
            all_good = False
    
    if not all_good:
        print_error("Certains fichiers ou répertoires sont manquants!")
        sys.exit(1)
    
    # ============ MENU ============
    print_header("📌 OPTIONS DE LANCEMENT")
    # print(f"{Colors.CYAN}1{Colors.END} - Charger les données (PDFs + Web scraping)")  # COMMENTÉ - Base de données déjà prête
    print(f"{Colors.CYAN}1{Colors.END} - Lancer le backend Django")
    print(f"{Colors.CYAN}2{Colors.END} - Lancer le frontend Vue.js")
    print(f"{Colors.CYAN}3{Colors.END} - Lancer tout (backend + frontend)")
    print(f"{Colors.CYAN}4{Colors.END} - Quitter")
    print()
    print_info("Note: La base de données est déjà chargée")
    print()
    
    choice = input(f"{Colors.BOLD}Choisissez une option (1-4): {Colors.END}").strip()
    
    if choice == "1":
        launch_backend(base_dir)
    elif choice == "2":
        launch_frontend(base_dir)
    elif choice == "3":
        # load_data(base_dir)  # COMMENTÉ - Base de données déjà prête
        # print_info("Attente de 3 secondes avant de lancer le backend...")
        # time.sleep(3)
        launch_backend_and_frontend(base_dir)
    elif choice == "4":
        print_info("Au revoir!")
        sys.exit(0)
    else:
        print_error("Option invalide!")
        sys.exit(1)

def load_data(base_dir):
    """Charge les données (PDFs + Web scraping)"""
    print_header("📥 CHARGEMENT DES DONNÉES")
    
    agent_script = base_dir / "agent ia.py"
    
    # ============ VÉRIFIER ET INSTALLER LES REQUIREMENTS ============
    print_info("Vérification des dépendances Python...")
    
    # Dépendances requises pour agent ia.py
    required_packages = [
        'sentence-transformers',
        'chromadb',
        'pypdf',
        'requests',
        'beautifulsoup4'
    ]
    
    missing_packages = []
    
    # Vérifier chaque package
    for package in required_packages:
        try:
            # Convertir le nom du package pour l'import
            import_name = package.replace('-', '_')
            if package == 'beautifulsoup4':
                import_name = 'bs4'
            elif package == 'pypdf':
                import_name = 'PyPDF2'
            
            __import__(import_name)
            print_success(f"Package {package} trouvé")
        except ImportError:
            print_warning(f"Package {package} manquant")
            missing_packages.append(package)
    
    # Installer les packages manquants
    if missing_packages:
        print_warning(f"Installation de {len(missing_packages)} package(s) manquant(s)...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install"] + missing_packages,
                check=True
            )
            print_success("Tous les packages ont été installés")
        except subprocess.CalledProcessError:
            print_error("Erreur lors de l'installation des packages")
            sys.exit(1)
    else:
        print_success("Toutes les dépendances sont installées")
    
    print()
    print_info("Démarrage du chargement des données...")
    print_info("Cela peut prendre plusieurs minutes...")
    print()
    
    try:
        # Lancer le script agent ia.py
        result = subprocess.run(
            [sys.executable, str(agent_script)],
            cwd=base_dir,
            check=False
        )
        
        if result.returncode == 0:
            print_success("Données chargées avec succès!")
        else:
            print_error("Erreur lors du chargement des données")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        sys.exit(1)

def launch_backend(base_dir):
    """Lance le backend Django"""
    print_header("🔧 LANCEMENT DU BACKEND DJANGO")
    
    backend_dir = base_dir / "Backend_ia"
    
    print_info("Vérification des dépendances...")
    
    # Vérifier si les dépendances sont installées
    try:
        import django
        import corsheaders
        print_success("Dépendances Django trouvées")
    except ImportError:
        print_warning("Installation des dépendances...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=backend_dir,
            check=True
        )
        print_success("Dépendances installées")
    
    print_info("Démarrage du serveur Django...")
    print_info("Accédez à: http://localhost:8000")
    print_info("Appuyez sur Ctrl+C pour arrêter")
    print()
    
    try:
        subprocess.run(
            [sys.executable, "manage.py", "runserver"],
            cwd=backend_dir,
            check=False
        )
    except KeyboardInterrupt:
        print_info("Serveur Django arrêté")
    except Exception as e:
        print_error(f"Erreur: {e}")
        sys.exit(1)

def launch_frontend(base_dir):
    """Lance le frontend Vue.js"""
    print_header("🎨 LANCEMENT DU FRONTEND VUE.JS")
    
    frontend_dir = base_dir / "Frontend"
    
    print_info("Vérification des dépendances...")
    
    # Vérifier si node_modules existe
    if not (frontend_dir / "node_modules").exists():
        print_warning("Installation des dépendances npm...")
        try:
            # Vérifier si npm est disponible
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                print_success(f"npm version {result.stdout.strip()} détecté")
                subprocess.run(
                    ["npm", "install"],
                    cwd=frontend_dir,
                    check=True,
                    shell=True
                )
                print_success("Dépendances npm installées")
            else:
                print_error("npm n'est pas accessible!")
                print_info("Vérifiez que Node.js est dans le PATH")
                sys.exit(1)
        except Exception as e:
            print_error(f"Erreur npm: {e}")
            print_info("Téléchargez Node.js depuis: https://nodejs.org/")
            sys.exit(1)
    else:
        print_success("Dépendances npm trouvées")
    
    print_info("Démarrage du serveur Vite...")
    print_info("Accédez à: http://localhost:5173")
    print_info("Appuyez sur Ctrl+C pour arrêter")
    print()
    
    try:
        subprocess.run(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            check=False,
            shell=True
        )
    except KeyboardInterrupt:
        print_info("Serveur Vite arrêté")
    except Exception as e:
        print_error(f"Erreur: {e}")
        sys.exit(1)

def launch_backend_and_frontend(base_dir):
    """Lance le backend et le frontend en parallèle"""
    print_header("🚀 LANCEMENT DU SYSTÈME COMPLET")
    
    backend_dir = base_dir / "Backend_ia"
    frontend_dir = base_dir / "Frontend"
    
    # Vérifier et installer les dépendances
    print_info("Vérification des dépendances...")
    
    # Django
    try:
        import django
        import corsheaders
        print_success("Dépendances Django trouvées")
    except ImportError:
        print_warning("Installation des dépendances Django...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=backend_dir,
            check=True
        )
        print_success("Dépendances Django installées")
    
    # NPM
    if not (frontend_dir / "node_modules").exists():
        print_warning("Installation des dépendances npm...")
        try:
            # Vérifier si npm est disponible
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                print_success(f"npm version {result.stdout.strip()} détecté")
                subprocess.run(
                    ["npm", "install"],
                    cwd=frontend_dir,
                    check=True,
                    shell=True
                )
                print_success("Dépendances npm installées")
            else:
                print_error("npm n'est pas accessible!")
                print_info("Vérifiez que Node.js est dans le PATH")
                sys.exit(1)
        except Exception as e:
            print_error(f"Erreur npm: {e}")
            print_info("Téléchargez Node.js depuis: https://nodejs.org/")
            sys.exit(1)
    else:
        print_success("Dépendances npm trouvées")
    
    print_header("✅ DÉMARRAGE DES SERVEURS")
    
    print_info("Démarrage du backend Django...")
    print_info("Les logs s'afficheront ci-dessous...")
    print()
    
    # Démarrer le backend en mode interactif (sans redirection)
    backend_process = subprocess.Popen(
        [sys.executable, "manage.py", "runserver"],
        cwd=backend_dir
    )
    print_success("Backend Django démarré (PID: {})".format(backend_process.pid))
    
    # Attendre que le backend soit prêt
    print_info("Attente de 5 secondes pour que le backend démarre...")
    time.sleep(5)
    
    print()
    print_info("Démarrage du frontend Vue.js...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        shell=True
    )
    print_success("Frontend Vue.js démarré (PID: {})".format(frontend_process.pid))
    
    print()
    print_header("🎉 SYSTÈME PRÊT")
    print(f"{Colors.GREEN}Backend:  http://localhost:8000{Colors.END}")
    print(f"{Colors.GREEN}Frontend: http://localhost:5173{Colors.END}")
    print(f"{Colors.GREEN}API:      http://localhost:8000/api/question/{Colors.END}")
    print()
    print_info("Appuyez sur Ctrl+C pour arrêter tous les serveurs")
    print()
    
    try:
        # Garder les processus actifs
        backend_process.wait()
    except KeyboardInterrupt:
        print()
        print_info("Arrêt des serveurs...")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Attendre que les processus se terminent
        try:
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
        
        print_success("Tous les serveurs ont été arrêtés")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("Lancement annulé")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erreur inattendue: {e}")
        sys.exit(1)
