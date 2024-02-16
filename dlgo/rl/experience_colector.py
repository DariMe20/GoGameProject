import numpy as np

from dlgo.goboard import GameState
from dlgo.rl.experience import ExperienceBuffer


class ExperienceCollector:
    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.current_episode_states = []
        self.current_episode_actions = []
        self.current_episode_rewards = []

    def begin_episode(self):
        self.current_episode_states = []
        self.current_episode_actions = []
        self.current_episode_rewards = []

    def record_decision(self, state, action, reward=0):

        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        
    def complete_episode(self, reward):
        print("Completed episode with reward: ", reward)
        num_states = len(self.current_episode_states)
        self.states += self.current_episode_states
        self.actions += self.current_episode_actions

        # Aici poți ajusta recompensa în funcție de rezultatul jocului și de capturi
        final_rewards = [reward + additional_reward for additional_reward in self.current_episode_rewards]

        self.rewards += final_rewards
        self.current_episode_states = []
        self.current_episode_actions = []
        self.current_episode_rewards = []

    def to_buffer(self):
        return ExperienceBuffer(
            states=np.array(self.states),
            actions=np.array(self.actions),
            rewards=np.array(self.rewards)
        )