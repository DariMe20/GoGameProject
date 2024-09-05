# Go AI Reinforcement Learning Project

## Overview

This GitHub repository contains the implementation of a reinforcement learning study focused on developing AI agents capable of playing the board game Go. This project explores the effectiveness of two distinct reinforcement learning methods: gradient descent and Q-value learning.

## Background

Inspired by the groundbreaking work of Google DeepMind's AlphaGo Zero, this project investigates the use of self-taught algorithms in Go, a game known for its complexity and strategic depth that surpasses simple deterministic algorithms. Using a convolutional neural network trained on a 9x9 board, this study aims to demonstrate how a relatively small number of self-played games can impact the performance of an AI with no prior knowledge of the game.

## Implementation Details

### Code Infrastructure

The neuronal network and game infrastructure implemented in this study were developed following the guidelines from "Deep Learning and the Game of Go" by Max Pumperla and Kevin Ferguson. For more in-depth information on the architecture and methodologies, please refer to their work:
[Deep Learning and the Game of Go GitHub Repository](https://github.com/maxpumperla/deep_learning_and_the_game_of_go).

### Technologies Used

- **Python**: Primary programming language.
- **Keras**: Utilized for building and training the neural network.
- **PyQt**: Employed for developing the graphical user interface.

## Methods

### Gradient Descent

- **Description**: Adjusts move probabilities incrementally based on game outcomes, aiming for long-term performance improvements.
- **Training Process**: Involves large volumes of data and subtle tuning of learning rates and batch sizes to refine the agent's decision-making capabilities.

### Q-value Learning

- **Description**: Evaluates the long-term benefits of moves, quickly adapting strategies based on the game dynamics.
- **Training Process**: Shows rapid initial improvements, with performance sensitivity to adjustments in learning parameters and temperature settings.

## GUI

The project includes a graphical user interface that enables users to:
- Challenge the AI agents.
- Watch matches between different AI models.
- Analyze the decision-making process in real-time.

## Results

The study details the evolution of the models through:
- **Self-Played Games**: Generates initial data for training the models by making models play against themselves.
- **Training on Experience**: Each model learns from the outcomes of games it plays.
- **Direct Confrontation**: Models are evaluated by putting them against each other, highlighting the distinct learning curves and strategic adaptations from one version to another.

## Repository Structure

```plaintext
/gradient_descent      # Gradient descent model and training scripts
/q_value               # Q-value model and training scripts
/gui                   # Graphical user interface for interacting with the models
/rlgo                  # Game rules implementation and infrastructure



