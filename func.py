# coding=utf-8
def match_site(site, sequence):
    start_at = -1
    positions = []
    while True:
        try:
            loc = sequence.index(site, start_at + 1)
        except ValueError:
            break
        else:
            positions.append(loc)
            start_at = loc
    return positions


def dna_to_rna(sequence):
    dict_rna = {
        'A': 'U',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }
    m_rna = ''
    for i in sequence:
        m_rna += dict_rna[i]
    return m_rna


def rna_to_pro(sequence, starts=0):
    dict_pro = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': 'END', 'UAG': 'END',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'UGU': 'C', 'UGC': 'C', 'UGA': 'END', 'UGG': 'W',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    pro_sequence = ''
    if starts < 0:
        sequence = sequence[::-1][abs(starts) - 1:]
    else:
        sequence = sequence[starts:]
    for i in range(0, len(sequence), 3):
        password = dict_pro.get(sequence[i:i+3], None)
        if not password or password == 'END':
            return pro_sequence
        pro_sequence += dict_pro[sequence[i:i+3]]
    return pro_sequence


if __name__ == '__main__':
    data = dna_to_rna('CGCGGAAAGGCTAACGGGAGGCAAAGAGACTTTATACCCAGAGATTTACCCCAGAAACCGGGAGATTTT')
    print 'mRNA:', data
    print rna_to_pro(data)
    print rna_to_pro(data, 1)
    print rna_to_pro(data, 2)
