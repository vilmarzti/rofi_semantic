from neural_compressor.config import PostTrainingQuantConfig
from optimum.intel import INCQuantizer, INCModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
from transformers import AutoModel


def load_model(model_name):
    return INCModelForSeq2SeqLM.from_pretrained(model_name)


def quantize(model_url, save_dir):
    model = AutoModel.from_pretrained(model_url)
    quantization_config = PostTrainingQuantConfig(approach='dynamic')
    quantizer = INCQuantizer.from_pretrained(model)
    quantizer.quantize(quantization_config=quantization_config, save_directory=save_dir)
