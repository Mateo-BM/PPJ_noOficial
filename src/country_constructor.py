class country_constructor:
    def __init__(self, country):
        # Define el tab_start en función del país seleccionado
        if country == "Costa Rica":
            self.tab_start = '/pj/app/inicio.php?op=menu1&cy=CR&co=PJ'
            self.tab_report = 'reporte.php?op=menu&cy=CR&co=PJ'
            self.tab_header_report = '../app/reporte.php?op=menu&cy=CR&co=PJ'
            self.tab_report
        elif country == "Guatemala":
            self.tab_start = '/pj/app/inicio.php?op=menu1&cy=GT&co=PJ'
            self.tab_report = 'reporte.php?op=menu&cy=GT&co=PJ'
            self.tab_header_report = '../app/reporte.php?op=menu&cy=GT&co=PJ'
        else:
            raise ValueError(f"País no válido: {country}. Selecciona 'Costa Rica' o 'Guatemala'.")