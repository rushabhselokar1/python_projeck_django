from web_application.utils.load_model import load_processor_and_model
import torch


# loading the processor and model from utils load models
processor,model = load_processor_and_model()

# Set up device
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def generate_result(user_question,_image):
    # Prepare the question prompt
    task_prompt = f"<s_docvqa><s_question>{user_question}</s_question><s_answer>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

    # Generate answer
    outputs = model.generate(
        processor(_image, return_tensors="pt").pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
        output_scores=True,
    )

    # Decode and display the answer
    seq = processor.batch_decode(outputs.sequences)[0]
    answer = seq.split("<s_answer>")[-1].strip("</s_answer>")
    return answer
