import os

star_in = "/path/to/input.star" #original .star file containing full list
star_out = "particles_subset.star"    # subset output
mrcs_dir = "/path/to/mrcs/directory/"

available = set(os.listdir(mrcs_dir))

with open(star_in) as f:
    lines = f.readlines()

out = []
state = "other"
columns = []
img_col = None
kept = dropped = 0

for line in lines:
    s = line.strip()

    if s == "loop_":
        columns = []
        state = "header"
        out.append(line)
        continue

    if state == "header":
        if s.startswith("_"):
            columns.append(s.split()[0])
            out.append(line)
            continue
        state = "data"
        img_col = columns.index("_rlnImageName") if "_rlnImageName" in columns else None

    if state == "data" and img_col is not None:
        if s == "" or s.startswith("data_"):
            state = "other"
        else:
            stack = s.split()[img_col].split("@")[-1]
            if os.path.basename(stack) in available:
                out.append(line)
                kept += 1
            else:
                dropped += 1
            continue

    out.append(line)

with open(star_out, "w") as f:
    f.writelines(out)

print(f"Kept {kept} particles, dropped {dropped}")