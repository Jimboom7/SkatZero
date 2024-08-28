import numpy as np

import torch
from torch import nn

class DMCNet(nn.Module):
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512]
    ):
        super().__init__()
        input_dim = np.prod(state_shape) + np.prod(action_shape)
        layer_dims = [input_dim] + mlp_layers
        fc = []
        for i in range(len(layer_dims)-1):
            fc.append(nn.Linear(layer_dims[i], layer_dims[i+1]))
            fc.append(nn.ReLU())
        fc.append(nn.Linear(layer_dims[-1], 1))
        self.fc_layers = nn.Sequential(*fc)

    def forward(self, obs, actions):
        obs = torch.flatten(obs, 1)
        actions = torch.flatten(actions, 1)
        x = torch.cat((obs, actions), dim=1)
        values = self.fc_layers(x).flatten()
        return values

class DMCNetLSTM(nn.Module):
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512]
    ):
        super().__init__()
        input_dim = np.prod(state_shape) + np.prod(action_shape) + 128
        layer_dims = [input_dim] + mlp_layers
        fc = []
        for i in range(len(layer_dims)-1):
            fc.append(nn.Linear(layer_dims[i], layer_dims[i+1]))
            fc.append(nn.ReLU())
        fc.append(nn.Linear(layer_dims[-1], 1))
        self.fc_layers = nn.Sequential(*fc)
        self.lstm = nn.LSTM(105, 128, batch_first=True)

    def forward(self, obs, history, actions):
        lstm_out, (_, _) = self.lstm(history)
        if history.dim() == 2:
            lstm_out = lstm_out[-1:,:] # transforms lstm output to shape (batch_size, hidden_dim)
            lstm_out = torch.repeat_interleave(lstm_out, obs.shape[0], dim=0)
        else:
            lstm_out = lstm_out[:,-1,:] # transforms lstm output to shape (batch_size, hidden_dim)
        obs = torch.cat([lstm_out, obs], dim=-1)
        #obs = torch.flatten(obs, 1)
        #actions = torch.flatten(actions, 1)
        x = torch.cat((obs, actions), dim=1)
        values = self.fc_layers(x).flatten()
        return values
