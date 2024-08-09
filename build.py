import torch.onnx

from skatzero.dmc.neural_net import DMCNetLSTM

def convert_onnx(player_id, input_size, gametype, postfix):

    path = 'models/checkpoints/skat_lstm_' + gametype + '/' + str(player_id) + '_' + postfix + '.pth'
    model = DMCNetLSTM(input_size, 32)
    model.load_state_dict(torch.load(path).state_dict())

    model.eval()

    dummy_input_obs = torch.zeros(1, input_size, requires_grad=True)
    dummy_input_history = torch.zeros(1, 10, 105, requires_grad=True)
    dummy_input_actions = torch.zeros(1, 32, requires_grad=True)

    # Export the model
    torch.onnx.export(model,         # model being run
         (dummy_input_obs, dummy_input_history, dummy_input_actions),       # model input (or a tuple for multiple inputs)
         f"models/onnx/{gametype}_{player_id}.onnx",       # where to save the model  
         export_params=True,  # store the trained parameter weights inside the model file
         opset_version=17,    # the ONNX version to export the model to
         do_constant_folding=True,  # whether to execute constant folding for optimization
         input_names = ['obs', 'history', 'actions'],   # the model's input names
         output_names = ['output'], # the model's output names
         dynamic_axes={'obs' : {0 : 'batch_size'}, 'history' : {0 : 'batch_size'}, 'actions' : {0 : 'batch_size'},    # variable length axes
                                'output' : {0 : 'batch_size'}}) 
    print(" ")
    print('Model has been converted to ONNX')

if __name__ == "__main__":

    for i, x in enumerate([551, 573, 573]):
        convert_onnx(i, x, 'D', '12620')

    for i, x in enumerate([551, 573, 573]):
        convert_onnx(i, x, 'G', '9980')

    for i, x in enumerate([310, 364, 364]):
        convert_onnx(i, x, 'N', '4060') #4080_0
