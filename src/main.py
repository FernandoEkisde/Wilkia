import flet as ft


def main(page: ft.Page):
    page.scroll = "auto"

    participantes = []
    contenedor_participantes = ft.Column(scroll="auto", expand=True)
    resultado = ft.Text("", size=16, weight="bold")

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

        intentos = []  # lista de diccionarios {field: TextField, container: Row}
        intentos_column = ft.Column()

        def eliminar_intento(e, intento_obj):
            # Remueve visualmente
            intentos_column.controls.remove(intento_obj['container'])
            # Remueve de la lista
            intentos.remove(intento_obj)
            # Renumera las etiquetas
            for idx, obj in enumerate(intentos, start=1):
                obj['field'].label = f"Intento N°{idx} (kg)"
            page.update()

        def agregar_intento(e=None):
            intento_num = len(intentos) + 1
            field = ft.TextField(label=f"Intento N°{intento_num} (kg)", keyboard_type=ft.KeyboardType.NUMBER)
            # Crear fila con field y botón eliminar
            btn_elim = ft.ElevatedButton("🗑️", on_click=lambda e, obj={'field': field, 'container': None}: eliminar_intento(e, obj), width=40)
            fila = ft.Row([field, btn_elim], alignment="spaceBetween")
            # Asociar container en el objeto
            intento_obj = {'field': field, 'container': fila}
            # Actualizar lambda referencia
            btn_elim.on_click = lambda e, obj=intento_obj: eliminar_intento(e, obj)

            intentos.append(intento_obj)
            intentos_column.controls.append(fila)
            page.update()

        agregar_intento()  # primer intento por defecto

        # Inicializa el contenedor para poder referenciarlo en la función de eliminación del participante
        contenedor = ft.Container()

        def eliminar_participante(e):
            contenedor_participantes.controls.remove(contenedor)
            for p in participantes:
                if p.get("contenedor") == contenedor:
                    participantes.remove(p)
                    break
            page.update()

        boton_eliminar = ft.ElevatedButton(
            text="❌ Eliminar Participante",
            on_click=eliminar_participante,
            bgcolor="red"
        )

        contenedor.content = ft.Column([
            nombre,
            sexo,
            peso_corporal,
            intentos_column,
            ft.Row([
                ft.ElevatedButton("Agregar Intento", on_click=agregar_intento),
                boton_eliminar
            ])
        ])
        contenedor.border = ft.border.all(1)
        contenedor.padding = 10
        contenedor.margin = 5

        participantes.append({
            "id": id_participante,
            "nombre": nombre,
            "sexo": sexo,
            "peso": peso_corporal,
            "intentos": intentos,
            "contenedor": contenedor
        })

        contenedor_participantes.controls.append(contenedor)
        page.update()

    def mostrar_ganador(e):
        mejor = None
        for p in participantes:
            try:
                sexo_val = p["sexo"].value
                wilks_coef = 0.60 if sexo_val == "Masculino" else 0.65

                puntos = []
                for obj in p["intentos"]:
                    try:
                        valor = float(obj['field'].value)
                        puntos.append(calcular_puntos(wilks_coef, valor))
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
                pesos = [float(obj['field'].value) for obj in p["intentos"] if obj['field'].value]
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
                resultado
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(main)
