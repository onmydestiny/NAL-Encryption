import numpy as np
from numba import njit, prange
from numpy import typing as npt


@njit
def _crypt_part(dest: npt.NDArray[np.uint8], part: npt.NDArray[np.uint8],
                i: int, part_num: int, prepared_passwds: npt.NDArray[np.uint8],
                decrypt: bool = False) -> None:
    if len(part) % 512 != 0 or len(part) == 0: raise ValueError("Part length must be equal 526k, k != 0")
    used_prepared_passwd = prepared_passwds[-i-1 if decrypt else i]
    n_shifts = len(part) // 512

    for block in range(n_shifts):
        shift = block + part_num
        for j in range(512):
            dest[block * 512 + j] = part[block * 512 + j] ^ used_prepared_passwd[(j - shift) % 512]


@njit
def crypt_parts(parts: npt.NDArray[np.uint8], i: int,
                 prepared_passwds: npt.NDArray[np.uint8], decrypt: bool = False) -> npt.NDArray[np.uint8]:
    res = np.empty_like(parts)
    for idx in prange(4):
        _crypt_part(res[idx], parts[idx], i, idx, prepared_passwds, decrypt)
    return res