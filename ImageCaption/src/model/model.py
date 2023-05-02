'''
    Module contains final Model and all pieces of it.
'''
import torch
import torch.nn as nn
from transformers import CLIPModel, CLIPProcessor, GPT2LMHeadModel, GPT2Tokenizer

class ImageEncoder(nn.Module):
    '''
        Encodes image and returns it's embedding.
    '''

    def __int__(self, model, device='cpu'):
        super(ImageEncoder, self).__int__()
        self.device = device

        self.preprocessor = CLIPProcessor.from_pretrained(model)
        self.model = CLIPModel.from_pretrained(model).vision_model.to(self.device)

    def forward(self, image):
        # only one image at a time
        image = self.preprocessor(images=image, return_tensors='pt').to(self.device)
        image_features = self.model(**image)

        return image_features.pooler_output

class Mapping(nn.Module):
    '''
        Maps image embedding to GPT-2 embedding.
    '''

    def __init(
        self,
        ep_len,
        num_layers,
        embed_size,
        n_heads,
        forward_expansion,
        dropout,
        device='cpu'
    ):
        super(Mapping, self).__init()
        self.ep_len = ep_len
        self.embed_size = embed_size
        self.device = device

        self.transformer_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=embed_size,
                nhead=n_heads,
                dim_feedforward=embed_size*forward_expansion,
                dropout=dropout,
                batch_first=True,
                device=device
            ),
            num_layers=num_layers
        ).to(self.device)

        self.mapper = nn.Linear(embed_size, ep_len * embed_size).to(self.device)

        self.init_weights()

    def forward(self, img_embedded, train_mode=False):
        x = self.transformer_encoder(img_embedded)
        x = self.mapper(x)

        x = x.view(
            *(
                [-1, self.ep_len, self.embed_size]
                if train_mode else
                [self.ep_len, self.embed_size]
            )
        )  # for batched input

        return x

    def init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weights, mode='fan_in', nonlinearity='relu')
                nn.init.zeros_(m.bias)

            elif isinstance(m, nn.LayerNorm):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)

class TextDecoder(nn.Module):
    '''
        Processes embedding into caption.
    '''

    def __init__(self, model, device='cpu'):
        super().__init__()
