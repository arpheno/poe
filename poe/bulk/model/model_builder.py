from poe.bulk.model import feature_extraction_factory, Model


def model_builder(opt):
    fe = feature_extraction_factory(opt.FeatureExtraction, opt.input_channel, opt.output_channel)
    model = Model(opt, fe)
    return model
