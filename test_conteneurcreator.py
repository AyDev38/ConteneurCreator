import platform
import subprocess
import pytest

# Test pour la détection du système d'exploitation
def test_detect_os():
    os = platform.system()
    assert os in ["Linux", "Windows"], f"Système non supporté : {os}"

# Test pour vérifier si Docker est installé
def test_check_docker_installed():
    try:
        result = subprocess.run(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        assert "Docker" in result.stdout.decode(), "Docker n'est pas installé ou accessible"
    except subprocess.CalledProcessError:
        pytest.fail("Commande Docker a échoué")
    except FileNotFoundError:
        pytest.fail("Commande Docker introuvable")

# Test pour la création d'un conteneur Docker
@pytest.mark.skipif(platform.system() != "Linux", reason="Test valable uniquement sur Linux")
def test_create_container():
    container_name = "test_container"
    try:
        # Création du conteneur
        result = subprocess.run(
            ["docker", "run", "--name", container_name, "-d", "ubuntu", "sleep", "5"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert result.returncode == 0, "Échec de la création du conteneur"
    finally:
        # Suppression du conteneur après le test
        subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Test pour vérifier si le service Docker est actif sur Linux
@pytest.mark.skipif(platform.system() != "Linux", reason="Test valable uniquement sur Linux")
def test_docker_service_active():
    try:
        result = subprocess.run(["systemctl", "is-active", "--quiet", "docker"], check=True)
        assert result.returncode == 0, "Le service Docker n'est pas actif"
    except subprocess.CalledProcessError:
        pytest.fail("Le service Docker n'est pas actif")
    except FileNotFoundError:
        pytest.fail("La commande systemctl n'est pas disponible sur ce système")

