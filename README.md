# Niri Wdisplays Sync

Questo tool colma il divario tra `wdisplays` e **Niri** (compositor Wayland), rendendo permanenti i layout degli schermi generati dinamicamente, garantendo anche un'integrazione perfetta con **linux-wallpaperengine**.

## Problema
Quando scolleghi o scambi un monitor, Niri resetta il layout oppure applica quello di default. Inoltre `linux-wallpaperengine` richiede nomi delle porte (`DP-1`, ecc.) per funzionare e, se queste vengono scambiate, lo sfondo sballa.

## Soluzione
Questo demone in Python:
1. Salva la posizione, risoluzione e configurazione di ogni schermo (in base al suo EDID hardware unico, indipendentemente dalla porta!).
2. Se un monitor viene disconnesso, se ne ricorda. Quando lo ricolleghi in un'altra porta, lo rimette subito nella sua posizione salvata.
3. Associa ad ogni monitor hardware un ID di sfondo specifico e rigenera al volo il comando corretto per `linux-wallpaperengine`, a prescindere da quale porta fisica sia connessa!

## Installazione
Clona la repository ed esegui lo script di installazione:
```bash
chmod +x install.sh
./install.sh
```

## Configurazione Sfondi
Per associare i tuoi schermi agli sfondi desiderati, prima dell'installazione apri `niri-wdisplays-sync.py` e aggiorna il dizionario `WALLPAPERS`:
```python
WALLPAPERS = {
    "Il Nome Del Tuo Schermo": "ID_WORKSHOP_STEAM",
}
```
Puoi trovare il "Nome" eseguendo `niri msg outputs` da terminale.
