# os.getcwd() – tagastab jooksva töötava kataloogi
# os.listdir() – loetleb kõik failid ja kaustad kataloogis
# os.path.isfile(path) – kontrollib, kas antud tee viitab failile
# os.path.splitext(filename) – jagab failinime nimeks ja laiendiks
# os.path.exists(path) – kontrollib, kas kaust või fail eksisteerib
# os.mkdir(path) – loob uue kataloogi
# os.remove(path) – kustutab faili
# glob.glob(pattern) – loetleb kõik failid, mis vastavad mustrile (nt "*.py")
# datetime.now().strftime(format) – tagastab jooksva kuupäeva/aja vormindatud tekstina
# input() – küsib kasutajalt sisendit
# print() – kuvab teksti ekraanile
# open(filename, ...) – avab faili lugemiseks/kirjutamiseks
# continue, break – tsükli juhtimine ("jätka" või "katkesta" tsükkel)


import glob
import os

def leia_projektifailid(laiend):
    """
    Tagastab kõik failid, mille laiend vastab etteantule (nt .py, .txt, .java).
    """
    return glob.glob(f"*{laiend}")

def analuusi_faili_sisu(failitee):
    """
    Loeb faili ridade kaupa ja arvutab:
      - ridade koguarv,
      - tühjade ridade arv,
      - TODO esinemiste arv,
      - FIXME esinemiste arv.
    Tagastab tulemused sõnastikuna.
    """
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
        return {"fail": failitee, "viga": str(e)}
    return {
        "fail": failitee,
        "read": ridade_arv,
        "tyhjad": tyhjade_arv,
        "TODO": todo_arv,
        "FIXME": fixme_arv
    }

def loo_raporti_kataloog(nimi="Analüüsi_Raportid"):
    """
    Loob raportite kataloogi, kui seda pole olemas.
    """
    if not os.path.exists(nimi):
        os.mkdir(nimi)

def leia_failid_algustahega(taht):
    """
    Tagastab kõik failid, mille nimi algab etteantud tähega.
    """
    return glob.glob(f"{taht}*.*")
