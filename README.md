# Image Caption Generator
- Implementation of CNN-LSTM with Soft Attention using Encoder/Decoder architecture
- Uses ResNet-34 as the CNN Encoder, LSTM with Attention Network as Decoder
- Trained on Flikr8k dataset
- Hosted locally using Flask/Python/Pytorch for the backend and React/Typescript for the frontend
- Small project that I hope to expand on in the future


# Small Demo
https://user-images.githubusercontent.com/53236934/210160063-38c80279-34c5-439c-af5b-bc5739b4930b.mp4


# Results
- All images in demo and in /results folder were never seen by the model (taken from test dataset)
- It was amazing to see the accuracy that the model with attention could achieve on unseen images, even if it's not a state-of-the-art model compared to now
- Before implementing the Attention network, I tested the model with just a CNN and LSTM, which became proficient at recognizing dogs but not colors or complex relations between objects


# Future Work
- Train on larger datasets (Flickr30k, MSCOCO)
- Implement state-of-the-art models
- Enhance React UI


# Resources
- [Show, Attend, and Tell](https://arxiv.org/pdf/1502.03044.pdf)
