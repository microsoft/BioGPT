# coding: utf-8
import re
import json
import sys
import os

pred_file = sys.argv[1]
gold_file = sys.argv[2]
pmids_file = sys.argv[3]

def normalize_name(s: str):
    s = s.strip()

    # normalize roman type id at end of string
    num2roman = {"0": "0", "1": "I", "2": "II", "3": "III", "4": "IV", "5": "V", "6": "VI", "7": "VII", "8": "VIII", "9": "IX"}
    if len(s) > 2 and s[-1].isnumeric() and not s[-2].isnumeric() and s[-1] in num2roman:
        tmps = list(s)
        s = ''.join(tmps[:-1]) + num2roman[tmps[-1]]

    # remove useless end string
    s = s.replace("-type", '')

    return re.sub('[^a-zA-Z0-9]+', '', s)


def rm_abbr(tgt_set):
    """ remove abbreviation in the brackets of entity, eg: aaa (bb) -> aaa """
    def rm(s):
        s = s.strip()
        if "(" in s and s[-1] == ')':  # entity end with a bracketed short cut
            return normalize_name(s[:s.rfind("(")].strip())
        else:
            return normalize_name(s)

    tgt_set = list(tgt_set)
    if tgt_set and type(tgt_set[0]) in [tuple, list]:  # process triples
        return set([(rm(tp[0]), rm(tp[1]), rm(tp[2])) for tp in tgt_set])
    else:  # process entities
        return set([rm(e) for e in tgt_set])


def get_abbr(tgt_set):
    """ extract abbreviation in the brackets of entity, eg: aaa (bb) -> bb """
    def rm(s):
        s = s.strip()
        if "(" in s and s[-1] == ')':
            return normalize_name(s[s.rfind("(")+1:-1].strip())
        else:
            return normalize_name(s)

    tgt_set = list(tgt_set)
    if tgt_set and type(tgt_set[0]) in [tuple, list]:  # process triples
        return set([(rm(tp[0]), rm(tp[1]), rm(tp[2])) for tp in tgt_set])
    else:  # process entities
        return set([rm(e) for e in tgt_set])


def acc(pred_set, gold_set):
    """ Multi-label style acc """
    tp_num = len(pred_set & gold_set)
    return int(pred_set == gold_set) if len(gold_set) == 0 else 1.0 * tp_num / len(pred_set | gold_set)


def precision(pred_set, gold_set):
    """ Multi-label style precision """
    tp_num = len(pred_set & gold_set)
    return int(pred_set == gold_set) if len(pred_set) == 0 else 1.0 * tp_num / len(pred_set)


def recall(pred_set, gold_set):
    """ Multi-label style recall """
    tp_num = len(pred_set & gold_set)
    return int(pred_set == gold_set) if len(gold_set) == 0 else 1.0 * tp_num / len(gold_set)


def normed_eval(pred_set, gold_set, metric):
    """ Both body and abbreviation match are considered correct """
    abbr_pred_set, abbr_gold_set = get_abbr(pred_set), get_abbr(gold_set)
    rm_pred_set, rm_gold_set = rm_abbr(pred_set), rm_abbr(gold_set)
    return max(metric(abbr_pred_set, abbr_gold_set), metric(rm_pred_set, rm_gold_set))


def get_f1(p, r):
    return 0 if (p + r) == 0 else (2.0 * p * r / (p + r))


def ave(scores):
    return 1.0 * sum(scores) / len(scores)


def do_eval(preds, pmids, golden):
    ret = []
    num_pred, num_gold, num_missing = 0, 0, 0
    all_f1, p, r, d_acc, t_acc, i_acc = [], [], [], [], [], []
    all_pred_triple, all_pred_d, all_pred_t, all_pred_i, all_gold_triple, all_gold_d, all_gold_t, all_gold_i = [], [], [], [], [], [], [], [],

    for pred, idx in zip(preds, pmids):
        gold_d_set, gold_t_set, gold_i_set, gold_set = set(), set(), set(), set()
        pred_d_set, pred_t_set, pred_i_set, pred_set = set(), set(), set(), set()
        
        if pred["triple_list_pred"] and pred["triple_list_pred"][0]["subject"] != 'failed':
            for tp in pred["triple_list_pred"]:
                d = tp["subject"].strip().lower().replace(' ', '')
                t = tp["object"].strip().lower().replace(' ', '')
                i = tp["relation"].strip().lower().replace(' ', '')

                pred_d_set.add(d)
                pred_t_set.add(t)
                pred_i_set.add(i)
                pred_set.add((d, t, i))
        if idx not in golden:
            num_missing += 1
            # print("----Missing:", idx)
            continue
        if golden[idx]["triples"]:
            for tp in golden[idx]["triples"]:
                d = tp["drug"].strip().lower().replace(' ', '')
                t = tp["target"].strip().lower().replace(' ', '')
                i = tp["interaction"].strip().lower().replace(' ', '')
                gold_d_set.add(d)
                gold_t_set.add(t)
                gold_i_set.add(i)
                gold_set.add((d, t, i))

        # sample level eval
        p.append(normed_eval(pred_set, gold_set, metric=precision))
        r.append(normed_eval(pred_set, gold_set, metric=recall))
        all_f1.append(get_f1(p[-1], r[-1]))
        d_acc.append(normed_eval(pred_d_set, gold_d_set, metric=acc))
        t_acc.append(normed_eval(pred_t_set, gold_t_set, metric=acc))
        i_acc.append(normed_eval(pred_i_set, gold_i_set, metric=acc))

        # onto level eval
        all_pred_d.extend(pred_d_set)
        all_pred_t.extend(pred_t_set)
        all_pred_i.extend(pred_i_set)
        all_pred_triple.extend(pred_set)
        all_gold_d.extend(gold_d_set)
        all_gold_t.extend(gold_t_set)
        all_gold_i.extend(gold_i_set)
        all_gold_triple.extend(gold_set)
        
        # if len(gold_set) < len(golden[idx]["triples"]):
            # print("Duplicate extists, ori", golden[idx]["triples"], gold_set)

        num_pred += len(pred_set)
        num_gold += len(gold_set)

        ret.append({
            "pmid": idx,
            "title": golden[idx]["title"] if "title" in golden[idx] else None,
            "abstract": golden[idx]["abstract"],
            "d_pred_gold": [d_acc[-1], list(pred_d_set), list(gold_d_set)],
            "t_pred_gold": [t_acc[-1], list(pred_t_set), list(gold_t_set)],
            "i_pred_gold": [i_acc[-1], list(pred_i_set), list(gold_i_set)],
            "all_pred_gold": [all_f1[-1], list(pred_set), list(gold_set)],
        })


    print("num sample", len(all_f1), "missing", len(preds) - len(all_f1), "num_gold tp", num_gold, "num_pred", num_pred)

    # Note: we adopt multi-label metrics following: http://129.211.169.156/publication/tkde13rev.pdf
    print("Sample: acc d: {:.4f}\tt:{:.4f}\ti: {:.4f}\ntp p: {:.4f}\ttp r: {:.4f}\ttp micro f1: {:.4f}\ttp macro f1: {:.4f} ".format(
        ave(d_acc), ave(t_acc), ave(i_acc), ave(p), ave(r), ave(all_f1), get_f1(ave(p), ave(r))))

    # Ontology evaluation_scripts
    all_p, all_r = normed_eval(set(all_pred_triple), set(all_gold_triple), metric=precision), normed_eval(set(all_pred_triple), set(all_gold_triple), metric=recall)
    d_p, d_r = normed_eval(set(all_pred_d), set(all_gold_d), metric=precision), normed_eval(set(all_pred_d), set(all_gold_d), metric=recall)
    t_p, t_r = normed_eval(set(all_pred_t), set(all_gold_t), metric=precision), normed_eval(set(all_pred_t), set(all_gold_t), metric=recall)
    i_p, i_r = normed_eval(set(all_pred_i), set(all_gold_i), metric=precision), normed_eval(set(all_pred_i), set(all_gold_i), metric=recall)

    print("Ontology: f1 d: {:.4f}\tt:{:.4f}\ti: {:.4f}\t \nall p: {:.4f}\tall r: {:.4f}\tonto f1: {:.4f}".format(
        get_f1(d_p, d_r), get_f1(t_p, t_r), get_f1(i_p, i_r), all_p, all_r, get_f1(all_p, all_r)
    ))
    return ret


def main():
    preds = []
    with open(pred_file) as reader:
        for line in reader:
            preds.append(json.loads(line))

    with open(gold_file) as reader:
        golden = json.load(reader)

    with open(pmids_file) as reader:
        if '.json' in pmids_file:
            pmids = json.load(reader)
        else:
            pmids = []
            for line in reader:
                pmids.append(line.strip())

    print("\n====File: ", os.path.basename(pred_file))
    result = do_eval(preds, pmids, golden)

    last_pos = pred_file.rfind('.json')
    res_file_name = pred_file[:last_pos] + '.eval_res.json'
    with open(res_file_name, 'w') as writer:
        json.dump(result, writer, indent=2)


if __name__ == "__main__":
    main()
