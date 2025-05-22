import flet as ft

def main(page: ft.Page):
    page.scroll = "auto"

    participantes = []
    tabla_resultados = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Promedio Wilks")),
            ft.DataColumn(label=ft.Text("Peso Máximo")),
        ],
        rows=[]
    )

    resultado = ft.Text("", size=16, weight="bold")
    contenedor_participantes = ft.Column(scroll="auto", expand=True)

    def calcular_puntos(wilks_coef, peso_levantado):
        return wilks_coef * peso_levantado

    def agregar_participante(e):
        id_participante = len(participantes) + 1
        nombre = ft.TextField(label=f"Nombre del Participante {id_participante}")
        sexo = ft.Dropdown(label="Sexo", options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino")
        ])
        peso_corporal = ft.TextField(label="Peso corporal (kg)", keyboard_type=ft.KeyboardType.NUMBER)

        intentos = []

        def agregar_intento(e=None):
            intento_num = len(intentos) + 1
            intento_peso = ft.TextField(label=f"Intento N°{intento_num} (kg)", keyboard_type=ft.KeyboardType.NUMBER)
            intentos.append(intento_peso)
            intentos_column.controls.append(intento_peso)
            page.update()

        intentos_column = ft.Column()
        agregar_intento()  # Añade el primer intento por defecto

        contenedor = ft.Container(
            content=ft.Column([
                nombre,
                sexo,
                peso_corporal,
                intentos_column,
                ft.ElevatedButton("Agregar Intento", on_click=agregar_intento),
            ]),
            border=ft.border.all(1),
            padding=10,
            margin=5
        )

        participantes.append({
            "id": id_participante,
            "nombre": nombre,
            "sexo": sexo,
            "peso": peso_corporal,
            "intentos": intentos
        })

        contenedor_participantes.controls.append(contenedor)
        page.update()

    def mostrar_ganador(e):
        mejor = None
        for p in participantes:
            try:
                peso = float(p["peso"].value)
                sexo = p["sexo"].value
                wilks_coef = 0.0

                # Wilks coefficient (simplificado, puedes poner fórmula real si gustas)
                if sexo == "Masculino":
                    wilks_coef = 0.60
                elif sexo == "Femenino":
                    wilks_coef = 0.65

                puntos = []
                for intento in p["intentos"]:
                    try:
                        peso_intento = float(intento.value)
                        puntos.append(calcular_puntos(wilks_coef, peso_intento))
                    except:
                        continue

                promedio = sum(puntos) / len(puntos) if puntos else 0

                if mejor is None or promedio > mejor["promedio"]:
                    mejor = {"nombre": p["nombre"].value, "promedio": promedio}

            except:
                continue

        if mejor:
            resultado.value = f"🏆 Ganador por puntos Wilks: {mejor['nombre']} con {mejor['promedio']:.2f} puntos"
        else:
            resultado.value = "No se encontraron datos válidos"
        page.update()

    def mostrar_fuerza_bruta(e):
        mas_fuerte = None
        for p in participantes:
            try:
                pesos = [float(i.value) for i in p["intentos"] if i.value]
                max_peso = max(pesos) if pesos else 0

                if mas_fuerte is None or max_peso > mas_fuerte["peso"]:
                    mas_fuerte = {"nombre": p["nombre"].value, "peso": max_peso}
            except:
                continue

        if mas_fuerte:
            resultado.value = f"💪 Participante más fuerte: {mas_fuerte['nombre']} con {mas_fuerte['peso']} kg"
        else:
            resultado.value = "No se encontraron datos válidos"
        page.update()

    # Layout principal
    page.add(
        ft.Column(
            controls=[
                ft.Row([
                    ft.ElevatedButton("Agregar Participante", on_click=agregar_participante),
                    ft.ElevatedButton("🏆 Ver ganador por Wilks", on_click=mostrar_ganador),
                    ft.ElevatedButton("💪 Ver más fuerte", on_click=mostrar_fuerza_bruta),
                ]),
                ft.Container(contenedor_participantes, expand=True),
                ft.Divider(),
                ft.Text("Tabla de resultados:", size=18, weight="bold"),
                tabla_resultados,
                resultado
            ],
            expand=True
        )
    )

ft.app(main)

