# PDF Split 1→2 (Gauche/Droite)

Petit site web Flask permettant de **couper chaque page d'un PDF en deux pages** :  
- Moitié gauche → page 1  
- Moitié droite → page 2  

**Conversion vectorielle** via `pypdf` → **aucune perte de qualité** (pas de rasterisation).  
Prend en charge **plusieurs PDF** à la fois, téléchargement **individuel** ou **ZIP global**.

---

## ✨ Fonctionnalités
- **Upload multiple** de PDF (glisser-déposer ou sélection).
- Découpe **verticale** (gauche/droite).
- Conversion côté serveur (Flask + pypdf).
- Téléchargement des fichiers **un par un** ou **tous en ZIP**.
- Interface responsive et épurée.

---

## 📦 Installation locale

### 1. Cloner le dépôt
```bash
git clone https://github.com/<ton-utilisateur>/<nom-du-repo>.git
cd <nom-du-repo>
