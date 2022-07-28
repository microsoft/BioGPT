import argparse
from fairseq.models.transformer_lm import TransformerLanguageModel

parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", type=str, default="../../data/PubMed/data-bin")
parser.add_argument("--model_dir", type=str, default="../../checkpoints/Pre-trained-BioGPT")
parser.add_argument("--model_file", type=str, default="checkpoint.pt")
parser.add_argument("--bpecodes", type=str, default="../../data/bpecodes")
parser.add_argument("--beam", type=int, default=5)
parser.add_argument("--lenpen", type=float, default=1.0)
parser.add_argument("--min_len", type=int, default=100)
parser.add_argument("--lower", default=False, action="store_true")
args, _ = parser.parse_known_args()


def main(args):

    m = TransformerLanguageModel.from_pretrained(
        args.model_dir, 
        args.model_file, 
        args.data_dir, 
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes=args.bpecodes,
        min_len=args.min_len,
        max_len_b=1024,
        beam=args.beam,
        lenpen=args.lenpen,
        max_tokens=12000)

    print(m.cfg)
    if m.cfg.common.fp16:
        print('Converting to float 16')
        m.half()
    m.cuda()

    while True:
        print("Please input and press enter:")
        _src = input().strip()
        src_tokens = m.encode(_src)
        generate = m.generate([src_tokens], beam=args.beam)[0]
        output = m.decode(generate[0]["tokens"])
        print(output)
if __name__ == "__main__":
    main(args)