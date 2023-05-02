from flask import Flask, request, jsonify
from fairseq.models.transformer_lm import TransformerLanguageModel


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    min_len = request.args.get("min_len", 100)
    max_len_b = request.args.get("max_len_b", 1024)
    beam = request.args.get("beam", 5)
    text = request.args["text"]

    model = TransformerLanguageModel.from_pretrained(
        "checkpoints/Pre-trained-BioGPT",
        "checkpoint.pt",
        "data",
        tokenizer="moses",
        bpe="fastbpe",
        bpe_codes="data/bpecodes",
        min_len=min_len,
        max_len_b=max_len_b,
    )
    model.cuda()
    src_tokens = model.encode(text)
    generate = model.generate([src_tokens], beam=beam)[0]
    outputs = model.decode(generate[0]["tokens"])
    return jsonify(outputs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
