"""
LABORATORIO DI ANALISI DEGLI ERRORI DI ARROTONDAMENTO E DERIVA COMPUTAZIONALE v3.0.0
Studio delle singolarità numeriche nella progressione geometrica Area/Perimetro.
Confronto analitico: Standard Hardware IEEE 754 vs Precisione Arbitraria (Decimal).
Sviluppo e Firma Scientifica: Mc84 (Mario Cera) - Anno 2026
"""

import os
from decimal import Decimal, getcontext

import matplotlib.pyplot as plt

# =====================================================================
# CONFIGURAZIONE STRUMENTI COMPUTAZIONALI E REQUISITI DI PRECISIONE
# =====================================================================
# Impostazione della precisione assoluta a 100 cifre per il sistema di riferimento
getcontext().prec = 100


def pulisci_schermo():
    """Ripulisce il terminale di comando in base al sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def richiedi_input_numerico(messaggio, consente_avviso_passi=False):
    """
    Richiede un input all'utente garantendo che sia un numero valido.
    Previene l'inserimento di valori negativi o nulli distruttivi per l'algoritmo.
    """
    while True:
        try:
            valore = float(input(messaggio))
            if valore <= 0:
                print("[Errore] Inserire un valore maggiore di zero.")
                continue

            if consente_avviso_passi and valore > 45:
                print(f"\n[ATTENZIONE] Hai inserito {int(valore)} iterazioni.")
                print(
                    "Con moltiplicatori alti, i numeri diventeranno astronomici ed esploderanno."
                )
                conferma = input("Vuoi procedere comunque? (s/n): ").lower()
                if conferma != "s":
                    print("Inserimento annullato. Riprova.")
                    continue

            return valore
        except ValueError:
            print("[Errore] Input non valido. Inserire solo cifre numeriche.")


def esegui_simulazione_fourier_analog(
    larghezza_ini, lunghezza_ini, moltiplicatore, passi
):
    """
    Risolve la progressione geometrica in parallelo su due motori di calcolo distinti:
    1. IEEE 754 standard in virgola mobile (Soggetto a deriva hardware).
    2. Decimal a 100 cifre (Riferimento asintotico a precisione infinita).
    """
    dati = []

    # Inizializzazione variabili per il motore float (IEEE 754)
    w_flt = float(larghezza_ini)
    l_flt = float(lunghezza_ini)
    m_flt = float(moltiplicatore)

    # Inizializzazione variabili per il motore Decimal (Precisione Arbitraria)
    w_dec = Decimal(str(larghezza_ini))
    l_dec = Decimal(str(lunghezza_ini))
    m_dec = Decimal(str(moltiplicatore))

    for n in range(1, passi + 1):
        # Avanzamento geometrico dei registri hardware
        w_flt *= m_flt
        l_flt *= m_flt
        somma_flt = w_flt + l_flt
        area_flt = w_flt * l_flt
        div_flt = area_flt / somma_flt if somma_flt != 0.0 else 0.0

        # Avanzamento geometrico a precisione infinita
        w_dec *= m_dec
        l_dec *= m_dec
        somma_dec = w_dec + l_dec
        area_dec = w_dec * l_dec
        div_dec = (
            area_dec / somma_dec if somma_dec != Decimal("0.0") else Decimal("0.0")
        )

        # Calcolo dell'errore relativo reale causato dalla cancellazione della mantissa
        div_dec_f = float(div_dec)
        errore_relativo = (
            abs(div_flt - div_dec_f) / div_dec_f if div_dec_f != 0.0 else 0.0
        )

        dati.append(
            {
                "iterazione": n,
                "larghezza_flt": w_flt,
                "lunghezza_flt": l_flt,
                "somma_flt": somma_flt,
                "area_flt": area_flt,
                "divisione_flt": div_flt,
                "errore_computazionale": errore_relativo,
            }
        )

    return dati


def stampa_tabella_terminale(dati):
    """Visualizza i dati calcolati in una tabella ingegneristica standard."""
    separatore = "-" * 115
    print(
        f"\n{'Iterazione':<12} | {'Larghezza (F)':<14} | {'Lunghezza (F)':<14} | "
        f"{'Area (F)':<16} | {'Div. Area/Somma':<16} | {'Errore IEEE 754':<18}"
    )
    print(separatore)

    for riga in dati:
        print(
            f"{riga['iterazione']:<12} | "
            f"{riga['larghezza_flt']:<14.1e} | "
            f"{riga['lunghezza_flt']:<14.1e} | "
            f"{riga['area_flt']:<16.1e} | "
            f"{riga['divisione_flt']:<16.4f} | "
            f"{riga['errore_computazionale']:<18.4e}"
        )
    print(separatore)


def esporta_file_csv(dati, nome_file="analisi_deriva_mc84.csv"):
    """Esporta i dati in un file CSV standard leggibile nativamente da Excel."""
    try:
        with open(nome_file, "w", encoding="utf-8") as file:
            file.write(
                "Iterazione;Larghezza;Lunghezza;Area;Divisione;Errore_Relativo_Mantissa\n"
            )
            for riga in dati:
                l_str = f"{riga['larghezza_flt']:.6e}".replace(".", ",")
                lu_str = f"{riga['lunghezza_flt']:.6e}".replace(".", ",")
                a_str = f"{riga['area_flt']:.6e}".replace(".", ",")
                d_str = f"{riga['divisione_flt']:.6f}".replace(".", ",")
                e_str = f"{riga['errore_computazionale']:.6e}".replace(".", ",")

                file.write(
                    f"{riga['iterazione']};{l_str};{lu_str};{a_str};{d_str};{e_str}\n"
                )
        print(f"[INFO] Report CSV salvato correttamente su disco: '{nome_file}'")
    except OSError as e:
        print(f"[Errore] Impossibile scrivere il file di report: {e}")


def genera_grafici(dati, nome_grafico="grafico_olografia_mc84.png"):
    """Genera e salva il pannello di monitoraggio della deriva dei registri."""
    passi = [riga["iterazione"] for riga in dati]
    aree = [riga["area_flt"] for riga in dati]
    divisioni = [riga["divisione_flt"] for riga in dati]
    errori = [riga["errore_computazionale"] for riga in dati]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(
        "ANALISI SCIENTIFICA DELLA SINGOLARITÀ GEOMETRICA E CORRUZIONE DELLA MANTISSA\n"
        "Validazione Numerica del Principio di Risonanza Olografica - Modello Mc84 (Anno 2026)",
        fontsize=12,
        fontweight="bold",
        color="darkblue",
        y=0.96,
    )

    # --- GRAFICO 1: EVOLUZIONE ESPONENZIALE DELLO SPAZIO ---
    ax1.plot(
        passi,
        aree,
        marker="o",
        color="crimson",
        linewidth=2,
        label="Espansione Spazio Solido",
    )
    ax1.set_title(
        "1. Crescita Esponenziale dell'Area di Confine", fontsize=10, fontweight="bold"
    )
    ax1.set_xlabel("Numero di Iterazioni Complesse (n)", fontsize=9)
    ax1.set_ylabel("Dimensione Bidimensionale (Scala Logaritmica)", fontsize=9)
    ax1.set_yscale("log")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left")

    # --- GRAFICO 2: PROGRESSIONE DEL RAPPORTO E VERIFICA DERIVA ---
    ax2.plot(
        passi,
        divisioni,
        marker="s",
        color="royalblue",
        linewidth=2,
        label="Rapporto Area/Perimetro (Float)",
    )
    ax2.set_title(
        "2. Stabilità Lineare del Rapporto Geometrico", fontsize=10, fontweight="bold"
    )
    ax2.set_xlabel("Numero di Iterazioni Complesse (n)", fontsize=9)
    ax2.set_ylabel("Valore Lineare Risultante", fontsize=9)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Iniezione del monitoraggio della deriva reale dell'hardware tramite asse secondario
    ax3 = ax2.twinx()
    ax3.plot(
        passi,
        errori,
        color="darkorange",
        linestyle="-.",
        linewidth=2,
        label="Errore di Troncamento Reale (IEEE 754)",
    )
    ax3.set_ylabel(
        "Scostamento Relativo Assoluto dalla Precisione Infinita",
        color="darkorange",
        fontsize=9,
    )
    ax3.tick_params(axis="y", labelcolor="darkorange")

    # Unificazione delle legende dei due assi sovrapposti
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax3.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.savefig(nome_grafico, dpi=300, bbox_inches="tight")
    print(f"[INFO] Pannello grafico esportato ad alta risoluzione: '{nome_grafico}'")
    plt.show()


def main():
    """Funzione pilota dell'intero flusso del programma."""
    pulisci_schermo()
    print("=" * 75)
    print("   LABORATORIO COMPUTAZIONALE DI OLOGRAFIA GEOMETRICA E DERIVA IEEE 754   ")
    print("   Modello di Analisi d'Invenzione Scientifica Convalidata: Mc84        ")
    print("=" * 75)

    larg_iniziale = richiedi_input_numerico("Inserisci la larghezza iniziale (es. 2): ")
    lung_iniziale = richiedi_input_numerico("Inserisci la lunghezza iniziale (es. 3): ")
    moltiplicatore = richiedi_input_numerico(
        "Inserisci il moltiplicatore geometrico (es. 5): "
    )

    iterazioni = int(
        richiedi_input_numerico(
            "Inserisci il numero di passi della serie (Consigliato 20-40): ",
            consente_avviso_passi=True,
        )
    )

    risultati = esegui_simulazione_fourier_analog(
        larg_iniziale, lung_iniziale, moltiplicatore, iterazioni
    )

    stampa_tabella_terminale(risultati)
    esporta_file_csv(risultati)
    genera_grafici(risultati)


if __name__ == "__main__":
    main()
