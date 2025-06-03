import sys

def calcular_IMC(peso, altura):
    return peso / (altura ** 2)

def calcula_porcentaje_grasa(peso, altura, edad, valor_genero):
    imc = calcular_IMC(peso, altura)
    return 1.2 * imc + 0.23 * edad - valor_genero

def calcular_calorias_en_reposo(peso, altura, edad, valor_genero):
    return (10 * peso) + (6.25 * altura * 100) - (5 * edad) + valor_genero

def calcular_calorias_en_actividad(peso, altura, edad, valor_genero, valor_actividad):
    tmb = calcular_calorias_en_reposo(peso, altura, edad, valor_genero)
    return tmb * valor_actividad

def consumo_calorias_recomendado(peso, altura, edad, valor_genero):
    tmb = calcular_calorias_en_reposo(peso, altura, edad, valor_genero)
    rango_inferior = tmb * 0.80
    rango_superior = tmb * 0.85
    return (int(rango_inferior), int(rango_superior))

def guardarInfoPaciente(nombre_archivo, datos, resultado):
    with open(nombre_archivo, "a", encoding="utf-8") as archivo:
        archivo.write("=== NUEVO PACIENTE ===\n")
        for clave, valor in datos.items():
            archivo.write(f"{clave}: {valor}\n")
        archivo.write(f"Resultado: {resultado}\n")
        archivo.write("=======================\n\n")

def datosGenerales():
    nombre = input("Nombre del paciente: ").strip()
    peso = float(input("Peso (kg): "))
    altura = float(input("Altura (m): "))
    return nombre, peso, altura

def datosCompletos():
    nombre, peso, altura = datosGenerales()
    edad = int(input("Edad: "))
    genero_str = input("Género (masculino/femenino): ").strip().lower()
    if genero_str not in ("masculino", "femenino"):
        print("Género inválido. Se asumirá femenino por defecto.")
        genero_str = "femenino"
    generoCalorias = 5 if genero_str == "masculino" else -161
    generoGrasa = 10.8 if genero_str == "masculino" else 0
    return nombre, peso, altura, edad, genero_str, generoCalorias, generoGrasa

def opcionIMC():
    print("\n--- Cálculo de IMC ---")
    nombre, peso, altura = datosGenerales()
    imc = calcular_IMC(peso, altura)
    print(f"Su IMC es: {imc:.2f}")
    datos = {
        "Nombre": nombre,
        "Peso": peso,
        "Altura": altura
    }
    resultado = f"IMC = {imc:.2f}"
    guardarInfoPaciente("pacientes.txt", datos, resultado)
    input("\nPresione Enter para volver al menú...")

def opcionPorcentajeGrasa():
    print("\n--- Cálculo de Porcentaje de Grasa Corporal ---")
    nombre, peso, altura, edad, genero_str, _, valor_genero_grasa = datosCompletos()
    grasa = calcula_porcentaje_grasa(peso, altura, edad, valor_genero_grasa)
    print(f"Su porcentaje de grasa corporal es: {grasa:.2f}%")
    datos = {
        "Nombre": nombre,
        "Peso": peso,
        "Altura": altura,
        "Edad": edad,
        "Género": genero_str
    }
    resultado = f"% Grasa corporal = {grasa:.2f}%"
    guardarInfoPaciente("pacientes.txt", datos, resultado)
    input("\nPresione Enter para volver al menú...")

def opcionCaloriasReposo():
    print("\n--- Cálculo de Calorías en Reposo (TMB) ---")
    nombre, peso, altura, edad, genero_str, valor_genero_calorias, _ = datosCompletos()
    tmb = calcular_calorias_en_reposo(peso, altura, edad, valor_genero_calorias)
    print(f"Su tasa metabólica basal (reposo) es: {tmb:.2f} calorías diarias")
    datos = {
        "Nombre": nombre,
        "Peso": peso,
        "Altura": altura,
        "Edad": edad,
        "Género": genero_str
    }
    resultado = f"TMB en reposo = {tmb:.2f} calorías"
    guardarInfoPaciente("pacientes.txt", datos, resultado)
    input("\nPresione Enter para volver al menú...")

def opcionCaloriasActividad():
    print("\n--- Cálculo de Calorías según Nivel de Actividad ---")
    nombre, peso, altura, edad, genero_str, valor_genero_calorias, _ = datosCompletos()
    print("\nNivel de actividad física:")
    print("1. Poco o ningún ejercicio")
    print("2. Ejercicio ligero (1-3 días/semana)")
    print("3. Ejercicio moderado (3-5 días/semana)")
    print("4. Deportista (6-7 días/semana)")
    print("5. Atleta (entrenamiento doble)")
    opcion = int(input("Seleccione una opción (1-5): "))
    valores_actividad = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.72, 5: 1.9}
    valor_actividad = valores_actividad.get(opcion, 1.2)
    tmb_actividad = calcular_calorias_en_actividad(peso, altura, edad, valor_genero_calorias, valor_actividad)
    print(f"Calorías estimadas diarias según su actividad: {tmb_actividad:.2f}")
    datos = {
        "Nombre": nombre,
        "Peso": peso,
        "Altura": altura,
        "Edad": edad,
        "Género": genero_str,
        "Nivel actividad": opcion
    }
    resultado = f"TMB con actividad = {tmb_actividad:.2f} calorías"
    guardarInfoPaciente("pacientes.txt", datos, resultado)
    input("\nPresione Enter para volver al menú...")

def opcionAdelgazar():
    print("\n--- Recomendación de Consumo de Calorías para Adelgazar ---")
    nombre, peso, altura, edad, genero_str, valor_genero_calorias, _ = datosCompletos()
    rango_inferior, rango_superior = consumo_calorias_recomendado(peso, altura, edad, valor_genero_calorias)
    print(f"Para adelgazar se recomienda consumir entre {rango_inferior} y {rango_superior} calorías al día.")
    datos = {
        "Nombre": nombre,
        "Peso": peso,
        "Altura": altura,
        "Edad": edad,
        "Género": genero_str
    }
    resultado = f"Recomendación = {rango_inferior}-{rango_superior} calorías"
    guardarInfoPaciente("pacientes.txt", datos, resultado)
    input("\nPresione Enter para volver al menú...")

def menuprincipal():
    while True:
        print("\n==============================")
        print("   Calculadora de Índices    ")
        print("==============================")
        print("1. Calcular IMC")
        print("2. Calcular % de Grasa Corporal")
        print("3. Calcular Calorías en Reposo (TMB)")
        print("4. Calcular Calorías según Actividad")
        print("5. Recomendación para Adelgazar")
        print("6. Salir")
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            opcionIMC()
        elif opcion == "2":
            opcionPorcentajeGrasa()
        elif opcion == "3":
            opcionCaloriasReposo()
        elif opcion == "4":
            opcionCaloriasActividad()
        elif opcion == "5":
            opcionAdelgazar()
        elif opcion == "6":
            print("¡Hasta luego!")
            sys.exit()
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menuprincipal()
