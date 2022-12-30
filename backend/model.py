import torch
import torch.nn as nn
import numpy as np
from torchvision.models import resnet34

# ResNet-34 CNN Encoder
class Encoder(nn.Module):
    def __init__(self, output_dim=14):
        super().__init__()
        resnet = resnet34(pretrained=True)
        layers = list(resnet.children())[:-2]
        self.resnet = nn.Sequential(*layers)
        # adaptive pool layer so encoder can take images of different sizes
        self.resize = nn.AdaptiveAvgPool2d((output_dim, output_dim))

        self.fine_tune()

    def forward(self, x):
        x = self.resnet(x)
        x = self.resize(x)
        x = x.permute(0, 2, 3, 1)
        return x

    # disable learning up to first three res blocks
    def fine_tune(self):
        for l in list(self.resnet.children())[:5]:
            for p in l.parameters():
                p.requires_grad = False

# Soft-Attention Network
class Attention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim, attention_dim):
        super().__init__()
        # [b_size, image_size, encoder_dim]
        self.encoder_att = nn.Linear(encoder_dim, attention_dim)
        # [b_size, decoder_dim]
        self.decoder_att = nn.Linear(decoder_dim, attention_dim)
        self.att = nn.Linear(attention_dim, 1)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    # takes in features from encoder and hidden layer from decoder
    def forward(self, features, hidden):
        att_features = self.encoder_att(features)
        att_hidden = self.decoder_att(hidden)
        att_cat = self.relu(att_features + att_hidden.unsqueeze(1))
        alpha_logits = self.att(att_cat).squeeze(2)
        # [b_size, image_size]
        alpha = self.softmax(alpha_logits)
        # weighted values for each pixel in feature map
        features_weighted = (features * alpha.unsqueeze(2)).sum(dim=1)

        return features_weighted, alpha


class Decoder(nn.Module):
    def __init__(self, decoder_dim, attention_dim, num_tokens, embed_size, device, encoder_dim=512):
        super().__init__()
        self.encoder_dim = encoder_dim
        self.decoder_dim = decoder_dim
        self.attention_dim = attention_dim
        self.num_tokens = num_tokens
        self.device = device

        self.attention = Attention(encoder_dim, decoder_dim, attention_dim)

        self.init_h0 = nn.Linear(encoder_dim, decoder_dim)
        self.init_c0 = nn.Linear(encoder_dim, decoder_dim)

        self.embedding = nn.Embedding(num_tokens, embed_size)
        self.lstm = nn.LSTMCell(embed_size + encoder_dim, decoder_dim)
        self.dropout = nn.Dropout(p=0.4)
        self.f_beta = nn.Linear(decoder_dim, encoder_dim)
        self.sigmoid = nn.Sigmoid()
        self.fc = nn.Linear(decoder_dim, num_tokens)
        
    def initialize(self, features):
        # [b_size, image_size, encoder_dim]
        features = features.mean(dim=1)
        h0 = self.init_h0(features)
        c0 = self.init_c0(features)
        
        return h0, c0

    # captions: [b_size, max_length]
    def forward(self, features, captions, caption_lengths):
        batch_size = features.shape[0]

        # [b_size, image_size, encoder_dim]
        features = features.reshape(batch_size, -1, self.encoder_dim)

        # sort captions and features in descending order by caption length
        caption_lengths, sort_indices = caption_lengths.sort(descending=True)
        captions = captions[sort_indices]
        features = features[sort_indices]

        h, c = self.initialize(features)
        # [b_size, max_length, embed_size]
        embedding = self.embedding(captions)

        # exclude end token
        decode_lengths = (caption_lengths - 1).tolist()
        max_length = max(decode_lengths)
        # storage tensors
        logits = torch.zeros(batch_size, max_length, self.num_tokens).to(self.device)
        alphas = torch.zeros(batch_size, max_length, features.shape[1]).to(self.device)

        for t in range(max_length):
            batch_t = sum([l > t for l in decode_lengths])
            # [b_size, encoder_dim]
            features_weighted, alpha = self.attention(features[:batch_t], h[:batch_t])
            # pass weighted features through gate (from paper)
            gate = self.sigmoid(self.f_beta(h[:batch_t]))
            features_weighted = features_weighted * gate

            # cat: [b_size, embed_size], [b_size, encoder_dim]
            input = torch.cat((embedding[:batch_t, t, :], features_weighted), dim=1)
            h, c = self.lstm(input, (h[:batch_t], c[:batch_t]))

            logit = self.fc(self.dropout(h))
            logits[:batch_t, t, :] = logit
            alphas[:batch_t, t, :] = alpha

        return logits, alphas, captions, decode_lengths
    
    # naivce greedy caption generation (BEAM search implemented below)
    def generate_caption(self, features, tokens_to_id, tokens, seed_phrase='', max_length=25): 
        features = features.reshape(1, -1, self.encoder_dim)
        embedding = self.embedding(torch.tensor([tokens_to_id[seed_phrase]]).to(self.device))
        h, c = self.initialize(features)

        output = []
        for i in range(max_length):
            features_weighted, alpha = self.attention(features, h)
            gate = self.sigmoid(self.f_beta(h))
            features_weighted = features_weighted * gate

            input = torch.cat((embedding, features_weighted), dim=1)
            h, c = self.lstm(input, (h, c))

            logits = self.fc(h).squeeze(0)
            # greedy
            next_token = torch.argmax(torch.softmax(logits, dim=0))
            # break if end token reached
            if next_token == tokens_to_id['<end>']:
                break
 
            output.append(tokens[next_token])
            embedding = self.embedding(torch.tensor([next_token]).to(self.device))

        return ' '.join(output)