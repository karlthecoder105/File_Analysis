import os
from datetime import datetime
import glob




print("Tere tulemast projekti analüüsaatorisse!\n")
print("Asukoht:", os.getcwd()) #os.getcwd() – tagastab jooksva töötava kataloogi

failid = [f for f in os.listdir() if os.path.isfile(f)] #os.path.isfile(path) – kontrollib, kas antud tee viitab failile, os.listdir() – loetleb kõik failid ja kaustad kataloogis
laiendid = set()
for f in failid:
    ext = os.path.splitext(f)[1] #os.path.splitext(filename) – jagab failinime nimeks ja laiendiks
    if ext:
        laiendid.add(ext)
print("Leitud failitüübid:", ", ".join(sorted(laiendid)) if laiendid else "Ei leitud laiendiga faile.")

viimane_statistika = None
viimased_detailid = None

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
        failid = glob.glob(f"*{laiend}")
        if not failid:
            print("Sobivaid faile ei leitud.")
            continue
        statistika = {"read":0, "tyhjad":0, "TODO":0, "FIXME":0}
        detailid = []
        for failitee in failid:
            ridade_arv = 0
            tyhjade_arv = 0
            todo_arv = 0
            fixme_arv = 0
            try:
                with open(failitee, encoding="utf-8") as f:
                    for rida in f:
                        ridade_arv += 1
                        if rida.strip() == "":
                            tyhjade_arv += 1
                        todo_arv += rida.count("TODO")
                        fixme_arv += rida.count("FIXME")
            except Exception as e:
                print(f"Viga faili {failitee} lugemisel: {e}")
                continue
            statistika["read"] += ridade_arv
            statistika["tyhjad"] += tyhjade_arv
            statistika["TODO"] += todo_arv
            statistika["FIXME"] += fixme_arv
            detailid.append({
                "fail": failitee,
                "read": ridade_arv,
                "tyhjad": tyhjade_arv,
                "TODO": todo_arv,
                "FIXME": fixme_arv
            })
        print("\nAnalüüsi tulemus:")
        print(statistika)
        viimane_statistika = statistika
        viimased_detailid = detailid

    elif valik == "2":
        if viimane_statistika is None:
            print("Pole tehtud ühtegi analüüsi!")
        else:
            kataloog = "Analüüsi_Raportid"
            if not os.path.exists(kataloog): #os.path.exists(path) – kontrollib, kas kaust või fail eksisteerib
                os.mkdir(kataloog) #os.mkdir(path) – loob uue kataloogi
            kuupaev = datetime.now().strftime("%Y_%m_%d_%H%M%S")
            failinimi = f"{kataloog}/raport_{kuupaev}.txt"
            with open(failinimi, "w", encoding="utf-8") as f:
                f.write("Üldstatistika:\n")
                for k, v in viimane_statistika.items():
                    f.write(f"{k}: {v}\n")
                f.write("\nDetailid:\n")
                for d in viimased_detailid:
                    f.write(str(d) + "\n")
            print(f"Raport salvestatud: {failinimi}")

    elif valik == "3":
        kataloog = "Analüüsi_Raportid"
        if not os.path.exists(kataloog):
            print("Logikataloogi pole.")
            continue
        logid = [os.path.join(kataloog, f) for f in os.listdir(kataloog) if f.endswith(".txt")]
        if not logid:
            print("Pole logifaile.")
            continue
        print(f"Leiti {len(logid)} logi/raportit.")
        kas = input("Kas kustutada kõik? (jah/ei): ").strip().lower()
        if kas == "jah":
            for f in logid:
                try:
                    os.remove(f) #os.remove(path) – kustutab faili
                except Exception as e:
                    print(f"Ei saanud kustutada {f}: {e}")
            print("Kustutatud.")
        else:
            print("Kustutamine tühistatud.")

    elif valik == "4":
        taht = input("Sisesta algustäht: ").strip()
        if not taht or len(taht) != 1:
            print("Sisesta just 1 täht.")
            continue
        failid = glob.glob(f"{taht}*.*")
        print(f"Failid algusega '{taht}':")
        if failid:
            print('\n'.join(failid))
        else:
            print("Ei leitud.")

    elif valik == "0":
        print("Head aega!")
        break
    else:
        print("Vale valik.")
