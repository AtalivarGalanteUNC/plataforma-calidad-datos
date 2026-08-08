import sys

from app.application.ejecutar_check import ejecutar_check


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python -m scripts.ejecutar_check <check_id>")
        sys.exit(1)

    try:
        check_id = int(sys.argv[1])
    except ValueError:
        print(f"El check_id tiene que ser un número entero, no {sys.argv[1]!r}")
        sys.exit(1)

    resultado = ejecutar_check(check_id)
    print(f"Check {check_id}: {resultado.estado.upper()}", end="")

    if resultado.valor_medido is not None:
        print(f" — valor medido: {resultado.valor_medido}", end="")

    if resultado.mensaje is not None:
        print(f" — {resultado.mensaje}", end="")

    print()


if __name__ == "__main__":
    main()