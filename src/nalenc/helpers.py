import numpy as np
from numba import njit, prange
from numpy import typing as npt


@njit
def _crypt_part8(dest: npt.NDArray[np.uint8], part: npt.NDArray[np.uint8],
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
def _crypt_parts8(parts: npt.NDArray[np.uint8], i: int,
                 prepared_passwds: npt.NDArray[np.uint8], decrypt: bool = False) -> npt.NDArray[np.uint8]:
    res = np.empty_like(parts)
    for idx in prange(4):
        _crypt_part8(res[idx], parts[idx], i, idx, prepared_passwds, decrypt)
    return res

@njit
def _crypt_block64_inplace(dest: npt.NDArray[np.uint64], src: npt.NDArray[np.uint64],
                           used_prepared_passwd: npt.NDArray[np.uint64],
                           shift: int) -> None:
    n = dest.shape[0]
    for i in prange(n):
        idx = (i - shift) % 64
        dest[i] = src[i] ^ used_prepared_passwd[idx]

@njit
def _crypt_part64_inplace(dest: npt.NDArray[np.uint8], src: npt.NDArray[np.uint8],
                          i: int, part_num: int, prepared_passwds: npt.NDArray[np.uint8],
                          decrypt: bool = False) -> None:
    if len(src) % 512 != 0 or len(src) == 0:
        raise ValueError("Part length must be equal 526k, k != 0")

    used_prepared_passwd = prepared_passwds[-i-1 if decrypt else i].view(np.uint64)
    src64 = src.view(np.uint64)
    dest64 = dest.view(np.uint64)

    n_blocks = len(src64) // 64
    block_size = 64

    for block in range(n_blocks):
        block_offset = block * block_size
        shift = block + part_num
        _crypt_block64_inplace(dest64[block_offset:block_offset+block_size],
                               src64[block_offset:block_offset+block_size],
                               used_prepared_passwd,
                               shift)

@njit(parallel=True)
def _crypt_parts64(parts: npt.NDArray[np.uint8], i: int,
                  prepared_passwds: npt.NDArray[np.uint8], decrypt: bool = False) -> npt.NDArray[np.uint8]:
    tmp = np.empty_like(parts)
    for idx in prange(4):
        _crypt_part64_inplace(tmp[idx], parts[idx], i, idx, prepared_passwds, decrypt)
    return tmp

def crypt_parts(parts: npt.NDArray[np.uint8], i: int,
                prepared_passwds: npt.NDArray[np.uint8], decrypt: bool = False) -> npt.NDArray[np.uint8]:
    if len(parts[0]) < 65536:
        return _crypt_parts8(parts, i, prepared_passwds, decrypt)
    else:
        return _crypt_parts64(parts, i, prepared_passwds, decrypt)