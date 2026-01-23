from __future__ import annotations

from dataclasses import dataclass
from math import factorial
from typing import Dict, Iterable, Optional, Union

import numpy as np


def sysmult_to_csbend_K(
    order: Union[Iterable[int], np.ndarray],
    normal: Union[Iterable[float], np.ndarray],
    skew: Optional[Union[Iterable[float], np.ndarray]] = None,
    *,
    L: float,
    angle: float,
    reference_radius: float,
    max_order: int = 8,
    output: str = "K",  # "K" -> K1..K8 (1/m^(n+1)), "b" -> b1..b8 (1/m^n)
) -> Dict[str, float]:
    """
    Convert SDDS (.MULT) normal/skew multipole fractions into CSBEND multipole parameters.

    Elegant CSBEND field expansions (midplane):
        By = B0 * (1 + sum_n (K_n * rho / n!) x^n)
        By = B0 * (1 + sum_n (b_n       / n!) x^n)   [when USE_bN != 0]
    => b_n = K_n * rho  =>  K_n = b_n / rho.

    SDDS multipole convention for SYSTEMATIC_MULTIPOLES files:
        a_n ("normal") is fractional field error at x=Rref:
            a_n = (ΔBy/B0)|_{x=Rref} = (b_n/n!) * Rref^n
        => b_n = a_n * n! / Rref^n
        => K_n = a_n * n! / (rho * Rref^n)

    Parameters
    ----------
    order : multipole order n (quad=1, sext=2, ...)
    normal, skew : SDDS columns (fractions at x=Rref)
    L, angle : CSBEND geometry; rho = L/angle
    reference_radius : SDDS referenceRadius [m]
    max_order : maximum n to return (CSBEND practical limit is 8)
    output : "K" or "b"

    Returns
    -------
    dict mapping parameter names to values:
      - if output="K": {"K1":..., "K2":..., ...} and optionally {"KS1":...}
      - if output="b": {"b1":..., "b2":..., ...} and optionally {"bs1":...}
    """
    if reference_radius <= 0:
        raise ValueError("reference_radius must be > 0.")
    if L <= 0:
        raise ValueError("L must be > 0.")
    if angle == 0:
        raise ValueError("angle must be nonzero (rho = L/angle).")

    rho = L / angle
    R = reference_radius

    order_arr = np.asarray(list(order), dtype=int)
    normal_arr = np.asarray(list(normal), dtype=float)
    if order_arr.shape != normal_arr.shape:
        raise ValueError("order and normal must have the same length.")

    skew_arr = None
    if skew is not None:
        skew_arr = np.asarray(list(skew), dtype=float)
        if skew_arr.shape != order_arr.shape:
            raise ValueError("skew must have the same length as order/normal.")

    out: Dict[str, float] = {}

    def emit(values: np.ndarray, prefix: str) -> None:
        for n, a_n in zip(order_arr, values):
            if not (1 <= n <= max_order):
                continue
            # b_n in By/B0 expansion
            b_n = float(a_n) * factorial(int(n)) / (R ** int(n))
            if output.lower() == "b":
                out[f"{prefix}{n}"] = b_n
            elif output.lower() == "k":
                out[f"{prefix}{n}"] = b_n / rho
            else:
                raise ValueError('output must be "K" or "b".')

    if output.lower() == "b":
        emit(normal_arr, "b")
        if skew_arr is not None:
            emit(skew_arr, "bs")
    else:
        emit(normal_arr, "K")
        if skew_arr is not None:
            emit(skew_arr, "KS")

    return out


def sysmult_sdds_dict_to_csbend_K(
    sdds_dict: dict,
    *,
    L: float,
    angle: float,
    max_order: int = 8,
    output: str = "K",
    normal_key: str = "normal",
    skew_key: str = "skew",
    order_key: str = "order",
    reference_radius_key: str = "referenceRadius",
) -> Dict[str, float]:
    """
    Convert a single pyelegant.sdds.sdds2dicts() record into CSBEND multipole parameters.
    """
    R = float(sdds_dict["params"][reference_radius_key])
    cols = sdds_dict["columns"]
    order = cols[order_key]
    normal = cols[normal_key]
    skew = cols.get(skew_key, None)
    return sysmult_to_csbend_K(
        order=order,
        normal=normal,
        skew=skew,
        L=L,
        angle=angle,
        reference_radius=R,
        max_order=max_order,
        output=output,
    )


if __name__ == "__main__":
    import pyelegant as pe

    sdds_path = (
        "/dev/shm/yhidaka-tmp/tmpLteZip_3w3fd5nw/lte_suppl/sys_mpole/CB1_1_000.MULT"
    )
    records = pe.sdds.sdds2dicts(sdds_path)

    # CSBEND example:
    L = 0.1
    ANGLE = 0.005550718042358

    # convert first record -> K's
    Kvals = sysmult_sdds_dict_to_csbend_K(
        records[0], L=L, angle=ANGLE, max_order=8, output="K"
    )
    print("Converted CSBEND multipoles (K form):")
    for k in sorted(Kvals.keys(), key=lambda s: (len(s), s)):
        print(f"  {k} = {Kvals[k]:.12g}")

    # If you prefer USE_BN=1 style coefficients:
    bvals = sysmult_sdds_dict_to_csbend_K(
        records[0], L=L, angle=ANGLE, max_order=8, output="b"
    )
    print("\nConverted CSBEND multipoles (b form):")
    for k in sorted(bvals.keys(), key=lambda s: (len(s), s)):
        print(f"  {k} = {bvals[k]:.12g}")
