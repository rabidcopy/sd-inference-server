import os
import torch
import torch.nn as nn
import torch.nn.functional as F

import geffnet

class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()

        basemodel_name = 'tf_efficientnet_b5_ap'
        basemodel = geffnet.create_model(basemodel_name, pretrained=True)

        # Remove last layer
        basemodel.global_pool = nn.Identity()
        basemodel.classifier = nn.Identity()

        self.original_model = basemodel

    def forward(self, x):
        features = [x]
        for k, v in self.original_model._modules.items():
            if (k == 'blocks'):
                for ki, vi in v._modules.items():
                    features.append(vi(features[-1]))
            else:
                features.append(v(features[-1]))
        return features


