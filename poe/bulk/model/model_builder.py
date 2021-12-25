from pathlib import Path

import torch

from poe.bulk.model.model import Model
from poe.bulk.model.modules.feature_extraction.factory import feature_extraction_factory
from poe.bulk.model.modules.prediction.factory import prediction_factory


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def model_builder(opt):
    predictor = prediction_factory(opt.Prediction, opt.output_channel, opt.hidden_size, opt.num_class,opt.batch_max_length)
    fe = feature_extraction_factory(opt.FeatureExtraction, opt.input_channel, opt.output_channel)
    model = Model(opt, fe, predictor=predictor)
    model = torch.nn.DataParallel(model).to(device)
    model.load_state_dict(torch.load(f'{Path(__file__).resolve().parent}/{opt.saved_model}', map_location=device))
    model.eval()
    return model
