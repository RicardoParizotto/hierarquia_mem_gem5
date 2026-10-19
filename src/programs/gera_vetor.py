import random

values = [int(random.uniform(0, 100000)) for i in range(1, 1000000)]

with open("vetor.c", "w") as f:
    f.write("#include <stddef.h>\n\n")
    f.write(f"int vetor[] = {{\n    ")
    for i, v in enumerate(values):
        f.write(f"{v},")
        if (i + 1) % 20 == 0:
            f.write("\n    ")
    f.write("\n};\n\n")
    f.write(f"const size_t vetor_len = {len(values)};\n")

print(f"vetor.c gerado com {len(values)} elementos.")
