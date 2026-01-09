import glob
import os

def leia_projektifailid(laiend):
    """Leiab kõik failid, mille laiend on 'laiend' – nt '.py'."""
    return glob.glob(f"*{laiend}")

def analuusi_faili_sisu(failitee):
    """Tagastab sõnastiku: ridade arv, tühjade ridade arv, 'TODO' ja 'FIXME' arv failis."""
    ridade_arv = 0
    tyhjade_arv = 0
    todo_arv = 0
    fixme_arv = 0
    try:
        with open(failitee, encoding="utf-8") as f:
            for rida in f:
                ridade_arv += 1
                if rida.strip() == '':
                    tyhjade_arv += 1
                todo_arv += rida.count("TODO")
                fixme_arv += rida.count("FIXME")
    except Exception as e:
        return {"viga": str(e)}
    return {
        "fail": failitee,
        "read": ridade_arv,
        "tyhjad": tyhjade_arv,
        "TODO": todo_arv,
        "FIXME": fixme_arv
    }

def loo_raporti_kataloog(nimi="Analüüsi_Raportid"):
    """Loob raportikataloogi, kui seda pole."""
    if not os.path.exists(nimi):
        os.mkdir(nimi)

def leia_failid_algustahega(taht):
    """Leiab kõik failid, mille nimi algab etteantud tähega."""
    return glob.glob(f"{taht}*.*")