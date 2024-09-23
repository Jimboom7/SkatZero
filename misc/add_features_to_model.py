import torch

# from skatzero.dmc.neural_net import DMCNet

# model = DMCNet(310, 32)
# model.load_state_dict(torch.load('models/checkpoints/skat_lstm_N/0_4070.pth'))

# model_new = DMCNet(314, 32)

# new_weights = torch.cat((model.state_dict()['fc_layers.0.weight'], torch.zeros((512, 4))), dim=1)

# new_state_dict = model.state_dict()

model_path = 'models/checkpoints/skat_lstm_G/model.tar'
model_path_new = 'models/checkpoints/skat_lstm_G/model_new.tar'

all_models = torch.load(model_path)

# all_models['model_state_dict'][0]['fc_layers.0.weight']
# all_models['optimizer_state_dict'][0]['state'][0]['square_avg']

new_weights = torch.cat((all_models['model_state_dict'][0]['fc_layers.0.weight'][:,:-57], torch.zeros((512, 4), device='cpu'), all_models['model_state_dict'][0]['fc_layers.0.weight'][:,-57:]), dim=1)

all_models['model_state_dict'][0]['fc_layers.0.weight'] = new_weights

state = all_models['optimizer_state_dict'][0]['state'][0]
new_opt = torch.cat((state['square_avg'][:,:-57], torch.zeros((512, 4), device='cpu') + state['square_avg'].mean(), state['square_avg'][:,-57:]), dim=1)
state['square_avg'] = new_opt


torch.save(all_models, model_path_new)
