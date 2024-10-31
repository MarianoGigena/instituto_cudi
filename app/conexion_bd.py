import mysql.connector


def obtener_conexion():
    return mysql.connector.connect(
        host="bpwepioek9qlpkrlo58y-mysql.services.clever-cloud.com",
        user="ufrojjoexr0lrd1y",
        password="UrDrhOOhFRzlF3r3FVYI",
        database="bpwepioek9qlpkrlo58y",
    )
