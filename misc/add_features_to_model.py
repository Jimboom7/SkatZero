import torch

# from skatzero.dmc.neural_net import DMCNet

# model = DMCNet(310, 32)
# model.load_state_dict(torch.load('models/checkpoints/skat_lstm_N/0_4070.pth'))

# model_new = DMCNet(314, 32)

# new_weights = torch.cat((model.state_dict()['fc_layers.0.weight'], torch.zeros((512, 4))), dim=1)

# new_state_dict = model.state_dict()

model_path = 'models/checkpoints/skat_lstm_D/model.tar'
model_path_2 = 'models/checkpoints/skat_resnet_D/model.tar'
model_path_new = 'models/checkpoints/skat_resnet_D/model_new.tar'

all_models = torch.load(model_path)
all_models_2 = torch.load(model_path_2)

# all_models['model_state_dict'][0]['fc_layers.0.weight']
# all_models['optimizer_state_dict'][0]['state'][0]['square_avg']

for i in range(0,3):
    new_weights = torch.cat((torch.zeros((512, 384), device='cuda:0'), all_models['model_state_dict'][i]['fc_layers.0.weight'][:,:]), dim=1)

    all_models_2['model_state_dict'][i]['fc_layers.0.weight'] = new_weights
    all_models_2['model_state_dict'][i]['fc_layers.0.bias'] = all_models['model_state_dict'][i]['fc_layers.0.bias']
    for j in range(2, 12, 2):
        all_models_2['model_state_dict'][i]['fc_layers.' + str(j) + '.weight'] = all_models['model_state_dict'][i]['fc_layers.' + str(j) + '.weight']
        all_models_2['model_state_dict'][i]['fc_layers.' + str(j) + '.bias'] = all_models['model_state_dict'][i]['fc_layers.' + str(j) + '.bias']

    state = all_models['optimizer_state_dict'][i]['state'][0]
    new_opt = torch.cat((torch.zeros((512, 384), device='cuda:0') + state['square_avg'].mean(), state['square_avg'][:,:]), dim=1)
    all_models_2['optimizer_state_dict'][i]['state'][16]['square_avg'] = new_opt
    for j in range(17, 28):
        all_models_2['optimizer_state_dict'][i]['state'][j]['square_avg'] = all_models['optimizer_state_dict'][i]['state'][j - 16]['square_avg']


torch.save(all_models_2, model_path_new)
