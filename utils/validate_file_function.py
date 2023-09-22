import pandas as pd
import os



def get_test_data(folderpath:str) -> pd.DataFrame:
    """
    Lire du fichier de donnees test et retourne la liste des RECL_ID_CAT sous 
    forme de DataFrame

    Args:
        folderpath (str): chemin complet du repos

    Returns:
        pd.DataFrame: dataframe des de la colonne RECL_ID_CAT des donnees test
    """    
    try:
        with open(f'{folderpath}\\donnees\\test.csv') as csv_file:
            df_test = pd.read_csv(csv_file)
    except:
        raise Exception("Assurez-vous que le fichier test.csv est au même endroit et a le même nom que dans le bitbucket")
    
    if ('RECL_ID_CAT' not in df_test.columns)\
        or (df_test.shape[0] != 100_000):
        raise Exception("Assurez-vous que le fichier test.csv n'a pas été modifié")

    return df_test[['RECL_ID_CAT']]


def validation_csv(filename: str,
                   folderpath: str) -> str:
    """
    Fonction qui valide que le fichier de prediction est conforme 
    au format attendu pour la correction. La fonction "Raise" une exception
    lorsqu'une erreur est detectee

    Args:
        filename (str): nom du fichier (excluant l'extension .csv)
        folderpath (str): chemin complet du repos

    Returns:
        str: Message de succès lorsque tout est conforme
    """    
    id_list = get_test_data(folderpath=folderpath)

    if not isinstance(filename, str):
        return "filename n'est pas un charactere!"
    
    if not isinstance(folderpath, str):
        return "foldername n'est pas un charactere!"
    
    file_path = f'{folderpath}\\prediction\\{filename}.csv'
    
    with open(file_path) as csv_file:
        df_pred = pd.read_csv(csv_file)
    
    # validation colonnes
    if len(df_pred.columns) != 2:
        raise Exception("Le fichier de predictions doit seulement contenir les colonnes suivantes: 'RECL_ID_CAT', 'PRED' ")
    for col in df_pred.columns:
        if col not in ['RECL_ID_CAT', 'PRED']:
            raise Exception("Le fichier de predictions doit seulement contenir les colonnes suivantes: 'RECL_ID_CAT', 'PRED' ")

    # validations nombre de lignes
    if id_list.shape[0] != df_pred.shape[0]:
        raise Exception(f"Le fichier de prediction doit avoir {str(id_list.shape[0])} lignes")

    #validation des valeurs
    for col in ['RECL_ID_CAT', 'PRED']:
        if df_pred[col].isna().sum() > 0:
            raise Exception(f"La colonne '{col}' du fichier de prediction contient des NA")

    for value in df_pred['PRED'].unique():
        if value not in [0, 1, 2]:
            raise Exception(f"La colonne PRED doit seulement contenir les valeurs 0, 1, ou 2. Nous avons detecte '{str(value)}'")
    try:
        if (id_list['RECL_ID_CAT'].sort_values() == df_pred['RECL_ID_CAT'].sort_values()).sum() != df_pred.shape[0]:
            raise Exception('RECL_ID_CAT du fichier prediction ne concorde pas avec les RECL_ID_CAT du fichier test.csv')
    except:
        raise Exception('RECL_ID_CAT du fichier prediction ne concorde pas avec les RECL_ID_CAT du fichier test.csv')

    return "Super, le fichier de prediction est conforme! Bonne chance :)"