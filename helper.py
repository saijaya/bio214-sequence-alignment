def read_input_file(filename):
    data = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # strip comments and empty lines
    clean = []
    for line in lines:
        if ';' in line:
            line = line.split(';')[0]
        line = line.strip()
        if line:
            clean.append(line)
    
    # grab the data
    data['seq_a'] = clean[0]
    data['seq_b'] = clean[1]
    data['global_alignment'] = (int(clean[2]) == 0)
    
    # gap penalties
    gaps = clean[3].split()
    data['dx'] = float(gaps[0])
    data['ex'] = float(gaps[1])
    data['dy'] = float(gaps[2])
    data['ey'] = float(gaps[3])
    
    # alphabets
    data['len_alphabet_a'] = int(clean[4])
    data['alphabet_a'] = clean[5]
    data['len_alphabet_b'] = int(clean[6])
    data['alphabet_b'] = clean[7]
    
    # match matrix
    data['match_matrix_entries'] = []
    for i in range(8, len(clean)):
        parts = clean[i].split()
        if len(parts) == 5:
            data['match_matrix_entries'].append({
                'row': int(parts[0]),
                'col': int(parts[1]),
                'char_a': parts[2],
                'char_b': parts[3],
                'score': float(parts[4])
            })
    
    return data


def print_data(data):
    print("seq_a:", data['seq_a'])
    print("seq_b:", data['seq_b'])
    print("global:", data['global_alignment'])
    print("gaps:", data['dx'], data['ex'], data['dy'], data['ey'])
    print("alphabets:", data['alphabet_a'], data['alphabet_b'])
    print("matrix entries:", len(data['match_matrix_entries']))
    for entry in data['match_matrix_entries']:
        print(f"  {entry['char_a']} {entry['char_b']}: {entry['score']}")
