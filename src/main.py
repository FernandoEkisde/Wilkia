import flet as ft

def calcular_wilks(sexo, peso, levantado):
    if sexo.lower() == "masculino":
        a, b, c, d, e, f = -216.0475144, 16.2606339, -0.002388645, -0.00113732, 7.01863E-06, -1.291E-08
    else:  # femenino
        a, b, c, d, e, f = 594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 0.00004731582, -0.00000009054

    coef = 500 / (
        a + b*peso + c*peso**2 + d*peso**3 + e*peso**4 + f*peso**5
    )
    return coef * levantado

def main(page: ft.Page):
    page.title = "Wilkia"
    page.theme_mode = ft.ThemeMode.LIGHT
    participantes = []
    drawer = ft.NavigationDrawer()

    output = ft.Text()
    nombre_input = ft.TextField(label="Nombre del participante")
    peso_input = ft.TextField(label="Peso corporal (kg)", keyboard_type=ft.KeyboardType.NUMBER)
    levantado_input = ft.TextField(label="Peso levantado (kg)", keyboard_type=ft.KeyboardType.NUMBER)
    sexo_dropdown = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")]
    )

    resultado_info = ft.Text("Selecciona un participante para ver sus datos.", selectable=True)

    def agregar_participante(e):
        try:
            nombre = nombre_input.value
            peso = float(peso_input.value)
            levantado = float(levantado_input.value)
            sexo = sexo_dropdown.value

            puntos = calcular_wilks(sexo, peso, levantado)
            id_participante = len(participantes) + 1

            info = {
                "id": id_participante,
                "nombre": nombre,
                "sexo": sexo,
                "peso": peso,
                "levantado": levantado,
                "wilks": round(puntos, 2)
            }
            participantes.append(info)

            drawer.controls.append(
                ft.NavigationDrawerDestination(
                    icon=ft.Icon(ft.Icons.PERSON),
                    label=f"{id_participante}. {nombre}",
                    selected_icon=ft.Icon(ft.Icons.CHECK),
                    data=info
                )
            )
            page.update()
            output.value = f"{nombre} agregado con {round(puntos,2)} puntos Wilks."
            nombre_input.value = peso_input.value = levantado_input.value = ""
        except Exception as ex:
            output.value = f"Error: {str(ex)}"
        page.update()

    def mostrar_drawer(e):
        page.drawer = drawer
        page.drawer.open = True
        page.update()

    def drawer_change(e):
        data = e.control.controls[e.control.selected_index].data
        resultado_info.value = (
            f"Nombre: {data['nombre']}\n"
            f"Sexo: {data['sexo']}\n"
            f"Peso corporal: {data['peso']} kg\n"
            f"Peso levantado: {data['levantado']} kg\n"
            f"Puntos Wilks: {data['wilks']}"
        )
        page.update()

    drawer.on_change = drawer_change

    page.add(
        ft.Column([
            ft.Text("Calculadora sencilla de puntos Wilks.", size=24, weight="bold"),
            nombre_input,
            peso_input,
            levantado_input,
            sexo_dropdown,
            ft.ElevatedButton("Agregar participante", on_click=agregar_participante),
            output,
            ft.ElevatedButton("Mostrar lista de participantes", on_click=mostrar_drawer),
            resultado_info
        ])
    )

ft.app(target=main)

