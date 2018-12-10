from collections import defaultdict

BLACKLIST = {
    '艹',

    '氵',
    '扌',
    '亻',
    '讠',

    '辶',
    '疒',
    '厂',
    '尸',

    '冖',
    '宀',
    '一',
    '亠',
    '丷',

    '丨',
    '凵',
    '丿',

    '竹',
    '十',
}


def load_cedict(path, word_freqs):
    cedict = defaultdict(list)
    pron_to_hanzi = defaultdict(set)
    traditional_to_simple = {}
    simple_to_traditional = {}
    hanzi_to_words = defaultdict(set)
    with open(path) as f:
        for line in f:
            es = line.strip().split(' ', 2)
            if not line.startswith('#') and len(es) == 3:
                traditional, simplified, es = es
                traditional_to_simple[traditional] = simplified
                simple_to_traditional[simplified] = traditional
                hanzi = simplified
                i = es.find(']')
                pron = es[1:i].lower().split()
                defs = es[i + 3:-1].split('/')
                defs = list(filter(lambda d: 'CL' not in d, defs))
                for i, (pron2, defs2) in enumerate(cedict[hanzi]):
                    # check for duplicate
                    if pron2 == pron:
                        new_entry = (pron, defs2 + defs)
                        cedict[hanzi][i] = new_entry
                        break
                else:
                    entry = (pron, defs)
                    cedict[hanzi].append(entry)
                if len(pron) == 1:
                    # hanzi
                    pron_to_hanzi[pron[0]].add(hanzi)
                if len(hanzi) >= 2:
                    for c, p in zip(hanzi, pron):
                        hanzi_to_words[(c, p)].add((hanzi, tuple(pron),
                                                    tuple(defs)))

    # sort character pronuncitaions by frequency
    for char, entries in cedict.items():

        def get_pron_frequency(entry):
            pron, defs = entry
            n = 0
            pron = pron[0]
            for word, _, _ in hanzi_to_words[(char, pron)]:
                n += word_freqs[word]
            return n

        entries.sort(key=get_pron_frequency, reverse=True)

    return cedict, pron_to_hanzi, traditional_to_simple, simple_to_traditional, hanzi_to_words


def load_ids(path, cedict):
    hanzi_to_parts = {}
    part_to_hanzi = defaultdict(set)
    with open(path) as f:
        for line in f:
            es = line.strip().split('\t')
            if len(es) >= 3:
                _, hanzi, decomposition = es[:3]
                i = decomposition.find('[')
                if i >= 0:
                    decomposition = decomposition[:i]
                decomposition = decomposition.strip()
                hanzi_to_parts[hanzi] = decomposition
                for part in decomposition:
                    if part in cedict and part not in BLACKLIST:
                        part_to_hanzi[part].add(hanzi)
    return hanzi_to_parts, part_to_hanzi


def load_frequency(path):
    word_freqs = defaultdict(int)
    with open(path) as f:
        for line in f:
            word, freq = line.split()
            freq = int(freq)
            word_freqs[word] = freq
    return word_freqs


def load_frequency_char(path):
    ranks = defaultdict(lambda: None)
    with open(path) as f:
        for i, line in enumerate(f):
            rank = i + 1
            c = line.strip()
            ranks[c] = rank
    return ranks
