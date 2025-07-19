# -*- coding: utf-8 -*-
"""Funcion para calcular el tamanio del efecto de Cohen d por grupo.

Requisitos:
- pandas, numpy, scipy

Ejemplo de uso al final del archivo.
"""
import pandas as pd
import numpy as np
from scipy import stats

def cohend_group(
    df: pd.DataFrame,
    varlist: list[str],
    group: str,
    method: str = "dz"
) -> pd.DataFrame:
    """Calcula Cohen d para variables binarias pre y post por grupo.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con datos.
    varlist : list[str]
        Lista de nombres de columnas PRE+POST en orden.
    group : str
        Nombre de la columna de grupo.
    method : str, optional
        Metodo para el denominador ("dz", "dav" o "drm"), por defecto "dz".

    Returns
    -------
    pd.DataFrame
        DataFrame con resultados por grupo.
    """

    # 1. Validaciones iniciales
    if group not in df.columns:
        raise ValueError(f"La columna de grupo '{group}' no existe en el DataFrame")
    if len(varlist) % 2 != 0:
        raise ValueError("'varlist' debe contener un numero par de variables")
    for col in varlist:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe en el DataFrame")

    # 2. Dividir en pre y post
    mid = len(varlist) // 2
    prevars = varlist[:mid]
    postvars = varlist[mid:]

    df_copy = df.copy()
    # 3. Convertir a numerico si es necesario
    df_copy[prevars + postvars] = df_copy[prevars + postvars].apply(
        pd.to_numeric, errors="coerce"
    )

    # 4. Calculos de proporciones y diferencia por registro
    df_copy["tpre"] = (df_copy[prevars] == 2).mean(axis=1)
    df_copy["tpost"] = (df_copy[postvars] == 2).mean(axis=1)
    df_copy["dif"] = df_copy["tpost"] - df_copy["tpre"]

    resultados = []

    # 5. Iterar por cada nivel de grupo
    for nivel in df_copy[group].astype(str).unique():
        sub = df_copy[df_copy[group].astype(str) == str(nivel)]
        sub = sub.dropna(subset=["tpre", "tpost"])
        N = len(sub)
        if N == 0:
            continue
        m_pre = sub["tpre"].mean()
        m_post = sub["tpost"].mean()
        m_diff = sub["dif"].mean()
        sd_pre = sub["tpre"].std(ddof=1)
        sd_post = sub["tpost"].std(ddof=1)
        sd_diff = sub["dif"].std(ddof=1)
        r_pp = sub["tpre"].corr(sub["tpost"])  # puede ser NaN con N<2

        if method == "dz":
            denom = sd_diff
        elif method == "dav":
            denom = (sd_pre + sd_post) / 2
        elif method == "drm":
            denom = np.sqrt(sd_pre ** 2 + sd_post ** 2 - 2 * r_pp * sd_pre * sd_post)
        else:
            raise ValueError("method debe ser 'dz', 'dav' o 'drm'")

        d_cohen = m_diff / denom if denom and denom != 0 else np.nan

        if N >= 2:
            t_res = stats.ttest_rel(sub["tpost"], sub["tpre"], nan_policy="omit")
            p_value = t_res.pvalue
        else:
            p_value = np.nan

        # Clasificacion de magnitud
        if pd.isna(d_cohen):
            magnitude = "NA"
            symbol = ""
        elif abs(d_cohen) >= 0.80:
            magnitude = "GRANDE"
            symbol = "★★★"
        elif abs(d_cohen) >= 0.50:
            magnitude = "MEDIANO"
            symbol = "★★"
        elif abs(d_cohen) >= 0.20:
            magnitude = "PEQUEÑO"
            symbol = "★"
        else:
            magnitude = "TRIVIAL"
            symbol = ""

        resultados.append({
            "grupo": nivel,
            "N": N,
            "m_pre": m_pre,
            "m_post": m_post,
            "m_diff": m_diff,
            "d_cohen": d_cohen,
            "p_value": p_value,
            "magnitude": magnitude,
            "symbol": symbol,
        })

    result_df = pd.DataFrame(resultados)

    # 7. Exportar a Excel. Se intenta usar xlsxwriter y, si no está
    # disponible, se recurre a openpyxl.
    filename = "cohend_resultados.xlsx"
    titulo = (
        f"Cohen d – Variables: {', '.join(prevars)}, {', '.join(postvars)} (método={method})"
    )

    try:
        import xlsxwriter  # noqa: F401
        engine = "xlsxwriter"
    except ImportError:
        try:
            import openpyxl  # noqa: F401
            engine = "openpyxl"
        except ImportError as e:
            raise ImportError(
                "Necesita instalar 'xlsxwriter' u 'openpyxl' para exportar a Excel"
            ) from e

    with pd.ExcelWriter(filename, engine=engine) as writer:
        result_df.to_excel(writer, sheet_name="resultados", startrow=2, index=False)
        worksheet = writer.sheets["resultados"]
        worksheet.write("A1", titulo)

    print(f"Archivo guardado: {filename}")

    return result_df

# Ejemplo minimo de uso
# varlist de variables pre y post
varlist_ejemplo = ["ce_p1", "ce_p2", "cs_i1_p1", "cs_i1_p2"]
# Llamada a la funcion
# resultados = cohend_group(df, varlist=varlist_ejemplo, group="macro", method="dav")
# print(resultados)
