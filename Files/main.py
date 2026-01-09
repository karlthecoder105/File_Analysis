import os
from datetime import datetime
import analuusaator

def kuva_failitüübid():
    tipus = set()
    for fname in os.listdir():
        if os.path.isfile(fname):
            ext = os.path.splitext(fname)[1]
            if ext:
                tipus.add(ext)
    print("Leitud failitüübid:", ", ".join(sorted(tipus) if tipus else ["-"]))

def summeeri_sta(failid):
    agg = {"read":0, "tyhjad":0, "TODO":0, "FIXME":0}
    detail = []
    for fail in failid:
        tulemus = analuusaator.analuusi_faili_sisu(fail)
        if "viga" in tulemus:
            print(f"Viga faili {fail} lugemisel: {tulemus['viga']}")
            continue
        for k in agg:
            agg[k] += tulemus[k]
        detail.append(tulemus)
    return agg, detail

def salvesta_raport(statistika, detailid):
    analuusaator.loo_raporti_kataloog()
    kuupaev = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    failinimi = f"Analüüsi_Raportid/raport_{kuupaev}.txt"
    with open(failinimi, "w", encoding="utf-8") as f:
        f.write("Üldstatistika:\n")
        for k, v in statistika.items():
            f.write(f"{k}: {v}\n")
        f.write("\nDetailid:\n")
        for d in detailid:
            f.write(str(d)+"\n")
    print(f"Raport salvestatud: {failinimi}")

def puhasta_logid():
    kataloog = "Analüüsi_Raportid"
    if not os.path.exists(kataloog):
        print("Logikataloogi pole.")
        return
    logid = [os.path.join(kataloog, f) for f in os.listdir(kataloog) if f.endswith(".txt")]
    if not logid:
        print("Pole logifaile.")
        return
    print(f"Leiti {len(logid)} logi/raportit.")
    kas = input("Kas kustutada kõik? (jah/ei): ").strip().lower()
    if kas == "jah":
        for f in logid:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Ei saanud kustutada {f}: {e}")
        print("Kustutatud.")
    else:
        print("Kustutamine tühistatud.")

def main():
    print("Tere tulemast projekti analüüsaatorisse!\n")
    print("Asukoht:", os.getcwd())
    kuva_failitüübid()
    viimati = (None, None)
    while True:
        print("\nValikud:")
        print("1 - Täisanalüüs (vali laiendi järgi)")
        print("2 - Salvesta viimane analüüs raportina")
        print("3 - Puhasta logid (kustuta raportid)")
        print("4 - Otsi faili algustähe järgi")
        print("0 - Välju")
        valik = input("Sisesta valiku number: ").strip()
        if valik == "1":
            laiend = input("Sisesta faililaiend (näiteks .py): ").strip()
            failid = analuusaator.leia_projektifailid(laiend)
            if not failid:
                print("Sobivaid faile ei leitud.")
                continue
            statistika, detailid = summeeri_sta(failid)
            print("\nAnalüüsi tulemus:")
            print(statistika)
            viimati = (statistika, detailid)
        elif valik == "2":
            if viimati[0] is None:
                print("Pole tehtud analüüsi.")
            else:
                salvesta_raport(viimati[0], viimati[1])
        elif valik == "3":
            puhasta_logid()
        elif valik == "4":
            taht = input("Sisesta algustäht: ").strip()
            if not taht or len(taht) != 1:
                print("Sisesta just 1 täht.")
                continue
            failid = analuusaator.leia_failid_algustahega(taht)
            print(f"Failid algusega '{taht}':")
            print('\n'.join(failid) if failid else "Ei leitud.")
        elif valik == "0":
            print("Head aega!")
            break
        else:
            print("Vale valik.")

if __name__ == "__main__":
    main()
