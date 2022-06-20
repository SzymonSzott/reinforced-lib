from functools import partial
from typing import Tuple

import chex
import gym.spaces
import jax
import jax.numpy as jnp

from reinforced_lib.agents.base_agent import BaseAgent, AgentState


@chex.dataclass
class ThompsonSamplingState(AgentState):
    """
    Container for the state of the Thompson Sampling agent.

    Attributes
    ----------
    alpha : array_like
        Number of successful tries for each arm.
    beta : array_like
        Number of failed tries for each arm.
    last_decay : array_like
        Time of the last decay for each arm.
    """

    alpha: chex.Array
    beta: chex.Array
    last_decay: chex.Array


def init(n_arms: jnp.int32) -> ThompsonSamplingState:
    """
    Creates and initializes instance of the Thompson Sampling agent.

    Parameters
    ----------
    n_arms : int
        Number of contextual bandit arms.

    Returns
    -------
    state : ThompsonSamplingState
        Initial state of the Thompson Sampling agent.
    """

    return ThompsonSamplingState(
        alpha=jnp.zeros(n_arms),
        beta=jnp.zeros(n_arms),
        last_decay=jnp.zeros(n_arms)
    )


def update(
        state: ThompsonSamplingState,
        key: chex.PRNGKey,
        action: jnp.int32,
        n_successful: jnp.int32,
        n_failed: jnp.int32,
        time: chex.Scalar,
        decay: chex.Scalar
) -> ThompsonSamplingState:
    """
    Updates the state of the agent after performing some action and receiving a reward.

    Parameters
    ----------
    state : ThompsonSamplingState
        Current state of agent.
    key : chex.PRNGKey
        A PRNG key used as the random key.
    action : int
        Previously selected action.
    n_successful : int
        Number of successful tries.
    n_failed : int
        Number of failed tries.
    time : float
        Current time.
    decay : float
        Smoothing factor.

    Returns
    -------
    state : ThompsonSamplingState
        Updated agent state.
    """

    state = decay_one(state, action, time, decay)
    state = ThompsonSamplingState(
        alpha=state.alpha.at[action].add(n_successful),
        beta=state.beta.at[action].add(n_failed),
        last_decay=state.last_decay
    )
    return state


def sample(
        state: ThompsonSamplingState,
        key: chex.PRNGKey,
        time: chex.Scalar,
        context: chex.Array,
        decay: chex.Scalar
) -> Tuple[ThompsonSamplingState, jnp.int32]:
    """
    Selects next action based on current agent state.

    Parameters
    ----------
    state : ThompsonSamplingState
        Current state of the agent.
    key : chex.PRNGKey
        A PRNG key used as the random key.
    time : float
        Current time.
    context : array_like
        One-dimensional array of features of each arm.
    decay : float
        Smoothing factor.

    Returns
    -------
    tuple[ThompsonSamplingState, int]
        Tuple containing updated agent state and selected action.
    """

    state = decay_all(state, time, decay)
    success_prob = jax.random.beta(key, 1 + state.alpha, 1 + state.beta)
    action = jnp.argmax(success_prob * context)
    return state, action


def decay_one(
        state: ThompsonSamplingState,
        action: jnp.int32,
        time: chex.Scalar,
        decay: chex.Scalar
) -> ThompsonSamplingState:
    """
    Applies exponential smoothing for parameters related to a given action.

    Parameters
    ----------
    state : ThompsonSamplingState
        Current state of the agent.
    action : int
        Action to apply smoothing.
    time : float
        Current time.
    decay : float
        Smoothing factor.

    Returns
    -------
    state : ThompsonSamplingState
        Updated agent state.
    """

    smoothing_value = jnp.exp(decay * (state.last_decay[action] - time))
    state = ThompsonSamplingState(
        alpha=state.alpha.at[action].multiply(smoothing_value),
        beta=state.beta.at[action].multiply(smoothing_value),
        last_decay=state.last_decay.at[action].set(time)
    )
    return state


def decay_all(
        state: ThompsonSamplingState,
        time: chex.Scalar,
        decay: chex.Scalar
) -> ThompsonSamplingState:
    """
    Applies exponential smoothing for parameters of all arms.

    Parameters
    ----------
    state : ThompsonSamplingState
        Current state of the agent.
    time : float
        Current time.
    decay : float
        Smoothing factor.

    Returns
    -------
    state : ThompsonSamplingState
        Updated agent state.
    """

    smoothing_value = jnp.exp(decay * (state.last_decay - time))
    state = ThompsonSamplingState(
        alpha=state.alpha * smoothing_value,
        beta=state.beta * smoothing_value,
        last_decay=jnp.full_like(state.last_decay, time)
    )
    return state


class ThompsonSampling(BaseAgent):
    """
    Contextual Thompson Sampling agent with exponential smoothing.

    Parameters
    ----------
    context : array_like
        One-dimensional array of arms values.
    decay : float, default=1.0
        Smoothing factor (decay = 0.0 means no smoothing).
    """

    def __init__(self, context: chex.Array, decay: chex.Scalar = 1.0) -> None:
        self.context_len = len(context)

        self.init = jax.jit(partial(init, n_arms=self.context_len))
        self.update = jax.jit(partial(update, decay=decay))
        self.sample = jax.jit(partial(sample, context=context, decay=decay))

    @property
    def update_observation_space(self) -> gym.spaces.Dict:
        return gym.spaces.Dict({
            'action': gym.spaces.Discrete(self.context_len),
            'n_successful': gym.spaces.Box(0, jnp.inf, (1,), jnp.int32),
            'n_failed': gym.spaces.Box(0, jnp.inf, (1,), jnp.int32),
            'time': gym.spaces.Box(0.0, jnp.inf, (1,))
        })

    @property
    def sample_observation_space(self) -> gym.spaces.Dict:
        return gym.spaces.Dict({
            'time': gym.spaces.Box(0.0, jnp.inf, (1,))
        })

    @property
    def action_space(self) -> gym.spaces.Discrete:
        return gym.spaces.Discrete(self.context_len)
