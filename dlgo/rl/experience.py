import numpy as np


class ExperienceBuffer:
    def __init__(self, states, actions, rewards):
        self.states = states
        self.actions = actions
        self.rewards = rewards

    def serialize(self, h5file):
        h5file.create_group('experience')
        actions_numeric = np.array(self.actions, dtype=np.int32)
        rewards_numeric = np.array(self.rewards, dtype=np.int32)

        h5file['experience'].create_dataset('states', data=self.states)
        h5file['experience'].create_dataset('actions', data=actions_numeric)
        h5file['experience'].create_dataset('rewards', data=rewards_numeric)


def combine_experience(collectors):
    combined_states = np.concatenate([np.array(c.states) for c in collectors])
    combined_actions = np.concatenate([np.array(c.actions) for c in collectors])
    combined_rewards = np.concatenate([np.array(c.rewards) for c in collectors])

    return ExperienceBuffer(
        combined_states,
        combined_actions,
        combined_rewards)


def load_experience(h5file):
    return ExperienceBuffer(
        states=np.array(h5file['experience']['states']),
        actions=np.array(h5file['experience']['actions']),
        rewards=np.array(h5file['experience']['rewards']))