from pathlib import Path


def read_file(path):

    try:

        content = Path(path).read_text(
            encoding="utf-8"
        )

        return content[:8000]

    except Exception as e:

        return f"File read error: {e}"



def list_directory(path="."):

    try:

        files = []

        for p in Path(path).iterdir():

            files.append(
                str(p)
            )

        return files


    except Exception as e:

        return f"Errore directory: {e}"