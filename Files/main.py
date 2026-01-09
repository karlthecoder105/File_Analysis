import glob
import os

laiend = input("Sisesta faililaiend (näiteks .py): ").strip()
failid = glob.glob(f"*{laiend}")

if not failid:
    print("Ühtegi faili laiendiga", laiend, "ei leitud.")
else:
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
        print(f"\nFail: {failitee}")
        print(f"  Ridade arv: {ridade_arv}")
        print(f"  Tühjade ridade arv: {tyhjade_arv}")
        print(f"  TODO: {todo_arv}")
        print(f"  FIXME: {fixme_arv}")
