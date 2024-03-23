import torch.onnx

from skatzero.dmc.neural_net import DMCNet

def convert_onnx(player_id, input_size):

    path = "checkpoints/skat_30_final/model.tar"
    model = DMCNet(input_size, 32)
    model.load_state_dict(torch.load(path)['model_state_dict'][player_id])

    model.eval()

    dummy_input_obs = torch.zeros(1, input_size, requires_grad=True)
    dummy_input_actions = torch.zeros(1, 32, requires_grad=True)

    # Export the model
    torch.onnx.export(model,         # model being run
         (dummy_input_obs, dummy_input_actions),       # model input (or a tuple for multiple inputs)
         f"onnx/normal_{player_id}.onnx",       # where to save the model  
         export_params=True,  # store the trained parameter weights inside the model file
         opset_version=17,    # the ONNX version to export the model to
         do_constant_folding=True,  # whether to execute constant folding for optimization
         input_names = ['obs', 'actions'],   # the model's input names
         output_names = ['output'], # the model's output names
         dynamic_axes={'obs' : {0 : 'batch_size'}, 'actions' : {0 : 'batch_size'},    # variable length axes
                                'output' : {0 : 'batch_size'}}) 
    print(" ")
    print('Model has been converted to ONNX')

if __name__ == "__main__":

    for i, x in enumerate([1601, 1623, 1623]):
        convert_onnx(i, x)
