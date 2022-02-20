import os.path


def write_to_file(filename: str, text: str) -> None:
    os.chdir("..")
    dirname = os.path.abspath(os.curdir)
    save_path = "/output/"
    complete_name = os.path.join(dirname + save_path, filename + ".tex")
    file = open(complete_name, "w", encoding="utf-8")
    file.write(text)
    file.close()
