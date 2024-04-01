""" Example handler file. """

import runpod
import transformers
import torch

# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.
tokenizer = transformers.NllbTokenizer.from_pretrained(
    "facebook/nllb-200-distilled-1.3B"
)
model = transformers.M2M100ForConditionalGeneration.from_pretrained(
    "jq/nllb-1.3B-many-to-many-step-2k"
)


def make_response(response):
    return {"data": response}


def translate(text, source_language, target_language):
    _language_codes = {
        "eng": 256047,
        "ach": 256111,
        "lgg": 256008,
        "lug": 256110,
        "nyn": 256002,
        "teo": 256006,
    }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    inputs = tokenizer(text, return_tensors="pt").to(device)
    inputs["input_ids"][0][0] = _language_codes[source_language]
    translated_tokens = model.to(device).generate(
        **inputs,
        forced_bos_token_id=_language_codes[target_language],
        max_length=100,
        num_beams=5,
    )

    result = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return result


def handler(job):
    """Handler function that will be used to process jobs."""
    job_input = job["input"]

    source_language = job_input.get("source_language")
    target_language = job_input.get("target_language")
    text_to_translate = job_input.get("text")

    translated_text = translate(text_to_translate, source_language, target_language)
    
    resp = {
        "text": text_to_translate,
        "translated_text": translated_text
    }

    return make_response(response=resp)


runpod.serverless.start({"handler": handler})
