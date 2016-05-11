"""
"""

from ..helpers import normalize_rvs
from ..utils import partitions
from .entropy import entropy

def dilworth(dist, rvs=None, crvs=None, rv_mode=None):
    """
    Calculates the ...

    Parameters
    ----------
    dist : Distribution
        The distribution from which the total correlation is calculated.
    rvs : list, None
        A list of lists. Each inner list specifies the indexes of the random
        variables used to calculate the total correlation. If None, then the
        total correlation is calculated over all random variables, which is
        equivalent to passing `rvs=dist.rvs`.
    crvs : list, None
        A single list of indexes specifying the random variables to condition
        on. If None, then no variables are conditioned on.
    rv_mode : str, None
        Specifies how to interpret `rvs` and `crvs`. Valid options are:
        {'indices', 'names'}. If equal to 'indices', then the elements of
        `crvs` and `rvs` are interpreted as random variable indices. If equal
        to 'names', the the elements are interpreted as random variable names.
        If `None`, then the value of `dist._rv_mode` is consulted, which
        defaults to 'indices'.

    Returns
    -------
    J : float
        The ...

    Examples
    --------
    >>> d = dit.example_dists.Xor()
    >>> dit.multivariate.dilworth(d)
    1.0
    >>> dit.multivariate.dilworth(d, rvs=[[0], [1]])
    0.0

    Raises
    ------
    ditException
        Raised if `dist` is not a joint distribution or if `rvs` or `crvs`
        contain non-existant random variables.
    """
    rvs, crvs, rv_mode = normalize_rvs(dist, rvs, crvs, rv_mode)

    def I_P(part):
        a = sum(entropy(dist, rvs=p, crvs=crvs) for p in part)
        b = entropy(dist, crvs=crvs)
        return a - b

    J = min( I_P(p) for p in partitions(map(tuple, rvs)) if len(p) > 1 )

    return J
