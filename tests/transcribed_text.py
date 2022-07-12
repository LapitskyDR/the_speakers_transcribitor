import click

import tooc_api


@click.command()
@click.option('--audio_path', type=str,
              help="Путь к аудиофайлу в формате WAV.")
@click.option('--amt', default=None, type=int,
              help="Количество дикторов.")
def main(audio_path, amt):
    res = tooc_api.transcribition(audio_path, amt)
    print(res.json())


if __name__ == "__main__":
    main()