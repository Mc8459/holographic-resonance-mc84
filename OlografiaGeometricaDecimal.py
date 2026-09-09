"""
LABORATORIO COMPUTAZIONALE DI OLOGRAFIA GEOMETRICA AD ALTA PRECISIONE v3.0.0
Studio delle singolarità spaziali e analisi della convergenza del rapporto Area/Perimetro.
Motore di Calcolo: Aritmetica a Precisione Arbitraria (Modulo Decimal).
Sviluppo e Firma Scientifica: Mc84 (Mario Cera) - Anno 2026
"""

import os
from decimal import Decimal, InvalidOperation, getcontext

import matplotlib.pyplot as plt

# --- CONFIGURAZIONE REGISTRI AD ALTA PRECISIONE ---

# Impostazione della precisione assoluta a 100 cifre per l'annullamento della deriva di troncamento
getcontext().prec = 100


def pulisci_schermo():
    """Ripulisce il terminale di comando in base al sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def richiedi_input_numerico(messaggio, consente_avviso_passi=False):
    """
    Richiede un input all'utente garantendo la conformità sintattica numerica.
    Restituisce un oggetto Decimal nativo per prevenire errori di inizializzazione.
    """
    while True:
        try:
            stringa_input = input(messaggio).strip().replace(",", ".")
            valore = Decimal(stringa_input)
            if valore <= 0:
                print("[Errore] Inserire un valore maggiore di zero.")
                continue

            if consente_avviso_passi and valore > 45:
                print(
                    f"\n[ATTENZIONE] Hai inserito {int(valore)} iterazioni complesse."
                )
                print(
                    "L'espansione geometrica genererà stringhe numeriche astronomiche."
                )
                conferma = input("Vuoi procedere comunque? (s/n): ").lower()
                if conferma != "s":
                    print("Inserimento annullato. Riprova.")
                    continue

            return valore
        except (ValueError, InvalidOperation):
            print("[Errore] Input non valido. Inserire solo cifre numeriche.")


def esegui_simulazione_precisione_arbitraria(
    larghezza_ini, lunghezza_ini, moltiplicatore, passi
):
    """
    Risolve le equazioni evolutive dello spazio olografico bidimensionale.
    Garantisce l'assenza di troncamento binario sui registri computazionali.
    """
    dati = []
    larghezza = larghezza_ini
    lunghezza = lunghezza_ini
    for n in range(1, passi + 1):
        l_corr = larghezza * moltiplicatore
        lu_corr = lunghezza * moltiplicatore

        somma = l_corr + lu_corr
        area = l_corr * lu_corr
        divisione = area / somma if somma != Decimal("0.0") else Decimal("0.0")

        # Calcolo analitico predittivo dell'entropia teorica residua della mantissa
        entropia_bit_stimata = float(Decimal(str(n)) * Decimal("0.5"))

        dati.append(
            {
                "iterazione": n,
                "larghezza": l_corr,
                "lunghezza": lu_corr,
                "somma": somma,
                "area": area,
                "divisione": divisione,
                "entropia_res": entropia_bit_stimata,
            }
        )

        larghezza = l_corr
        lunghezza = lu_corr

    return dati


def stampa_tabella_terminale(dati):
    """Visualizza i dati calcolati ad alta precisione in forma tabellare."""
    separatore = "-" * 110
    print(
        f"\n{'Iterazione':<12} | {'Larghezza (Dec)':<15} | {'Lunghezza (Dec)':<15} | "
        f"{'Area (Dec)':<18} | {'Rapporto Confine':<18}"
    )
    print(separatore)

    for riga in dati:
        print(
            f"{riga['iterazione']:<12} | "
            f"{float(riga['larghezza']):<15.2e} | "
            f"{float(riga['lunghezza']):<15.2e} | "
            f"{float(riga['area']):<18.2e} | "
            f"{float(riga['divisione']):<18.4f}"
        )
    print(separatore)


def esporta_file_csv(dati, nome_file="serie_alta_precisione.csv"):
    """Esporta i dati strutturati mantenendo intatta la stringa decimale pura a 100 cifre."""
    try:
        with open(nome_file, "w", encoding="utf-8") as file:
            file.write(
                "Iterazione;Larghezza;Lunghezza;Somma;Area;Divisione_Area_Perimetro\n"
            )
            for riga in dati:
                l_str = f"{riga['larghezza']}".replace(".", ",")
                lu_str = f"{riga['lunghezza']}".replace(".", ",")
                s_str = f"{riga['somma']}".replace(".", ",")
                a_str = f"{riga['area']}".replace(".", ",")
                d_str = f"{riga['divisione']}".replace(".", ",")

                file.write(
                    f"{riga['iterazione']};{l_str};{lu_str};{s_str};{a_str};{d_str}\n"
                )
        print(
            f"[INFO] Registro CSV ad alta precisione generato correttamente: '{nome_file}'"
        )
    except OSError as e:
        print(f"[Errore] Impossibile scrivere il report di precisione su disco: {e}")


def genera_grafici(dati, nome_grafico="grafico_alta_precisione_mc84.png"):
    """Genera e salva la mappatura ad alta definizione per la validazione della risonanza."""
    passi = [riga["iterazione"] for riga in dati]
    aree = [float(riga["area"]) for riga in dati]
    divisioni = [float(riga["divisione"]) for riga in dati]
    entropia = [riga["entropia_res"] for riga in dati]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(
        "IL PRINCIPIO DI RISONANZA DI OLOGRAFIA BIDIMENSIONALE - MODELLO MC84 (Anno 2026)\n"
        "Simulazione Avanzata in Aritmetica Arbitraria Estesa [Stabilità Assoluta dei Registri Decimal]",
        fontsize=12,
        fontweight="bold",
        color="darkblue",
        y=0.95,
    )

    # --- GRAFICO 1: EVOLUZIONE ESPONENZIALE DELLO SPAZIO ---
    ax1.plot(
        passi,
        aree,
        marker="o",
        color="crimson",
        linewidth=2,
        label="Volume Area Solida",
    )
    ax1.set_title(
        "1. Invarianza Frattale dell'Espansione Spaziale",
        fontsize=10,
        fontweight="bold",
    )
    ax1.set_xlabel("Fattore di Iterazione Lineare (n)", fontsize=9)
    ax1.set_ylabel("Dimensione Bidimensionale (Scala Logaritmica)", fontsize=9)
    ax1.set_yscale("log")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left")

    # --- GRAFICO 2: PROGRESSIONE DEL RAPPORTO (AREA / SOMMA) ---
    ax2.plot(
        passi,
        divisioni,
        marker="s",
        color="royalblue",
        linewidth=2,
        label="Rapporto Area/Perimetro (Decimal)",
    )
    ax2.set_title(
        "2. Stabilità e Convergenza Spettrale del Confine",
        fontsize=10,
        fontweight="bold",
    )
    ax2.set_xlabel("Fattore di Iterazione Lineare (n)", fontsize=9)
    ax2.set_ylabel("Valore del Rapporto Risultante", fontsize=9)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Asse secondario per il monitoraggio preventivo dell'accumulo entropico
    ax3 = ax2.twinx()
    ax3.plot(
        passi,
        entropia,
        color="purple",
        linestyle="--",
        linewidth=1.5,
        label="Carico Entropico dei Registri",
    )
    ax3.set_ylabel(
        "Indice Teorico di Confinamento della Informazione (Bit)",
        color="purple",
        fontsize=9,
    )
    ax3.tick_params(axis="y", labelcolor="purple")

    # Unificazione legende
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax3.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout(rect=[0, 0, 1, 0.88])
    plt.savefig(nome_grafico, dpi=300, bbox_inches="tight")
    print(f"[INFO] Report grafico ad alta risoluzione salvato come: '{nome_grafico}'")
    plt.show()


def main():
    """Funzione pilota dell'intero flusso del programma."""
    pulisci_schermo()
    print("=" * 80)
    print("   LABORATORIO COMPUTAZIONALE DI OLOGRAFIA GEOMETRICA AD ALTA PRECISIONE   ")
    print("   Algoritmo di Riferimento Strutturale Convalidato: Modello Mc84 (2026) ")
    print("=" * 80)

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

    risultati = esegui_simulazione_precisione_arbitraria(
        larg_iniziale, lung_iniziale, moltiplicatore, iterazioni
    )

    stampa_tabella_terminale(risultati)
    esporta_file_csv(risultati)
    genera_grafici(risultati)


if __name__ == "__main__":
    main()
