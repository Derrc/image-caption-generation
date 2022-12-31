from collections import defaultdict
import torch
import torch.nn as nn
import numpy as np
from PIL import Image
from urllib.request import urlretrieve
import torchvision.transforms as transforms

START_TOKEN, END_TOKEN, PAD_TOKEN = '<start>', '<end>', '<pad>'
TARGET_SIZE = (256, 256)

transform = transforms.Compose([
    transforms.Resize(TARGET_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# currently for Flickr8k dataset
# return: tokens list, tokens_to_id, num_tokens
def process_tokens(caption_filepath):
    with open(caption_filepath) as f:
        lines = f.read().split('\n')
        # first and last lines are not images
        lines = [line.split(',', maxsplit=1) for line in lines][1:-1]

    # dictionary of image_file -> captions
    captions = defaultdict(list)
    for line in lines:
        image = line[0]
        # add start and end tokens
        caption = f'{START_TOKEN} {line[1]} {END_TOKEN}'
        captions[image].append(caption)

    # parse caption vocabulary for tokens
    tokens = set()
    tokens.add(PAD_TOKEN)
    for caption in captions.values():
        words = [word for sentence in caption for word in sentence.split(' ')]
        tokens = tokens.union(set(words))

    # total number of tokens (vocab size)
    num_tokens = len(tokens)
    tokens = list(tokens)
    tokens.sort()
    tokens_to_id = dict((token, i) for i, token in enumerate(tokens))

    return tokens, tokens_to_id, num_tokens


# run beam search to caption given image
# image: src url
def beam_search(encoder, decoder, image_src, tokens, tokens_to_id, num_tokens, k=3, max_length=35):
    # image preprocessing
    # urlretrieve(image_src, './cache/image.png')
    image = Image.open('./cache/dogs.jpg')
    image = transform(image).unsqueeze(0)

    features = encoder(image)
    # [1, num_pixels, 512]
    features = features.reshape(1, -1, features.shape[3])
    # initialize with batch of k (considering top k candidates for first step)
    features = features.expand(k, features.shape[1], features.shape[2])

    # storage tensors: [k, 1]
    k_prev_words = torch.tensor([[tokens_to_id[START_TOKEN]]] * k, dtype=torch.int64).to(decoder.device)
    k_seq = torch.tensor([[tokens_to_id[START_TOKEN]]] * k, dtype=torch.int64).to(decoder.device)
    top_k_scores = torch.zeros(k, 1).to(decoder.device)

    # storage lists
    seqs_done = list()
    seqs_done_scores = list()

    h, c = decoder.initialize(features)
    for step in range(max_length):
        # [k, embed_size]
        embedding = decoder.embedding(k_prev_words.squeeze(1))

        features_weighted, _ = decoder.attention(features, h)
        gate = torch.sigmoid(decoder.f_beta(h))
        # [k, encoder_dim]
        features_weighted = features_weighted * gate

        input = torch.cat((embedding, features_weighted), dim=1)
        h, c = decoder.lstm(input, (h, c))
        # [k, num_tokens]
        logits = decoder.fc(h)
        # generate all possible [step, step+1] scores, pick top k
        scores = torch.log_softmax(logits, dim=1)

        # scores = sum of log probs
        scores = top_k_scores.expand_as(scores) + scores
        top_k_scores, top_k_tokens = scores.flatten().topk(k, 0, True, True)

        # gets which previous k seq the tokens are part of
        prev_k_indices = top_k_tokens / num_tokens
        prev_k_indices = prev_k_indices.long()
        # gets token_ids
        next_k_indices = top_k_tokens % num_tokens

        # add to previous sequences
        k_seq = torch.cat((k_seq[prev_k_indices], next_k_indices.unsqueeze(1)), dim=1)

        # find all indices that reached 
        indices_not_done = [i for i, token in enumerate(next_k_indices) if token != tokens_to_id[END_TOKEN]]
        indices_done = list(set(range(len(next_k_indices))) - set(indices_not_done))

        if len(indices_done) > 0:
            seqs_done.extend(k_seq[indices_done].tolist())
            seqs_done_scores.extend(top_k_scores[indices_done].tolist())
            k -= len(indices_done)

        # break if all sequences are terminated
        if k == 0:
            break
        
        # update variables to continue from chosen prev sequences
        prev_seq = prev_k_indices[indices_not_done]
        k_seq = k_seq[indices_not_done]
        h = h[prev_seq]
        c = c[prev_seq]
        features = features[prev_seq]
        top_k_scores = top_k_scores[indices_not_done].unsqueeze(1)
        k_prev_words = next_k_indices[indices_not_done].unsqueeze(1)

    ind = np.argmax(seqs_done_scores)
    best_seq = seqs_done[ind]

    best_seq = [tokens[id] for id in best_seq]

    return ' '.join(best_seq)