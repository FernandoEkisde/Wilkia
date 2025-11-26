import flet as ft

# ---------------------------
#  Cálculo de discos
# ---------------------------

def calcular_discos(peso_objetivo: float, peso_barra: float):
    discos = [25, 20, 10, 5, 2.5, 1.25, 0.5]
    restante_total = peso_objetivo - peso_barra
    if restante_total < 0:
        return "El peso objetivo es menor que el peso de la barra."

    por_lado = restante_total / 2
    resultado = {}
    for d in discos:
        cantidad = int(por_lado // d)
        if cantidad > 0:
            resultado[d] = cantidad
            por_lado -= cantidad * d
    return resultado


# ---------------------------
#  Cálculo Wilks
# ---------------------------

def coeficiente_wilks(peso_corporal: float, sexo: str) -> float:
    w = peso_corporal
    if sexo == "Masculino":
        a, b, c, d, e, f = -216.0475144, 16.2606339, -0.002388645, -0.00113732, 7.01863e-06, -1.291e-08
    else:
        a, b, c, d, e, f = 594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 4.731582e-05, -9.054e-08
    denom = a + b*w + c*w**2 + d*w**3 + e*w**4 + f*w**5
    return 500.0 / denom if denom != 0 else 0.0


# ---------------------------
#  APLICACIÓN PRINCIPAL
# ---------------------------

def main(page: ft.Page):
    page.title = "Competencia de Fuerza"
    page.scroll = "auto"

    participantes = []
    contenedor_participantes = ft.Column(scroll="auto", expand=True)
    resultado = ft.Text("", size=16, weight="bold")

    # Peso de la barra
    peso_barra = ft.TextField(label="Peso de la barra (kg)", value="20", width=150)

    # ===========================
    #  DIALOGO PARA LOS DISCOS
    # ===========================

    dialogo_discos = ft.AlertDialog(
        modal=True,
        title=ft.Text("Distribución de Discos"),
        content=ft.Text(""),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(e))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def cerrar_dialogo(e):
        dialogo_discos.open = False
        page.update()

    def mostrar_discos(field):
        try:
            objetivo = float(field.value)
            barra = float(peso_barra.value)
            discos = calcular_discos(objetivo, barra)

            if isinstance(discos, dict):
                detalle = "\n".join([f"{v} × {k} kg por lado" for k, v in discos.items()])
            else:
                detalle = discos
        except:
            detalle = "Ingrese un valor válido"

        dialogo_discos.content = ft.Text(detalle)

        # IMPORTANTE: agregar al overlay antes de abrir
        if dialogo_discos not in page.overlay:
            page.overlay.append(dialogo_discos)

        dialogo_discos.open = True
        page.update()

# ---------------------------
    #  Agregar participante
    # ---------------------------

    def agregar_participante(e):
        idx = len(participantes) + 1
        nombre = ft.TextField(label=f"Nombre del Participante {idx}")
        sexo = ft.Dropdown(label="Sexo", options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino")])
        peso_corporal = ft.TextField(label="Peso corporal (kg)", keyboard_type=ft.KeyboardType.NUMBER)

        intentos = []
        intentos_column = ft.Column()

        # ---- eliminar intento ----
        def eliminar_intento(e, obj):
            intentos_column.controls.remove(obj['container'])
            intentos.remove(obj)
            for i, it in enumerate(intentos, 1):
                it['field'].label = f"Intento N°{i} (kg)"
            page.update()

        # ---- agregar intento ----
        def agregar_intento(e=None):
            n = len(intentos) + 1
            field = ft.TextField(label=f"Intento N°{n} (kg)", keyboard_type=ft.KeyboardType.NUMBER)

            btn_eliminar = ft.ElevatedButton("🗑️", width=40)
            btn_calcular = ft.ElevatedButton("Discos", width=80,
                                             on_click=lambda e, f=field: mostrar_discos(f))

            row = ft.Row([field, btn_calcular, btn_eliminar], alignment="spaceBetween")
            intento = {"field": field, "container": row}

            btn_eliminar.on_click = lambda e, obj=intento: eliminar_intento(e, obj)

            intentos.append(intento)
            intentos_column.controls.append(row)
            page.update()

        # Crear primer intento por defecto
        agregar_intento()

        # Contenedor del competidor
        contenedor = ft.Container(border=ft.border.all(1), padding=10, margin=5)

        def eliminar_participante(e, cont):
            contenedor_participantes.controls.remove(cont)
            participantes[:] = [p for p in participantes if p["contenedor"] != cont]
            page.update()

        btn_agregar_int = ft.ElevatedButton("Agregar Intento", on_click=agregar_intento)
        btn_eliminar_part = ft.ElevatedButton("❌ Eliminar Participante", bgcolor="red",
                                              on_click=lambda e, c=contenedor: eliminar_participante(e, c))

        contenedor.content = ft.Column([
            nombre,
            sexo,
            peso_corporal,
            intentos_column,
            ft.Row([btn_agregar_int, btn_eliminar_part])
        ])

        participantes.append({
            "nombre": nombre,
            "sexo": sexo,
            "peso": peso_corporal,
            "intentos": intentos,
            "contenedor": contenedor
        })

        contenedor_participantes.controls.append(contenedor)
        page.update()

    # ---------------------------
    #  Ranking Wilks
    # ---------------------------

    def mostrar_ranking_wilks(e):
        ranking = []
        for p in participantes:
            try:
                peso = float(p["peso"].value)
                coef = coeficiente_wilks(peso, p["sexo"].value)
                total = sum(float(i["field"].value) for i in p["intentos"] if i["field"].value)
                ranking.append((p["nombre"].value, coef * total))
            except:
                continue

        ranking.sort(key=lambda x: x[1], reverse=True)
        if ranking:
            texto = "🏆 Ranking Wilks:\n" + "\n".join(
                f"{i}. {n}: {p:.1f} pts" for i, (n, p) in enumerate(ranking, 1)
            )
        else:
            texto = "No hay datos válidos para Wilks"
        resultado.value = texto
        page.update()

    # ---------------------------
    #  Ranking Fuerza Bruta
    # ---------------------------

    def mostrar_ranking_fuerza(e):
        ranking = []
        for p in participantes:
            try:
                maximo = max(float(i["field"].value) for i in p["intentos"] if i["field"].value)
                ranking.append((p["nombre"].value, maximo))
            except:
                continue

        ranking.sort(key=lambda x: x[1], reverse=True)
        if ranking:
            texto = "💪 Ranking Fuerza Bruta:\n" + "\n".join(
                f"{i}. {n}: {w:.1f} kg" for i, (n, w) in enumerate(ranking, 1)
            )
        else:
            texto = "No hay datos válidos para fuerza bruta"

        resultado.value = texto
        page.update()

    # ---------------------------
    #  Filtrar peso
    # ---------------------------

    def ordenar_por_peso(e):
        # Crear lista temporal con (participante, peso_max)
        lista = []
        for p in participantes:
            try:
                maximo = max(
                    float(i["field"].value)
                    for i in p["intentos"]
                    if i["field"].value
                )
                lista.append((p, maximo))
            except:
                continue

        # Ordenar de menor a mayor
        lista.sort(key=lambda x: x[1])

        # Limpiar el contenedor
        contenedor_participantes.controls.clear()

        # Reagregar según el nuevo orden
        for p, _ in lista:
            contenedor_participantes.controls.append(p["contenedor"])

        page.update()


    # ===========================
    #  UI PRINCIPAL
    # ===========================

    page.add(
        ft.Column([
            ft.Row([
                ft.ElevatedButton("Agregar Participante", on_click=agregar_participante),
                ft.ElevatedButton("🏆 Ranking Wilks", on_click=mostrar_ranking_wilks),
                ft.ElevatedButton("💪 Ranking Fuerza", on_click=mostrar_ranking_fuerza),
                ft.ElevatedButton("📉 Ordenar por peso (menor a mayor)", on_click=ordenar_por_peso),
                peso_barra,
            ]),
            ft.Container(contenedor_participantes, expand=True),
            ft.Divider(),
            resultado
        ], expand=True)
    )


if __name__ == "__main__":
    ft.app(main)

