from app.application.ingestar_dolar import ingestar_dolar


if __name__ == "__main__":
    guardadas = ingestar_dolar()
    print(f"Ingesta de dólar completada. Cotizaciones nuevas guardadas: {guardadas}")