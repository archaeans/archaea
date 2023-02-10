import re
import sys


def patch(tag):
    print(f"Patching version: {tag}")

    with open("setup.py", "r") as f:
        lines = f.readlines()

        if "version" not in lines[2]:
            raise Exception("Invalid setup.py. Could not patch version.")

        lines[5] = f'\tversion="{tag}"\n'
        with open("setup.py", "w") as file:
            file.writelines(lines)


def main():
    if len(sys.argv) < 2:
        return

    tag = sys.argv[1]
    if not re.match(r"[0-9]+(\.[0-9]+)*$", tag):
        raise ValueError(f"Invalid tag provided: {tag}")

    patch(tag)


if __name__ == "__main__":
    main()
