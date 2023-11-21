
from transformers import DonutProcessor, VisionEncoderDecoderModel


def load_processor_and_model():
    # Load the processor and the model
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    return processor,model



