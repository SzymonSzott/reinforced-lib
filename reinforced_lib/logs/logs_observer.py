from collections import defaultdict
from typing import Any, Callable, Dict, List

import jax.numpy as jnp

from reinforced_lib.agents import BaseAgent
from reinforced_lib.logs import BaseLogger, Source, SourceType
from reinforced_lib.utils.exceptions import IncorrectLoggerTypeError, IncorrectSourceTypeError


class LogsObserver:
    """
    Class responsible for managing singleton instances of the loggers, initialization and finalization
    of the loggers, and passing the logged values to the appropriate loggers and methods.
    """

    def __init__(self) -> None:
        self._loggers_instances = {}
        self._loggers_sources = defaultdict(list)

        self._observations_loggers = defaultdict(list)
        self._agent_state_loggers = defaultdict(list)
        self._metrics_loggers = defaultdict(list)

    def add_logger(self, source: Source, logger_type: type, logger_params: Dict[str, Any]) -> None:
        """
        Initializes a singleton instance of the logger and connects a given source with that logger.

        Parameters
        ----------
        source : Source
            Source to connect.
        logger_type : type
            Type of the selected loger.
        logger_params : dict
            Parameters of the selected logger.
        """

        if not issubclass(logger_type, BaseLogger):
            raise IncorrectLoggerTypeError(logger_type)

        if isinstance(source, tuple):
            if len(source) != 2 or not isinstance(source[0], str) or not hasattr(source[1], 'name'):
                raise IncorrectSourceTypeError(type(source))
        elif not isinstance(source, str):
            raise IncorrectSourceTypeError(type(source))

        logger = self._loggers_instances.get(logger_type, logger_type(**logger_params))

        if isinstance(source, tuple):
            if source[1] == SourceType.OBSERVATION:
                self._observations_loggers[logger].append((source, source[0]))
            elif source[1] == SourceType.STATE:
                self._agent_state_loggers[logger].append((source, source[0]))
            elif source[1] == SourceType.METRIC:
                self._metrics_loggers[logger].append((source, source[0]))
        elif isinstance(source, str):
            self._observations_loggers[logger].append((source, source))
            self._agent_state_loggers[logger].append((source, source))
            self._metrics_loggers[logger].append((source, source))

        self._loggers_sources[logger].append(source)
        self._loggers_instances[logger_type] = logger

    def init_loggers(self):
        """
        Initializes all loggers by calling their ``init`` method.
        """

        for logger, sources in self._loggers_sources.items():
            logger.init(sources)

    def finish_loggers(self):
        """
        Finalizes the work of all loggers by calling their ``finish`` method.
        """

        for logger in self._loggers_sources.keys():
            logger.finish()

    def update_observations(self, observations: Any) -> None:
        """
        Passes new observations to the loggers.

        Parameters
        ----------
        observations : dicy or any
            Observations received by the agent.
        """

        if isinstance(observations, dict):
            self._update(self._observations_loggers, lambda name: observations.get(name, None))
        else:
            self._update(self._observations_loggers, lambda name: observations)

    def update_agent_state(self, agent_state: BaseAgent) -> None:
        """
        Passes the agent state to the loggers.

        Parameters
        ----------
        agent_state : BaseAgent
            Current agent state.
        """

        self._update(self._agent_state_loggers, lambda name: getattr(agent_state, name, None))

    def update_metrics(self, metric: Any, metric_name: str) -> None:
        """
        Passes metrics to loggers.

        Parameters
        ----------
        metric : any
            Metric value.
        metric_name : str
            Name of the metric.
        """

        self._update(self._metrics_loggers, lambda name: metric if name == metric_name else None)

    @staticmethod
    def _update(loggers: Dict[BaseLogger, List[str]], get_value: Callable) -> None:
        """
        Passes values to the appropriate loggers and method based on the type and the source of the value.

        Parameters
        ----------
        loggers : dict
            Dictionary with the loggers instances and the connected sources.
        get_value : callable
            Function that gets the selected value from the observations, state, or metrics.
        """

        for logger, sources in loggers.items():
            for source, name in sources:
                if (value := get_value(name)) is not None:
                    if jnp.isscalar(value) or (hasattr(value, 'ndim') and value.ndim == 0):
                        logger.log_scalar(source, value)
                    elif isinstance(value, dict):
                        logger.log_dict(source, value)
                    elif isinstance(value, (list, tuple)) or (hasattr(value, 'ndim') and value.ndim == 1):
                        logger.log_array(source, value)
                    else:
                        logger.log_other(source, value)
