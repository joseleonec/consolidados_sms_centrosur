from termcolor import colored
from pandas.io.parsers.readers import read_csv
import pandas as pd
import os
import glob
import re
from unicodedata import normalize
from werkzeug.utils import secure_filename

home_salida = "./uploads/"

"""### Lectura de archivos

#### Subir los archivos

Cargar todos los archivos de la carpeta
"""

# from google.colab import files


def quitar_tildes(dataframe_column):
    # import unicodedata
    # dataframe_column = dataframe_column.apply(lambda x: unicodedata.normalize("NFKD", x.encode("ascii","ignore").decode("ascii")))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'á', "a", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'Á', "A", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'é', "e", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'É', "E", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'í', "i", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'Í', "I", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'ó', "o", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'Ó', "O", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'ú', "u", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'Ú', "U", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'ñ', "n", x))
    dataframe_column = dataframe_column.apply(lambda x: re.sub(r'Ñ', "N", x))
    return dataframe_column


def reducir_caracteres_mensaje(df):
    maximo = df["Mensaje"].apply(lambda x: len(x)).max()

    df["Mensaje corto"] = df["Mensaje"].apply(lambda x: x.replace(
        "Duracion aproximada", "Duracion aprox") if len(x) > 150 else x)

    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: x.replace("_", " "))
    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: get_duration_from_time(x))  # duracion 04:00 horas --> duracion 4 horas

    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: x.replace(" horas", "h") if len(x) > 150 else x)
    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: x.replace(": Debido", ":Debido") if len(x) > 150 else x)

    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : re.sub(r'(\d)(\d)(\:\d\d)(h|horas)', r"\2\4", x) ) # duracion 04:00 horas --> duracion 4 horas
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : re.sub(r'(\d)(\d)(\:\d\d)(h)', "\\2\\4", x) if len(x) > 150  else x)

    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("sector", "",1) if len(x) > 150 and x.lower().count('sector') > 1 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : re.sub(r"(?:sector|Sector|SECTOR|sectro)","",x,) if len(x) > 150  else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : re.sub(r"(?:sector|Sector|SECTOR|sectro)","en",x) if len(x) > 150  else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : re.sub(r"(?:en el sector|en el Sector|en el SECTOR|en el sectro)","en",x) )
    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"(?:sector SECTOR|sector Sector|SECTOR SECTOR|sectro sectr)", "sector", x))

    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"\(.*?\)", "", x) if len(x) > 150 else x)  # eliminar "(texto em parentesis)"
    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"(?: y | Y )", "/", x) if len(x) > 150 else x)  # cambiar " y " por "/"

    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"(?:suspendera|suspender)", "suspende", x) if len(x) > 150 else x)
    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"(?:Calles|calles|CALLEs|Cales|Calle|calle|CALLE|Cale)", "", x) if len(x) > 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("suspender", "suspende") if len(x) > 150 else x)
    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: x.replace("PARROQUIA", "/") if len(x) > 150 else x)
    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        "(?:Cuenca|CUENCA|cuenca|CUENCA|Morona Santiago|morona santiago|MORONA SANTIAGO|Cañar|CAÑAR|cañar|Canar|CANAR|canar)", "", x) if len(x) > 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("en el", "en") if len(x) > 150 else x)

    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: x.replace(" Duracion", "Duracion") if len(x) > 150 else x)

    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"[\.|\,|;]", "", x) if len(x) > 150 else x)  # eliminar puntos, COMAS y puntos y comas
    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"(\d)(?=(\d)(?:(h+)))", r"\1.", x) if len(x) > 150 else x)  # 05 horas --> 0.5 horas
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : re.sub(r"0(?=(\d)(?:(h+)))","0.",x) if len(x) > 150  else x)# 05 horas --> 0.5 horas

    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: x.replace("Duracion aprox", "por") if len(x) > 150 else x)
    df["Mensaje corto"] = df["Mensaje corto"].apply(
        lambda x: x.replace("en el sector", "en") if len(x) > 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("por", " por") if len(x) < 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("Debido a", "Por") if len(x) > 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("Comunica", "informa") if len(x) > 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("CENTROSUR informa", "CENTROSUR") if len(x) > 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("mejoras en el ", "mejoras ") if len(x) > 150 else x)
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : x.replace("durante", "por") if len(x) > 150 else x)

    df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x: re.sub(
        r"[^\S\r\n]{2,}", " ", x))  # corrige dos o mas espacios juntos
    # df["Mensaje corto"] = df["Mensaje corto"].apply(lambda x : re.sub(r"[^\S\r\n]{2,}", " ", x) if len(x) > 150  else x) # corrige dos o mas espacios juntos

    minimo = df["Mensaje corto"].apply(lambda x: len(x)).max()
    print("Se ha reducido el mensaje en ", maximo - minimo, "caracteres")
    return df


def get_duration_from_time(mensaje):
    try:
        from datetime import timedelta
        # de este mensaje --> "CENTROSUR Comunica: Debido a mejoras en el sector SEVILLA DE ORO el 04/06/2022 el servicio se suspende a las 09:00, Duracion aproximada 02:30 horas"
        # se pasa a este  --> "CENTROSUR Comunica: Debido a mejoras en el sector SEVILLA DE ORO el 04/06/2022 el servicio se suspende a las 09:00, Duracion aproximada 2.5 horas"
        msg = re.sub(r'(\d)(\d)(\:\d\d)(?:\s)?(horas|h)',
                     r"(\1\2\3)\4", mensaje)
        text = re.search(
            r"(\()(\d)(\d)(\:\d\d)(?:\s)?(\))(horas|h)", msg).group()
        # print(text)
        text2 = re.search(r"\(([^)]+)\)", text).group()
        # print(text2)
        str_time = text2.replace("(", "").replace(")", "")
        # print(str_time)
        horas_y_minutos = str_time.split(":")
        horas = int(horas_y_minutos[0])
        minutos = int(horas_y_minutos[-1])
        delta = timedelta(minutes=minutos, hours=horas)
        duracion_en_horas = delta.seconds/3600
        duracion_en_horas = int(duracion_en_horas) if duracion_en_horas == round(
            duracion_en_horas) else round(duracion_en_horas, 1)
        return msg.replace(text2, str(duracion_en_horas)+" ")
    except:
        return msg

# print("================ ARCHIVOS LEIDOS ================" if len(uploaded) > 0 else "")


def read_files(uploads_dir, files):
    columnas_utiles_base_fuente1 = [
        "NOMBRES", "TELEFONO", "MENSAJE", "WR", "CUEN"]
    c_bf1 = ["SMSNOMBRE", "SMSCLITEL", "SMSMSG", "WR"]
    columnas_utiles_base_fuente2 = [
        'Nombre', "Celular", 'SMSMSG', "WR", "Cuenta"]
    c_bf2 = ['Nombre', "Celular", 'SMSMSG', "Unnamed: 18", "Cuenta"]
    # uploaded = files.upload()
    archivos_unidos = 0
    base_fuente1 = pd.DataFrame(columns=columnas_utiles_base_fuente1)
    base_fuente2 = pd.DataFrame(
        columns=columnas_utiles_base_fuente2, dtype=str)
    filenames = []
    for i in files:
      filenames.append(os.path.join(uploads_dir, secure_filename(i.filename)))
    try:
        for fn in filenames:
            # print(('ARCHIVO LEIDO \033[1m' + '"{name}" \033[0m CON TAMAÑO {length} KB').format(
            # name=fn, length=int(len(uploaded[fn]))//(1024)))
            extensión = fn.split(".")[-1]
            try:
                base_fuente2 = base_fuente2.append(pd.read_excel(
                    fn, dtype=str, usecols=columnas_utiles_base_fuente2))
            except:
                try:
                    base_fuente2 = base_fuente2.append(pd.read_excel(
                        fn, dtype=str, usecols=c_bf2).rename(columns={"Unnamed: 18": "WR"}))
                except:
                    if extensión == "xlsx" or extensión == "xls":
                        base_fuente1 = base_fuente1.append(pd.read_excel(fn, usecols=c_bf1).rename(columns={
                                                           "SMSNOMBRE": "NOMBRES", "SMSCLITEL": "TELEFONO", "SMSMSG": "MENSAJE", "CUEN": "Cuenta"}))
                        archivos_unidos += 1
                    elif extensión == "csv":
                        base_fuente1 = base_fuente1.append(pd.read_csv(
                            fn, encoding="ISO-8859-1", usecols=columnas_utiles_base_fuente1))
                        archivos_unidos += 1
                    else:
                        raise Exception(
                            "="*45+"\n"+"==TODOS LOS ARCHIVOS NO ESTÁN EL FORMATO CSV, XLSX, XLS=="+"\n"+"="*45)
        print(colored(
            "============== \033[1mSE HAN LEIDO CORRECTAMENTE LOS ARCHIVOS \033[0m================", "green"))
    except Exception as e:
        # print(traceback.format_exc())
        # or
        # print(sys.exc_info()[2])
        # raise Exception("="*45 + "\n" + "==LOS ARCHIVOS NO TIENEN EL FORMATO ESTABLECIDO==" + "\n" + "Los archivos deben tener las columnas[NOMBRES, TELEFONO, MENSAJE] o [ SMSNOMBRE, SMSCLITEL, SMSMSG] o [ SMSNOMBRE, SMSCLITEL, SMSMSG]" + "\n" + "="*45)
        raise Exception(str(e))
    # return base_fuente1, base_fuente2

    # Selleccionamos solo las columnas utiles de la fuente 1
    # columnas_utiles_base_fuente1 = ["NOMBRES", "TELEFONO", "MENSAJE", "WR", "CUEN"]
    base_fuente1 = base_fuente1[columnas_utiles_base_fuente1]
    columnas_utiles_base_fuente2 = [
        'Nombre', "Celular", 'SMSMSG', "WR", "Cuenta"]
    base_fuente2 = base_fuente2[columnas_utiles_base_fuente2]

    # Renombrar columnas
    mapeo_nombres_columnas_base_fuente1 = {
        "MENSAJE": "Mensaje", "NOMBRES": "Nombre Cliente", "TELEFONO": "Celular"}
    base_fuente1.rename(
        columns=mapeo_nombres_columnas_base_fuente1, inplace=True)

    # mapeo_nombres_columnas_base_fuente2 = {"Nombre": "Nombre Cliente", "SMSCLITEL": "Celular", "Duracion": "Mensaje"}
    mapeo_nombres_columnas_base_fuente2 = {
        "Nombre": "Nombre Cliente", "SMSCLITEL": "Celular", "SMSMSG": "Mensaje", "Cuenta": "CUEN"}
    base_fuente2.rename(
        columns=mapeo_nombres_columnas_base_fuente2, inplace=True)

    """### Filtrar datos no válidos"""

    # Cálculo de la longitud de los campos
    base_fuente1['Celular'] = base_fuente1['Celular'].apply(
        lambda x: str(x).split(".")[0])
    base_fuente1["CaracteresCelular"] = base_fuente1["Celular"].apply(
        lambda x: len(str(x)))
    base_fuente1["CaracteresCliente"] = base_fuente1['Nombre Cliente'].apply(
        lambda x: len(str(x)))
    base_fuente1['No. Caractres'] = base_fuente1['Mensaje'].apply(
        lambda x: len(str(x)))
    base_fuente1['CUEN'] = base_fuente1['CUEN'].apply(
        lambda x: "0"*(12-len(str(x))) + str(x))

    base_fuente2['Celular'] = base_fuente2['Celular'].apply(
        lambda x: str(x).split(".")[0])

    base_fuente2["CaracteresCelular"] = base_fuente2["Celular"].apply(
        lambda x: len(str(x)))
    base_fuente2["CaracteresCliente"] = base_fuente2['Nombre Cliente'].apply(
        lambda x: len(str(x)))
    base_fuente2['No. Caractres'] = base_fuente2['Mensaje'].apply(
        lambda x: len(str(x)))
    base_fuente2['WR'] = base_fuente2['WR'].apply(lambda x: "WR " + str(x))
    base_fuente2['CUEN'] = base_fuente2['CUEN'].apply(
        lambda x: "0"*(12-len(str(x))) + str(x))

    base_fuente2["CaracteresCelular"].value_counts()

    base_fuente2["CaracteresCelular"].value_counts()
    base_fuente2[base_fuente2["CaracteresCelular"] == 10]

    base_fuente1 = base_fuente1[((base_fuente1["CaracteresCelular"] >= 9) & (base_fuente1["CaracteresCelular"] < 10)) & (
        base_fuente1["CaracteresCliente"] > 1) & (base_fuente1['No. Caractres'] > 50)]
    base_fuente2 = base_fuente2[((base_fuente2['Celular'] != "9999999999") & (base_fuente2['Celular'] != "Celular")) & ((base_fuente2["CaracteresCelular"] >= 9) & (
        base_fuente2["CaracteresCelular"] < 10)) & (base_fuente2["CaracteresCliente"] > 1) & (base_fuente2['No. Caractres'] > 50)]

    """### AJUSTE DEL MENSAJE PARA QUE TENGA COMO MÁXIMO 150 CARACTERES
  #### Eliminacion de la letra Ñ y tildes del mensaje
  """
    base_fuente1["Mensaje"] = quitar_tildes(base_fuente1["Mensaje"])
    base_fuente2["Mensaje"] = quitar_tildes(base_fuente2["Mensaje"])
# Eliminar las filas que no tienen mensaje, telefono o cliente
    base_fuente1 = reducir_caracteres_mensaje(base_fuente1)
    base_fuente1.drop(columns=["Mensaje", 'No. Caractres',
                      "CaracteresCelular", "CaracteresCliente"], inplace=True)
    base_fuente1.rename(columns={"Mensaje corto": "Mensaje"}, inplace=True)

    base_fuente2 = reducir_caracteres_mensaje(base_fuente2)
    base_fuente2.drop(columns=["Mensaje", 'No. Caractres',
                      "CaracteresCelular", "CaracteresCliente"], inplace=True)
    base_fuente2.rename(columns={"Mensaje corto": "Mensaje"}, inplace=True)

    """### Correcciones de los tipos de datos"""

    base_fuente1["Celular"] = base_fuente1["Celular"].astype(float)
    base_fuente1["Celular"] = base_fuente1["Celular"].astype(int)
    base_fuente1["Celular"] = base_fuente1["Celular"].apply(
        lambda x: "0" + str(x))

    base_fuente2["Celular"] = base_fuente2["Celular"].astype(float)
    base_fuente2["Celular"] = base_fuente2["Celular"].astype(int)
    base_fuente2["Celular"] = base_fuente2["Celular"].apply(
        lambda x: "0" + str(x))

    """### Unión de archivos"""

    consolidado = base_fuente1.append(base_fuente2)

    consolidado.reset_index(drop=True, inplace=True)
    consolidado = consolidado.iloc[consolidado.agg(
        {"Mensaje": len}).sort_values('Mensaje', ascending=False).index]
    consolidado.reset_index(drop=True, inplace=True)
    # msg = consolidado["Mensaje"].tail(1)[0]
    msg = consolidado["Mensaje"].iat[-1]
    wr = consolidado["WR"].iat[-1]
    cuen = consolidado["CUEN"].iat[-1]
    consolidado.loc[-1] = ["Richar Edmundo Samaniego Leòn ",
                           "0984363757", wr, cuen, msg]
    consolidado.reset_index(drop=True, inplace=True)
    consolidado.loc[-1] = ["Juana Cristina Idrovo Cordero",
                           "0984366133", wr, cuen, msg]
    consolidado.reset_index(drop=True, inplace=True)
    consolidado.loc[-1] = ["karla Guillèn Montenegro",
                           "0984822092", wr, cuen, msg]
    consolidado.reset_index(drop=True, inplace=True)
    consolidado.loc[-1] = ["Juan Fernando Bueno bailòn ",
                           "0992956294", wr, cuen, msg]
    consolidado.reset_index(drop=True, inplace=True)

    # consolidado.loc[-1] = ["Richar Edmundo Samaniego Leòn ", "0984363757", .tail(1)[0]]
    consolidado["Mensaje"].iat[-1]

    consolidado.rename(columns={"Nombre Cliente": "NOMBRE_CLIENTE",
                       "Celular": "CELULAR",	"Mensaje": "MENSAJE_CLIENTE"}, inplace=True)
    columnas_consolidado = ["CELULAR", "CONVENCIONAL", "OFICINA", "ACUERDO_COMERCIAL",
                            "CORREO_CLIENTE", "EMPRESA_DISTRIBUIDORA", "MENSAJE_CLIENTE", "NOMBRE_CLIENTE"]

    consolidado["EMPRESA_DISTRIBUIDORA"] = "05_CENTROSUR_Cuenca"
    consolidado["ACUERDO_COMERCIAL"] = consolidado["CUEN"]

    consolidado[["CONVENCIONAL", "OFICINA", "CORREO_CLIENTE"]] = ""

    consolidado["OFICINA"] = consolidado["WR"]
    consolidado.drop(columns=["WR"], inplace=True)
    consolidado.drop(columns=["CUEN"], inplace=True)

    consolidado = consolidado[columnas_consolidado]

    """### Extras"""

    consolidado["Caracteres"] = consolidado["MENSAJE_CLIENTE"].apply(
        lambda x: len(x))
    consolidado[["MENSAJE_CLIENTE", "Caracteres"]]

    consolidado["CELULAR"].apply(lambda x: len(x)).value_counts()

    consolidado[consolidado["Caracteres"] >
                150][["MENSAJE_CLIENTE", "Caracteres"]]

    consolidado[consolidado["Caracteres"] ==
                150][["MENSAJE_CLIENTE", "Caracteres"]]

    """### Verificación de longitud del mensaje"""

    consolidado[consolidado["Caracteres"] >
                150][["MENSAJE_CLIENTE", "Caracteres"]]

    consolidado["Caracteres"] = consolidado["MENSAJE_CLIENTE"].apply(
        lambda x: len(x))
    consolidado[["MENSAJE_CLIENTE", "Caracteres"]]

    revisar_longitud = ""

    if len(consolidado[consolidado["Caracteres"] > 150]) > 0:
        revisar_longitud = "REVISAR CANTIDAD CARACTERES"
        # consolidado.sort_values(key=lambda x)
        # raise Exception("EL MENSAJE TIENE MAS DE 150 CARACTERES")
        consolidado.drop(columns=["Caracteres"], inplace=True)
    else:
        # consolidado[consolidado["Caracteres"]>150][["MENSAJE_CLIENTE", "Caracteres"]]
        consolidado.drop(columns=["Caracteres"], inplace=True)
    consolidado.drop_duplicates(inplace=True)
    """### Generación archivo EXCEL y CSV"""
    from datetime import date
    today = date.today()
    filename = revisar_longitud + "consolidado"
    # filename = f"FORMATO PARA CONVERSIÓN {str(today)}"
    consolidado.to_excel(home_salida + filename + ".xlsx",
                         index=False, encoding='utf-8-sig')
    consolidado.to_csv(home_salida + filename + ".csv",
                       index=False, encoding='utf-8-sig')
    # return File(home_salida + filename + ".csv")

# python main method


def main():
    files = ["21.06.2022_COD.xlsx", "SIGADE_2022-06-21.csv"]
    read_files(files)
# main()
