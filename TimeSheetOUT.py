from datetime import datetime, timedelta

# --- Fonction pour calculer l'heure de sortie ---
def calcul_sortie(entree_str, travail_heures=8, pause_minutes=30):
    """
    Calcule l'heure de sortie
    :param entree_str: heure d'entrée "HH:MM"
    :param travail_heures: nombre d'heures de travail
    :param pause_minutes: durée de pause à soustraire
    :return: heure de sortie "HH:MM"
    """
    entree = datetime.strptime(entree_str, "%H:%M")
    
    # Durée totale à passer au bureau = travail + pause
    duree_totale = timedelta(hours=travail_heures) + timedelta(minutes=pause_minutes)
    
    # Heure de sortie
    sortie = entree + duree_totale
    return sortie.strftime("%H:%M")

# --- Interface utilisateur ---
print("Calculateur d'heure de sortie (8h de travail + 30 min pause)")
entree = input("Entrez votre heure d'entrée le matin (HH:MM) : ")

sortie = calcul_sortie(entree)
print(f"Vous devez sortir à : {sortie}")
