import base64
import hashlib
import pathlib
import sys
from typing import Annotated

import pwinput  # type: ignore
import typer
from cryptography.fernet import Fernet, InvalidToken

cli = typer.Typer()


def create_password():
    # запрашиваем пароль
    password = pwinput.pwinput(prompt="Введите пароль: ", mask="👾")

    if len(password) < 1:
        typer.secho(
            "Пароль не может быть пуст !", fg=typer.colors.RED, bg=typer.colors.BLACK
        )
        sys.exit()

    # создаем ключ на основе пароля
    hashed_password = hashlib.sha256(password.encode()).digest()
    key = base64.urlsafe_b64encode(hashed_password)

    return Fernet(key)


@cli.command()
def encryption(
    file_to_encryption: Annotated[str, typer.Option("--file", "-f")],
    new_file_name: Annotated[str, typer.Option("--new-name", "-nn")],
):
    # шифруем данные
    if not pathlib.Path(file_to_encryption).exists():
        typer.secho(
            f"{file_to_encryption} Файла не существует !",
            fg=typer.colors.RED,
            bg=typer.colors.BLACK,
        )
        sys.exit()
    with open(file_to_encryption, "rb") as file:
        ffernet_ = create_password()
        encryption_data = ffernet_.encrypt(file.read())
        with open(new_file_name, "wb") as file:
            file.write(encryption_data)
        typer.secho(
            "Файл успешно зашифрован !", fg=typer.colors.BLUE, bg=typer.colors.BLACK
        )


@cli.command()
def dencryption(
    file_to_dencryption: Annotated[str, typer.Option("--file", "-f")],
    new_file_name: Annotated[str, typer.Option("--new-name", "-nn")],
):
    # расшифровываем данные
    if not pathlib.Path(file_to_dencryption).exists():
        typer.secho(
            f"{file_to_dencryption} Файла не существует !",
            fg=typer.colors.RED,
            bg=typer.colors.BLACK,
        )
        sys.exit()
    with open(file_to_dencryption, "rb") as file:
        ffernet_ = create_password()
        try:
            data_decryption = ffernet_.decrypt(file.read())
        except InvalidToken:
            typer.secho(
                "Расшифровка не удалась, не верный ключ !",
                fg=typer.colors.RED,
                bg=typer.colors.BLACK,
            )
            sys.exit()
        with open(new_file_name, "wb") as file:
            file.write(data_decryption)
        typer.secho(
            "Файл успешно расшифрован !", fg=typer.colors.GREEN, bg=typer.colors.BLACK
        )


if __name__ == "__main__":
    cli()
