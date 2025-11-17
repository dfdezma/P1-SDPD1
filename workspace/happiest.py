import glob

state_happiness = {}

for filename in glob.glob("results/part-000*"):
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().replace('"', '')
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 2:
                continue
            state, value = parts
            try:
                value = float(value)
            except ValueError:
                continue
            state_happiness[state] = value

if state_happiness:
    best_state = max(state_happiness.items(), key=lambda x: x[1])
    print("Estado mas feliz:", best_state[0], "con felicidad media de cada tweet de:", best_state[1])
else:
    print("No se encontraron datos validos")
