import numpy as np
import torch

from skatzero.dmc.neural_net import DMCNet

class DMCAgent:
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512],
        exp_epsilon=0.01,
        device="0",
    ):
        self.device = 'cuda:'+device if device != "cpu" else "cpu"
        self.net = DMCNet(state_shape, action_shape, mlp_layers).to(self.device)
        self.exp_epsilon = exp_epsilon
        self.action_shape = action_shape

    def step(self, state):
        if self.exp_epsilon > 0 and np.random.rand() < self.exp_epsilon:
            legal_actions = state['legal_actions']
            action_keys = np.array(list(legal_actions.keys()))
            action = np.random.choice(action_keys)
        else:
            action_keys, values = self.predict(state)
            action_idx = np.argmax(values)
            action = action_keys[action_idx]

        return action

    def eval_step(self, state, raw=False):
        action_keys, values = self.predict(state, raw)

        action_idx = np.argmax(values)
        action = action_keys[action_idx]

        info = {}
        info['values'] = {state['raw_legal_actions'][i]: float(values[i]) for i in range(len(action_keys))}

        return action, info

    def share_memory(self):
        self.net.share_memory()

    def eval(self):
        self.net.eval()

    def parameters(self):
        return self.net.parameters()

    def predict(self, state, raw=False):
        legal_actions = state['legal_actions']
        if len(legal_actions) == 1 and not raw:
            return np.array(list(legal_actions.keys())), np.array([100])

        obs = state['obs'].astype(np.float32)
        history = state['history'].astype(np.float32)

        action_keys = np.array(list(legal_actions.keys()))
        action_values = list(legal_actions.values())
        for i in range(len(action_values)):
            if action_values[i] is None:
                action_values[i] = np.zeros(self.action_shape[0])
                action_values[i][action_keys[i]] = 1
        action_values = np.array(action_values, dtype=np.float32)

        obs = np.repeat(obs[np.newaxis, :], len(action_keys), axis=0)
        # history = np.repeat(history[np.newaxis, :, :], len(action_keys), axis=0)

        with torch.no_grad():
            values = self.net.forward(torch.from_numpy(obs).to(self.device), torch.from_numpy(history).to(self.device),
                                        torch.from_numpy(action_values).to(self.device))

        return action_keys, values.cpu().detach().numpy()

    def forward(self, obs, history, actions):
        return self.net.forward(obs, history, actions)

    def load_state_dict(self, state_dict):
        return self.net.load_state_dict(state_dict)

    def state_dict(self):
        return self.net.state_dict()

    def set_device(self, device):
        self.device = device
