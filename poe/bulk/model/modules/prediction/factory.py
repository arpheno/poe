from torch import nn

from poe.bulk.model.modules.prediction.attention import Attention


def prediction_factory(
    predictor_type: str, input_size, hidden_size, num_classes, batch_max_length
):

    if predictor_type == "CTC":
        predictor = nn.Linear(hidden_size, num_classes)
    elif predictor_type == "Attn":
        predictor = Attention(hidden_size, hidden_size, num_classes, batch_max_length)
    else:
        raise Exception("Prediction is neither CTC or Attn")

    return predictor
