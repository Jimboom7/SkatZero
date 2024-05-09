from skatzero.agents.deep_agent import DMCAgent, DMCAgentLSTM


class DMCModel:
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512],
        exp_epsilon=0.01,
        device=0
    ):
        self.agents = []
        for player_id in range(len(state_shape)):
            agent = DMCAgent(
                state_shape[player_id],
                action_shape[player_id],
                mlp_layers,
                exp_epsilon,
                device,
            )
            self.agents.append(agent)

    def share_memory(self):
        for agent in self.agents:
            agent.share_memory()

    def eval(self):
        for agent in self.agents:
            agent.eval()

    def parameters(self, index):
        return self.agents[index].parameters()

    def get_agent(self, index):
        return self.agents[index]

    def get_agents(self):
        return self.agents

class DMCModelLSTM:
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512],
        exp_epsilon=0.01,
        device=0
    ):
        self.agents = []
        for player_id in range(len(state_shape)):
            agent = DMCAgentLSTM(
                state_shape[player_id],
                action_shape[player_id],
                mlp_layers,
                exp_epsilon,
                device,
            )
            self.agents.append(agent)

    def share_memory(self):
        for agent in self.agents:
            agent.share_memory()

    def eval(self):
        for agent in self.agents:
            agent.eval()

    def parameters(self, index):
        return self.agents[index].parameters()

    def get_agent(self, index):
        return self.agents[index]

    def get_agents(self):
        return self.agents
