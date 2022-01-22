from argparse import Namespace

import cv2
import torch

from poe.bulk.model.model_builder import model_builder
from poe.bulk.model.modules.converters import AttnLabelConverter

model=None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def predict(model,converter, image_tensors, opt):
    """ validation or evaluation """
    batch_size = image_tensors.size(0)
    image = image_tensors.to(device)
    length_for_pred = torch.IntTensor([opt.batch_max_length] * batch_size).to(device)
    text_for_pred = torch.LongTensor(batch_size, opt.batch_max_length + 1).fill_(0).to(device)
    preds = model(image, text_for_pred)


    # Calculate evaluation loss for CTC deocder.
    preds_size = torch.IntTensor([preds.size(1)] * batch_size)

    # Select max probabilty (greedy decoding) then decode index to character
    _, preds_index = preds.max(2)
    # preds_str = converter.decode(preds_index, preds_size.data)
    preds = ''.join(converter.decode(preds_index, length_for_pred))
    pred_EOS = preds.find('[s]')
    preds_str = preds[:pred_EOS]  # prun



    return preds_str


def predict_wrapper(gray,model_params={}):
    model_params = dict(
        batch_max_length=8,
        imgH=32,
        imgW=80,
        character='0123456789.',
        input_channel=1,
        output_channel=512,
        hidden_size=256,
        Transformation='None',
        FeatureExtraction='RCNN',
        SequenceModeling='BiLSTM',
        Prediction='Attn',
        saved_model='rcnn.pth'
    )
    model_params = Namespace(**model_params)

    converter = AttnLabelConverter(model_params.character)
    model_params.num_class = len(converter.character)
    global model
    if not model:
        model = model_builder(model_params)

    my_img_tensor = torch.from_numpy(gray)
    img_tensor = my_img_tensor[None, None, :].float().div(255).sub(0.5).div(0.5)
    with torch.no_grad():
        result = predict(model,converter, image_tensors=img_tensor, opt=model_params)
    return result

if __name__ == '__main__':
    tests={
        '61.2':'data/handlabeling/4ef3b6dd3f/11_2.png',
        '0.02':'data/handlabeling/4ef3b6dd3f/13_8.png',
        '1':'data/handlabeling/4ef3b6dd3f/19_10.png',
        '165.1':'data/handlabeling/fe4ffabf2c/11_7.png',
        '26.6':'data/handlabeling/82659fc57c/11_11.png',
        '2.01':'data/handlabeling/9c0256e2ef/13_0.png',
        '223.36': 'data/handlabeling/fe4ffabf2c/11_5.png',
        '120':'data/handlabeling/e2d5e1294b/24_1.png',
    }
    for label,path in tests.items():
        img=cv2.imread(path)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        result = predict_wrapper(gray)
        print(result,label)