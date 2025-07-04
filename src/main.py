import flet as ft

# Cálculo oficial de Wilks según géneros
def coeficiente_wilks(peso_corporal: float, sexo: str) -> float:
    w = peso_corporal
    if sexo == "Masculino":
        a, b, c, d, e, f = -216.0475144, 16.2606339, -0.002388645, -0.00113732, 7.01863e-06, -1.291e-08
    else:
        a, b, c, d, e, f = 594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 4.731582e-05, -9.054e-08
    denom = a + b*w + c*w**2 + d*w**3 + e*w**4 + f*w**5
    return 500.0 / denom if denom != 0 else 0.0


def main(page: ft.Page):
    page.scroll = "auto"
    participantes = []
    contenedor_participantes = ft.Column(scroll="auto", expand=True)
    resultado = ft.Text("", size=16, weight="bold")

    def calcular_puntos(wilks_coef, peso_levantado):
        return wilks_coef * peso_levantado

    def agregar_participante(e):
        idx = len(participantes) + 1
        nombre = ft.TextField(label=f"Nombre del Participante {idx}")
        sexo = ft.Dropdown(label="Sexo", options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")])
        peso_corporal = ft.TextField(label="Peso corporal (kg)", keyboard_type=ft.KeyboardType.NUMBER)

        intentos = []
        intentos_column = ft.Column()

        def eliminar_intento(e, obj):
            intentos_column.controls.remove(obj['container'])
            intentos.remove(obj)
            for i, it in enumerate(intentos, 1):
                it['field'].label = f"Intento N°{i} (kg)"
            page.update()

        def agregar_intento(e=None):
            n = len(intentos) + 1
            field = ft.TextField(label=f"Intento N°{n} (kg)", keyboard_type=ft.KeyboardType.NUMBER)
            btn = ft.ElevatedButton("🗑️", width=40)
            row = ft.Row([field, btn], alignment="spaceBetween")
            intento = {'field': field, 'container': row}
            btn.on_click = lambda e, obj=intento: eliminar_intento(e, obj)
            intentos.append(intento)
            intentos_column.controls.append(row)
            page.update()

        agregar_intento()

        # Crear contenedor vacío primero
        contenedor = ft.Container(border=ft.border.all(1), padding=10, margin=5)

        def eliminar_participante(e, cont):
            contenedor_participantes.controls.remove(cont)
            participantes[:] = [p for p in participantes if p['contenedor'] != cont]
            page.update()

        # Botones ahora que contenedor existe
        btn_agregar_int = ft.ElevatedButton("Agregar Intento", on_click=agregar_intento)
        btn_eliminar_part = ft.ElevatedButton("❌ Eliminar Participante", bgcolor="red",
                                              on_click=lambda e, c=contenedor: eliminar_participante(e, c))

        # Asignar contenido al contenedor
        contenedor.content = ft.Column([
            nombre,
            sexo,
            peso_corporal,
            intentos_column,
            ft.Row([btn_agregar_int, btn_eliminar_part])
        ])

        participantes.append({"nombre": nombre, "sexo": sexo, "peso": peso_corporal,
                              "intentos": intentos, "contenedor": contenedor})
        contenedor_participantes.controls.append(contenedor)
        page.update()

    def mostrar_ranking_wilks(e):
        ranking = []
        for p in participantes:
            try:
                peso = float(p['peso'].value)
                coef = coeficiente_wilks(peso, p['sexo'].value)
                total = sum(float(i['field'].value) for i in p['intentos'] if i['field'].value)
                puntos = coef * total
                ranking.append((p['nombre'].value, puntos))
            except ValueError:
                continue
        ranking.sort(key=lambda x: x[1], reverse=True)
        if ranking:
            texto = "🏆 Ranking Wilks:\n" + "\n".join(f"{i}. {n}: {p:.1f} pts" for i, (n, p) in enumerate(ranking, 1))
        else:
            texto = "No hay datos válidos para Wilks"
        resultado.value = texto
        page.update()

    def mostrar_ranking_fuerza(e):
        ranking = []
        for p in participantes:
            try:
                maximo = max(float(i['field'].value) for i in p['intentos'] if i['field'].value)
                ranking.append((p['nombre'].value, maximo))
            except ValueError:
                continue
        ranking.sort(key=lambda x: x[1], reverse=True)
        if ranking:
            texto = "💪 Ranking Fuerza Bruta:\n" + "\n".join(f"{i}. {n}: {w:.1f} kg" for i, (n, w) in enumerate(ranking, 1))
        else:
            texto = "No hay datos válidos para fuerza bruta"
        resultado.value = texto
        page.update()

    page.add(
        ft.Column([
            ft.Row([
                ft.ElevatedButton("Agregar Participante", on_click=agregar_participante),
                ft.ElevatedButton("🏆 Ver Ranking Wilks", on_click=mostrar_ranking_wilks),
                ft.ElevatedButton("💪 Ver Ranking Fuerza", on_click=mostrar_ranking_fuerza),
            ]),
            ft.Container(contenedor_participantes, expand=True),
            ft.Divider(),
            resultado
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(main)

