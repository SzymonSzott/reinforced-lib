.. _agents_page:

Agents
======

This module is a set of RL agents. You can either choose one of our built-in agents or implement
your agent with the help of the :ref:`Custom agents` guide.


BaseAgent
---------

.. currentmodule:: reinforced_lib.agents.base_agent

.. autoclass:: AgentState
    :members:

.. autoclass:: BaseAgent
    :members:


Deep Q-Learning
---------------

.. currentmodule:: reinforced_lib.agents.deep.q_learning

.. autoclass:: QLearningState
    :show-inheritance:
    :members:

.. autoclass:: QLearning
    :show-inheritance:
    :members:


Deep Expected SARSA
-------------------

.. currentmodule:: reinforced_lib.agents.deep.expected_sarsa

.. autoclass:: ExpectedSarsaState
    :show-inheritance:
    :members:

.. autoclass:: ExpectedSarsa
    :show-inheritance:
    :members:


Deep Double Q-Learning (DQN)
----------------------------

.. currentmodule:: reinforced_lib.agents.deep.dqn

.. autoclass:: DQNState
    :show-inheritance:
    :members:

.. autoclass:: DQN
    :show-inheritance:
    :members:


Deep Deterministic Policy Gradient (DDPG)
-----------------------------------------

.. currentmodule:: reinforced_lib.agents.deep.ddpg

.. autoclass:: DDPGState
    :show-inheritance:
    :members:

.. autoclass:: DDPG
    :show-inheritance:
    :members:


Epsilon-greedy
--------------

.. currentmodule:: reinforced_lib.agents.mab.e_greedy

.. autoclass:: EGreedyState
    :show-inheritance:
    :members:

.. autoclass:: EGreedy
    :show-inheritance:
    :members:


Exp3
----

.. currentmodule:: reinforced_lib.agents.mab.exp3

.. autoclass:: Exp3State
    :show-inheritance:
    :members:

.. autoclass:: Exp3
    :show-inheritance:
    :members:


Softmax
---------------

.. currentmodule:: reinforced_lib.agents.mab.softmax

.. autoclass:: SoftmaxState
    :show-inheritance:
    :members:

.. autoclass:: Softmax
    :show-inheritance:
    :members:


Thompson sampling
-----------------

.. currentmodule:: reinforced_lib.agents.mab.thompson_sampling

.. autoclass:: ThompsonSamplingState
    :show-inheritance:
    :members:

.. autoclass:: ThompsonSampling
    :show-inheritance:
    :members:


Upper confidence bound (UCB)
----------------------------

.. currentmodule:: reinforced_lib.agents.mab.ucb

.. autoclass:: UCBState
    :show-inheritance:
    :members:

.. autoclass:: UCB
    :show-inheritance:
    :members:


Particle filter (Core)
----------------------

.. automodule:: reinforced_lib.agents.core.particle_filter
    :show-inheritance:
    :members:
