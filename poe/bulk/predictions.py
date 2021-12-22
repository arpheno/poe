import time
from argparse import Namespace

import cv2
import torch
from easyocr.utils import CTCLabelConverter

from poe.bulk.model import Model
from poe.bulk.model.model_builder import model_builder

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def predict(model, image_tensors, opt):
    """ validation or evaluation """
    converter = CTCLabelConverter('0123456789.')
    batch_size = image_tensors.size(0)
    image = image_tensors.to(device)
    text_for_pred = torch.LongTensor(batch_size, opt.batch_max_length + 1).fill_(0).to(device)

    preds = model(image, text_for_pred)

    # Calculate evaluation loss for CTC deocder.
    preds_size = torch.IntTensor([preds.size(1)] * batch_size)

    # Select max probabilty (greedy decoding) then decode index to character
    _, preds_index = preds.max(2)
    preds_str = converter.decode(preds_index.data, preds_size.data)



    return preds_str


def predict_wrapper(gray):
    global opt
    opt = dict(
        workers=4,
        batch_size=192,
        num_iter=300000,
        valInterval=2000,
        lr=1,
        beta1=0.9,
        rho=0.95,
        eps=1e-8,
        grad_clip=5,
        select_data='MJ-ST',
        batch_ratio=0.5 - 0.5,
        total_data_usage_ratio=1.0,
        batch_max_length=25,
        imgH=32,
        imgW=80,
        character='0123456789. ',
        num_fiducial=20,
        input_channel=1,
        output_channel=512,
        hidden_size=256,
        Transformation='None',
        FeatureExtraction='VGG',
        SequenceModeling='BiLSTM',
        Prediction='CTC',
        saved_model='/Users/swozny/.EasyOcr/model/32801.pth'
    )
    opt = Namespace(**opt)
    opt.num_class = len(opt.character)
    model = model_builder(opt)
    model = torch.nn.DataParallel(model).to(device)
    model.load_state_dict(torch.load(opt.saved_model, map_location=device))
    my_img_tensor = torch.from_numpy(gray)
    img_tensor = my_img_tensor[None, None, :].float().div(255).sub(0.5).div(0.5)
    result = predict(model, image_tensors=img_tensor, opt=opt)
    return result

if __name__ == '__main__':

    img=cv2.imread('data/handlabeling/4ef3b6dd3f/11_2.png')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    result = predict_wrapper(gray)
    print(result)