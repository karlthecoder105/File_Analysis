import os
from datetime import datetime
import analuusaator

def kuva_leitud_failitüübid():
    failid = os.listdir()
    laiendid = set()
    for f in failid:
        if os.path.isfile(f):
            ext = os.path.splitext(f)[1]
            if ext:  # ignoreeri failid ilma laiendita
                laiendid.add(ext)
    print("Leitud failitüübid selles kataloogis:")
    print(", ".join(sorted(laiendid)) if laiendid else "Faililaiendeid ei leitud.")

def summeeri_statistika(failinimekiri):
    koguarv = {"read": 0, "tyhjad": 0, "TODO": 0, "FIXME": 0}
    detailid = []
    for fail in failinimekiri:
        tulemus = analuusaator.analuusi_faili_sisu(fail)
        if "viga" in tulemus:
            print(f"Viga faili {fail} lugemisel: {tulemus['viga']}")
            continue
        for k in koguarv.keys():
            koguarv[k] += tulemus[k]
        detailid.append(tulemus)
    return koguarv, detailid

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

def kustuta_logid():
    kataloog = "Analüüsi_Raportid"
    if not os.path.exists(kataloog):
        print("Logikataloogi pole.")
        return
    logid = [os.path.join(kataloog, f) for f in os.listdir(kataloog) if f.endswith(".txt")]
    if not logid:
        print("Pole ühtegi logifaili kustutamiseks.")
        return
    print("\nLeiti logifaile:")
    for i, f in enumerate(logid):
        print(f"{i+1}. {f}")
    kas = input("Kas kustutada KÕIK logid? (jah/ei): ").strip().lower()
    if kas == "jah":
        for f in logid:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Ei saanud kustutada {f}: {e}")
        print("Logid on kustutatud.")
    else:
        print("Logisid ei kustutatud.")

def otsi_algustahega():
    taht = input("Sisesta failinime algustäht: ").strip()
    if not taht or len(taht) != 1:
        print("Palun sisesta üks täht.")
        return
    failid = analuusaator.leia_failid_algustahega(taht)
    print(f"Failid, mis algavad tähega '{taht}':")
    print("\n".join(failid) if failid else "Sobivaid faile ei leitud.")

def main():
    print("Tere tulemast projekti analüüsaatorisse!")
    kuva_leitud_failitüübid()
    viimati = (None, None)  # (statistika, detailid)
    while True:
        print("\nValikud:")
        print("1 - Täisanalüüs vali laiendiga faile")
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
            statistika, detailid = summeeri_statistika(failid)
            print("Analüüsi tulemus:")
            print(statistika)
            viimati = (statistika, detailid)
        elif valik == "2":
            if viimati[0] is None:
                print("Pole ühtegi tehtud analüüsi, mida salvestada!")
            else:
                salvesta_raport(viimati[0], viimati[1])
        elif valik == "3":
            kustuta_logid()
        elif valik == "4":
            otsi_algustahega()
        elif valik == "0":
            print("Head aega!")
            break
        else:
            print("Tundmatu valik!")

if __name__ == '__main__':
    main()