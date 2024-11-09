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

        # Input: 30 x 18

        self.conv_z_1 = torch.nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=(1, 18)),  # 64 x 30 x 1
            nn.ReLU(inplace=True),
            nn.BatchNorm3d(64),
        )
        self.conv_z_2 = torch.nn.Sequential(
            nn.Conv1d(64, 128, kernel_size=3, stride=3),  # 128 x 10
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(128),
        )
        self.conv_z_3 = torch.nn.Sequential(
            nn.Conv1d(128, 256, kernel_size=3),  # 256 x 8
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(256),
        )
        self.conv_z_4 = torch.nn.Sequential(
            nn.Conv1d(256, 512, kernel_size=3, padding=1), # 512 x 4
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(512),
        )
        self.conv_z_5 = torch.nn.Sequential(
            nn.Conv1d(512, 1024, kernel_size=2), # 1024 x 1
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(1024),
        )

        input_dim = np.prod(state_shape) + np.prod(action_shape) + 1024
        layer_dims = [input_dim] + mlp_layers
        fc = []
        for i in range(len(layer_dims)-1):
            fc.append(nn.Linear(layer_dims[i], layer_dims[i+1]))
            fc.append(nn.ReLU())
        fc.append(nn.Linear(layer_dims[-1], 1))
        self.fc_layers = nn.Sequential(*fc)

    def forward(self, obs, history, actions):
        is_fake_batch = False
        if history.dim() == 4:
            history = history.unsqueeze(1)
        else: # Fake Batch
            is_fake_batch = True
            history = history.unsqueeze(0).unsqueeze(0)
        history = self.conv_z_1(history)
        history = history.squeeze(-1) # 64 x 30
        history = self.conv_z_2(history)
        history = self.conv_z_3(history)
        #history = history.squeeze(-1).squeeze(-1)
        history = torch.max_pool1d(history, 2) # 256 x 4
        history = self.conv_z_4(history)
        history = torch.max_pool1d(history, 2) # 512 x 2
        history = self.conv_z_5(history)
        #history = torch.max_pool1d(history, 2) # 1024 x 1
        history = history.flatten(1,2) # 1024
        if is_fake_batch: # Fake Batch
            history = torch.repeat_interleave(history, obs.shape[0], dim=0)
        obs = torch.cat([history, obs], dim=-1)
        fc_input = torch.cat((obs, actions), dim=1)
        values = self.fc_layers(fc_input).flatten()
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
