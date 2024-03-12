import numpy as np

from reinforcement_learning.exerience_collector.experience import ExperienceBuffer


class ExperienceCollector:
    def __init__(self):
        self.states = []
        self.actions = []
        self.rewards = []

        self._current_episode_states = []
        self._current_episode_actions = []
        self.experience_buffer = None

    def begin_episode(self):
        self._current_episode_states = []
        self._current_episode_actions = []

    def record_decision(self, state, action, estimated_value=0):
        self._current_episode_states.append(state)
        self._current_episode_actions.append(action)

    def complete_episode(self, reward):
        num_states = len(self._current_episode_states)
        self.states += self._current_episode_states
        self.actions += self._current_episode_actions
        self.rewards += [reward for _ in range(num_states)]

        self._current_episode_states = []
        self._current_episode_actions = []

    def to_buffer(self):
        self.experience_buffer = ExperienceBuffer(
            states=np.array(self.states),
            actions=np.array(self.actions),
            rewards=np.array(self.rewards)
            )
        return self.experience_buffer
