from poe.bulk.model.modules.feature_extraction.VGG import VGG_FeatureExtractor
from poe.bulk.model.modules.feature_extraction.rcnn import RCNN_FeatureExtractor


def feature_extraction_factory(
    feature_extraction_type: str, input_channel: int, output_channel: int
):
    cls = {"VGG": VGG_FeatureExtractor, "RCNN": RCNN_FeatureExtractor}
    return cls[feature_extraction_type](input_channel, output_channel)
