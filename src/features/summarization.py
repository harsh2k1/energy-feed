
def summary_generator(tokenizer, model, text):
    inputs = tokenizer.encode("summarize: " + text,
                          return_tensors='pt',
                          max_length=512,
                          truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)
    summary = tokenizer.decode(summary_ids[0])

    return summary.split(">",1)[-1].split(".<")[0].strip()