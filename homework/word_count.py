import glob
import os
import os.path
import string


def copy_raw_files_to_input_folder(n=1000):
    """
    Copia n veces los archivos de files/raw a files/input
    """

    if os.path.exists("files/input"):
        for file in glob.glob("files/input/*"):
            if os.path.isfile(file):
                os.remove(file)
    else:
        os.makedirs("files/input")

    for file in glob.glob("files/raw/*"):

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        raw_filename_with_extension = os.path.basename(file)
        raw_filename_without_extension = os.path.splitext(
            raw_filename_with_extension
        )[0]

        for i in range(1, n + 1):
            new_filename = (
                f"files/input/{raw_filename_without_extension}_{i}.txt"
            )

            with open(new_filename, "w", encoding="utf-8") as f2:
                f2.write(text)


def run_job(input_path, output_path):
    """
    Ejecuta Word Count
    """

    # Leer archivos
    sequence = []

    files = glob.glob(f"{input_path}/*")

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                sequence.append((file, line))

    # Mapper
    pairs_sequence = []

    for _, line in sequence:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        line = line.replace("\n", "")
        words = line.split()

        for word in words:
            pairs_sequence.append((word, 1))

    # Shuffle and Sort
    pairs_sequence = sorted(pairs_sequence)

    # Reducer
    result = []

    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))

    # Crear output
    if os.path.exists(output_path):
        for file in glob.glob(f"{output_path}/*"):
            if os.path.isfile(file):
                os.remove(file)
    else:
        os.makedirs(output_path)

    # Guardar resultado
    with open(
        f"{output_path}/part-00000",
        "w",
        encoding="utf-8",
    ) as f:
        for key, value in result:
            f.write(f"{key}\t{value}\n")

    # Archivo success
    with open(
        f"{output_path}/_SUCCESS",
        "w",
        encoding="utf-8",
    ) as f:
        f.write("")