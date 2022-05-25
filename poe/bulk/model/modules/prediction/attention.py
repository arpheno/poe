import torch
from torch import nn as nn
from torch.nn import functional as F

from poe.bulk.model.modules.prediction.interface import Predictor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Attention(Predictor):
    def __init__(self, input_size, hidden_size, num_classes, batch_max_length):
        super(Attention, self).__init__()
        self.attention_cell = AttentionCell(input_size, hidden_size, num_classes)
        self.hidden_size = hidden_size
        self.num_classes = num_classes
        self.generator = nn.Linear(hidden_size, num_classes)
        self.batch_max_length = batch_max_length

    def _char_to_onehot(self, input_char, onehot_dim=38):
        input_char = input_char.unsqueeze(1)
        batch_size = input_char.size(0)
        one_hot = torch.FloatTensor(batch_size, onehot_dim).zero_().to(device)
        one_hot = one_hot.scatter_(1, input_char, 1)
        return one_hot

    def forward(self, batch_H):
        """
        input:
            batch_H : contextual_feature H = hidden state of encoder. [batch_size x num_steps x contextual_feature_channels]
            text : the text-index of each image. [batch_size x (max_length+1)]. +1 for [GO] token. text[:, 0] = [GO].
        output: probability distribution at each step [batch_size x num_steps x num_classes]
        """
        batch_size = batch_H.size(0)
        num_steps = self.batch_max_length + 1  # +1 for [s] at end of sentence.

        hidden = (
            torch.FloatTensor(batch_size, self.hidden_size).fill_(0).to(device),
            torch.FloatTensor(batch_size, self.hidden_size).fill_(0).to(device),
        )

        targets = torch.LongTensor(batch_size).fill_(0).to(device)  # [GO] token
        probs = (
            torch.FloatTensor(batch_size, num_steps, self.num_classes)
            .fill_(0)
            .to(device)
        )

        for i in range(num_steps):
            char_onehots = self._char_to_onehot(targets, onehot_dim=self.num_classes)
            hidden, alpha = self.attention_cell(hidden, batch_H, char_onehots)
            probs_step = self.generator(hidden[0])
            probs[:, i, :] = probs_step
            _, next_input = probs_step.max(1)
            targets = next_input

        return probs  # batch_size x num_steps x num_classes


class AttentionCell(Predictor):
    def __init__(self, input_size, hidden_size, num_embeddings):
        super(AttentionCell, self).__init__()
        self.i2h = nn.Linear(input_size, hidden_size, bias=False)
        self.h2h = nn.Linear(
            hidden_size, hidden_size
        )  # either i2i or h2h should have bias
        self.score = nn.Linear(hidden_size, 1, bias=False)
        self.rnn = nn.LSTMCell(input_size + num_embeddings, hidden_size)
        self.hidden_size = hidden_size

    def forward(self, prev_hidden, batch_H, char_onehots):
        # [batch_size x num_encoder_step x num_channel] -> [batch_size x num_encoder_step x hidden_size]
        batch_H_proj = self.i2h(batch_H)
        prev_hidden_proj = self.h2h(prev_hidden[0]).unsqueeze(1)
        e = self.score(
            torch.tanh(batch_H_proj + prev_hidden_proj)
        )  # batch_size x num_encoder_step * 1

        alpha = F.softmax(e, dim=1)
        context = torch.bmm(alpha.permute(0, 2, 1), batch_H).squeeze(
            1
        )  # batch_size x num_channel
        concat_context = torch.cat(
            [context, char_onehots], 1
        )  # batch_size x (num_channel + num_embedding)
        cur_hidden = self.rnn(concat_context, prev_hidden)
        return cur_hidden, alpha
