"""
Modulo di Simulazione Geometrico-Computazionale.
Sviluppato per lo studio delle singolarità nella progressione Area/Somma.
Autore d'Invenzione: Mc84 (Mario Cera)
Codice conforme alle specifiche di stile PEP 8 e ottimizzato per Ruff.
"""

import os

import matplotlib.pyplot as plt


def pulisci_schermo():
    """Ripulisce il terminale di comando in base al sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def richiedi_input_numerico(messaggio, consente_avviso_passi=False):
    """
    Richiede un input all'utente garantendo che sia un numero valido.
    Se consente_avviso_passi è True, avverte l'utente sui rischi dei grandi numeri.
    """
    while True:
        try:
            valore = float(input(messaggio))
            if valore <= 0:
                print("[Errore] Inserire un valore maggiore di zero.")
                continue

            if consente_avviso_passi and valore > 25:
                print(f"\n[ATTENZIONE] Hai inserito {int(valore)} iterazioni.")
                print("Con moltiplicatori alti, i numeri diventeranno astronomici.")
                conferma = input("Vuoi procedere comunque? (s/n): ").lower()
                if conferma != "s":
                    print("Inserimento annullato. Riprova.")
                    continue

            return valore
        except ValueError:
            print("[Errore] Input non valido. Inserire solo cifre numeriche.")


def esegui_simulazione(larghezza_ini, lunghezza_ini, moltiplicatore, passi):
    """
    Esegue l'algoritmo iterativo raccogliendo i dati geometrici.
    Accetta qualsiasi numero di passi definito in input dall'utente.
    """
    dati = []
    larghezza = larghezza_ini
    lunghezza = lunghezza_ini

    for n in range(1, passi + 1):
        larghezza_corr = larghezza * moltiplicatore
        lunghezza_corr = lunghezza * moltiplicatore

        somma = larghezza_corr + lunghezza_corr
        area = larghezza_corr * lunghezza_corr
        divisione = area / somma if somma != 0 else 0.0

        dati.append(
            {
                "iterazione": n,
                "larghezza": larghezza_corr,
                "lunghezza": lunghezza_corr,
                "somma": somma,
                "area": area,
                "divisione": divisione,
            }
        )

        larghezza = larghezza_corr
        lunghezza = lunghezza_corr

    return dati


def stampa_tabella_terminale(dati):
    """Visualizza i dati calcolati in una tabella formattata a video."""
    separatore = "-" * 90
    print(
        f"\n{'Iterazione':<12} | {'Larghezza':<12} | {'Lunghezza':<12} | "
        f"{'Somma':<12} | {'Area':<16} | {'Div. Area/Somma':<16}"
    )
    print(separatore)

    for riga in dati:
        print(
            f"{riga['iterazione']:<12} | "
            f"{riga['larghezza']:<12.1f} | "
            f"{riga['lunghezza']:<12.1f} | "
            f"{riga['somma']:<12.1f} | "
            f"{riga['area']:<16.1f} | "
            f"{riga['divisione']:<16.4f}"
        )
    print(separatore)


def esporta_file_csv(dati, nome_file="serie_moltiplicatore.csv"):
    """Esporta i dati in un file CSV ottimizzato per Microsoft Excel Italiano."""
    try:
        with open(nome_file, "w", encoding="utf-8") as file:
            file.write(
                "Iterazione;Larghezza;Lunghezza;Somma;Area;Divisione Area/Somma\n"
            )
            for riga in dati:
                l_str = str(riga["larghezza"]).replace(".", ",")
                lu_str = str(riga["lunghezza"]).replace(".", ",")
                s_str = str(riga["somma"]).replace(".", ",")
                a_str = str(riga["area"]).replace(".", ",")
                d_str = str(riga["divisione"]).replace(".", ",")

                file.write(
                    f"{riga['iterazione']};{l_str};{lu_str};{s_str};{a_str};{d_str}\n"
                )
        print(f"[INFO] File Excel salvato con successo: '{nome_file}'")
    except OSError as e:
        print(f"[Errore] Impossibile scrivere il file su disco: {e}")


def genera_grafici(dati):
    """Genera e mostra il pannello grafico potenziato per la massima leggibilità scientifica."""
    passi = [riga["iterazione"] for riga in dati]
    aree = [riga["area"] for riga in dati]
    divisioni = [riga["divisione"] for riga in dati]
    tot_passi = len(passi)

    # Impostazione stile grafico ad alta leggibilità
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    fig.suptitle(
        "IL PRINCIPIO DI RISONANZA DI OLOGRAFIA BIDIMENSIONALE (Autore: Mc84)",
        fontsize=14,
        fontweight="bold",
        color="darkblue",
        y=0.96,
    )

    # --- GRAFICO 1: EVOLUZIONE ESPONENZIALE DELL'AREA ---
    ax1.plot(
        passi, aree, marker="o", color="crimson", linewidth=2.5, label="Area Rettangolo"
    )
    ax1.set_title(
        "Invarianza Frattale dello Spazio Interno",
        fontsize=11,
        fontweight="bold",
        pad=10,
    )
    ax1.set_xlabel("Iterazione (n)", fontsize=10)
    ax1.set_ylabel("Spazio Bidimensionale (Scala Log)", fontsize=10)
    ax1.set_yscale("log")
    ax1.grid(True, which="both", linestyle=":", alpha=0.6)

    # Etichette numeriche sul grafico dell'Area (Inizio e Fine)
    ax1.annotate(
        f"{aree[0]:.1e}",
        (passi[0], aree[0]),
        textcoords="offset points",
        xytext=(10, -5),
        ha="left",
        fontsize=9,
        fontweight="bold",
        color="darkred",
    )
    ax1.annotate(
        f"{aree[-1]:.1e}",
        (passi[-1], aree[-1]),
        textcoords="offset points",
        xytext=(-15, 10),
        ha="right",
        fontsize=9,
        fontweight="bold",
        color="darkred",
    )
    ax1.legend(loc="upper left")

    # --- GRAFICO 2: PROGRESSIONE DEL RAPPORTO (AREA / SOMMA) ---
    ax2.plot(
        passi,
        divisioni,
        marker="s",
        color="royalblue",
        linewidth=2.5,
        label="Rapporto Area/Somma",
    )
    ax2.set_title(
        "La Singolarità Critica del Confine", fontsize=11, fontweight="bold", pad=10
    )
    ax2.set_xlabel("Iterazione (n)", fontsize=10)
    ax2.set_ylabel("Rapporto Lineare Risultante", fontsize=10)
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Etichette numeriche nei 3 punti di controllo strategici per la leggibilità dello Shift-2
    # 1. Punto iniziale
    ax2.annotate(
        f"{divisioni[0]:.1f}",
        (passi[0], divisioni[0]),
        textcoords="offset points",
        xytext=(5, 10),
        ha="left",
        fontsize=9,
        fontweight="bold",
        color="navy",
    )

    # 2. Punto di rottura (se ci sono abbastanza passi, indicativamente a 3/4 della serie)
    if tot_passi >= 25:
        p_rottura = int(tot_passi * 0.8) - 1
        ax2.annotate(
            f"{divisioni[p_rottura]:.1e}",
            (passi[p_rottura], divisioni[p_rottura]),
            textcoords="offset points",
            xytext=(-15, -15),
            ha="right",
            fontsize=9,
            fontweight="bold",
            color="navy",
            arrowprops=dict(arrowstyle="->", color="blue", alpha=0.5),
        )

    # 3. Punto di picco finale
    ax2.annotate(
        f"{divisioni[-1]:.1e}",
        (passi[-1], divisioni[-1]),
        textcoords="offset points",
        xytext=(-15, 10),
        ha="right",
        fontsize=9,
        fontweight="bold",
        color="navy",
    )

    ax2.legend(loc="upper left")

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    print("[INFO] Apertura del pannello grafico ad alta leggibilità in corso...")
    plt.savefig("grafico_olografia_mc84.png", dpi=300, bbox_inches="tight")
    plt.show()


def main():
    """Funzione pilota dell'intero flusso del programma."""
    pulisci_schermo()
    print("=" * 65)
    print("   LABORATORIO COMPUTAZIONALE DI OLOGRAFIA GEOMETRICA (Mc84)   ")
    print("=" * 65)

    larg_iniziale = richiedi_input_numerico("Inserisci la larghezza iniziale (es. 2): ")
    lung_iniziale = richiedi_input_numerico("Inserisci la lunghezza iniziale (es. 3): ")
    moltiplicatore = richiedi_input_numerico("Inserisci il moltiplicatore (es. 5): ")

    iterazioni = int(
        richiedi_input_numerico(
            "Inserisci il numero di iterazioni desiderate (es. 30): ",
            consente_avviso_passi=True,
        )
    )

    risultati = esegui_simulazione(
        larg_iniziale, lung_iniziale, moltiplicatore, iterazioni
    )

    stampa_tabella_terminale(risultati)
    esporta_file_csv(risultati)
    genera_grafici(risultati)


if __name__ == "__main__":
    main()
