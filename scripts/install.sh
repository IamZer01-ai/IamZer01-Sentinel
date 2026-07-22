#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# IamZer01 Sentinel – Install Script (Dependencies + Setup)
# Version 1.0
# ═══════════════════════════════════════════════════════════

set -euo pipefail

echo "╔══════════════════════════════════════════╗"
echo "║   IamZer01 Sentinel — Install           ║"
echo "╚══════════════════════════════════════════╝"

# ── OS Detection ────────────────────────────────────────
OS="$(uname -s)"
ARCH="$(uname -m)"

echo "[*] Detected: $OS / $ARCH"

install_docker_debian() {
    echo "[*] Installing Docker (Debian/Ubuntu)..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | \
        sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') \
        $(lsb_release -cs) stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -qq
    sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo usermod -aG docker "$USER"
}

install_docker_macos() {
    echo "[*] Please install Docker Desktop for Mac from https://docs.docker.com/desktop/mac/install/"
    echo "    Or use: brew install --cask docker"
}

# ── Check / Install Docker ──────────────────────────────
if ! command -v docker &>/dev/null; then
    echo "[!] Docker not found. Attempting installation..."
    case "$OS" in
        Linux)
            if grep -qi "debian\|ubuntu" /etc/os-release 2>/dev/null; then
                install_docker_debian
            else
                echo "[-] Unsupported Linux distro. Install Docker manually."
                exit 1
            fi
            ;;
        Darwin)
            install_docker_macos
            exit 0
            ;;
        *)
            echo "[-] Unsupported OS. Install Docker manually."
            exit 1
            ;;
    esac
fi

echo "[*] Docker version: $(docker --version)"

# ── Configure environment ──────────────────────────────
if [ ! -f .env ]; then
    echo "[*] Creating .env from .env.example..."
    cp .env.example .env
    echo "[!] Edit .env with your settings before deploying."
fi

# Run deploy
bash "$(dirname "$0")/deploy.sh"
