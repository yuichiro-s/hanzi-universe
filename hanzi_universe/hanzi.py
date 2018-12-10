from collections import defaultdict

from hanzi_universe.loader import load_cedict, load_frequency, load_frequency_char, load_ids
from hanzi_universe.pinyin import decode_pinyin

word_freqs = load_frequency('data/frequency')
ranks = load_frequency_char('data/frequency_char')
cedict, pron_to_hanzi, traditional_to_simple, simple_to_traditional, hanzi_to_words = load_cedict(
    'data/cedict_ts.u8', word_freqs)
hanzi_to_parts, part_to_hanzi = load_ids('data/cjkvi-ids/ids.txt', cedict)

INF = float('inf')

def zip_with_frequency(words, f, reverse=False):
    return sorted(
        map(lambda w: (w, f[w]), words), key=lambda kv: kv[1] or INF, reverse=reverse)


def list_hanzi_with_pronuncitation(pron, max_rank):
    hanzi = pron_to_hanzi[pron]
    results = []
    for w, rank in zip_with_frequency(hanzi, ranks):
        if rank and rank <= max_rank:
            results.append((w, rank))
    return results


def exclude(hanzi_list, hanzi):
    res = []
    for h, r in hanzi_list:
        if h != hanzi:
            res.append((h, r))
    return res


def get_words(hanzi, pron):
    a = []
    for w, p, d in hanzi_to_words[(hanzi, pron)]:
        f = word_freqs[w]
        if f >= 5:
            a.append((-f, w, p, d))
    a.sort()

    res = []
    for _, word, pron, defs in a:
        chars = []
        for c in word:
            rank = ranks.get(c, None)
            chars.append((c, rank))
        res.append((chars, pron, defs))
    return res


def normalize(pron):
    pron = pron.replace('q', 'j')
    pron = pron.replace('c', 'z')
    pron = pron.replace('k', 'g')
    pron = pron.replace('t', 'd')
    pron = pron.replace('p', 'b')
    return pron


def get_related_hanzi(hanzi, pron, max_rank):
    s = part_to_hanzi[hanzi]
    if hanzi in hanzi_to_parts:
        parts = hanzi_to_parts[hanzi]
        for part in parts:
            s = s.union(part_to_hanzi[part])
            s.add(part)
    if hanzi in s:
        s.remove(hanzi)

    level1 = []
    level2 = defaultdict(list)
    for hanzi2 in s:
        for pron2, _ in cedict[hanzi2]:
            pron2 = pron2[0]
            rank2 = ranks[hanzi2]
            if rank2 and rank2 <= max_rank:
                if pron == pron2:
                    level1.append((hanzi2, rank2))
                elif normalize(pron[:-1]) == normalize(pron2[:-1]):
                    level2[pron2].append((hanzi2, rank2))

    level1.sort(key=lambda e: e[1] or INF)
 
    level2_list = []
    for pron2, hs in sorted(level2.items()):
        level2_list.append((pron2, sorted(hs, key=lambda e: e[1] or INF)))

    return level1, level2_list


def lookup(hanzi, max_rank):
    rank = ranks[hanzi]

    entries = []
    for pron, defs in cedict[hanzi]:
        pron = pron[0]
        same = exclude(list_hanzi_with_pronuncitation(pron, max_rank), hanzi)
        l1, l2 = get_related_hanzi(hanzi, pron, max_rank)
        words = get_words(hanzi, pron)
        entries.append({
            'pron': pron,
            'defs': defs,
            'same': same,
            'related1': l1,
            'related2': l2,
            'words': words,
        })

    return {
        'hanzi':
        hanzi,
        'rank':
        rank,
        'entries':
        entries,
        'traditional':
        simple_to_traditional[hanzi]
        if hanzi in simple_to_traditional else None,
    }


def lookup_pinyin(pinyin, max_rank):
    tones = []
    for tone in range(1, 5):
        p = pinyin + str(tone)
        p_str = decode_pinyin(p)
        chars = []
        for c, rank in list_hanzi_with_pronuncitation(p, max_rank):
            chars.append((c, rank, get_category(rank)))
        tones.append({
            'pinyin': p_str,
            'chars': chars,
        })

    result = {
        'pinyin': pinyin,
        'tones': tones,
    }

    return result


def get_category(rank):
    if isinstance(rank, int):
        n = (rank - 1) // 500
        if n == 0:
            return 'SSS'
        elif n == 1:
            return 'SS'
        elif n == 2:
            return 'S'
        elif n == 3:
            return 'A'
        elif n == 4:
            return 'B'
        elif n == 5:
            return 'C'
        else:
            return 'D'
    else:
        return 'D'
