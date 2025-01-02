"""
   NAL Encryption. Easy encryption
   Copyright (C) 2025 David Lishchyshen

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 3 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections import deque
from itertools import cycle
from typing import Iterable, Union

input_type = Union[str, bytes, Iterable[int]]

class NALEnc:
    def __init__(self, passwd: input_type):
        passwd_encoded = self.__encode_value(passwd)
        if len(passwd_encoded) != 512: raise ValueError("passwd len must equal 512 byte")
        self.__validate_data(passwd_encoded)
        self.__passwd = passwd_encoded
        self.__prepare_passwds()


    def encrypt(self, msg: input_type) -> list[int]:
        message = self.__encode_value(msg)

        self.__validate_data(message)

        message = self.__finish_message(message)

        parts = self.__split_message(message)

        for i in range(256):
            for k in range(3):
                parts[k] = [v ^ parts[k+1][idx] for idx, v in enumerate(parts[k])]
            for idx, part in enumerate(parts):
                self.__crypt_part(part, i, idx)
            d = deque(parts)
            d.rotate(1)
            parts = list(d)
        res = []
        for part in parts:
            res.extend(part)

        return res


    def decrypt(self, msg: input_type) -> list[int]:
        message = self.__encode_value(msg)

        self.__validate_data(message)

        parts = self.__split_message(message)

        for i in range(256):
            d = deque(parts)
            d.rotate(-1)
            parts = list(d)
            for idx, part in enumerate(parts):
                self.__crypt_part(part, i, idx, True)
            for k in range(3):
                parts[2-k] = [v ^ parts[3-k][idx] for idx, v in enumerate(parts[2-k])]

        res = []
        for part in parts:
            res.extend(part)

        return self.__cut_message(res)


    def __crypt_part(self, part: list[int], i: int, part_num: int, decrypt: bool = False) -> list[int]:
        if len(part) % 512 != 0 or len(part) == 0: raise ValueError("Part length must be equal 526k, k != 0")
        passwd: list[int] = []
        d = deque(self.__prepared_passwds[::-1][i] if decrypt else self.__prepared_passwds[i])
        d.rotate(part_num)
        passwd.extend(d)
        for p in range(int(len(part) / 512)-1):
            d.rotate(1)
            passwd.extend(d)

        for idx, val in enumerate(part):
            part[idx] = val ^ passwd[idx]
        return part


    def __prepare_passwds(self) -> None:
        self.__prepared_passwds: list[list[int]] = [self.__passwd.copy()]
        for i in range(0, 255):
            xor_value = self.__prepared_passwds[i-1][i]
            self.__prepared_passwds.append([self.__prepared_passwds[i-1][k] ^ xor_value for k in range(len(self.__passwd)) if k != i])
            self.__prepared_passwds[i+1].insert(i, xor_value)


    def __finish_message(self, msg: list[int]) -> list[int]:
        additional_len = 2046 - (len(msg) % 2046) + (len(msg) // 2048) * 2
        if additional_len != 2046 or len(msg) % 2048 == 0:
            l1, l2 = additional_len >> 8, additional_len & 0xFF
            for _, k in zip(range(additional_len), cycle(self.__passwd)):
                msg.append(msg[k % len(msg)] ^ msg[(k+1) % len(msg)])
            msg.insert(0, l2)
            msg.insert(0, l1)
        else:
            msg.insert(0, 0)
            msg.insert(0, 0)
        return msg


    def __validate_data(self, data: list[int]) -> None:
        if not all(isinstance(i, int) for i in data): raise TypeError("all list element must be int")
        if not self.__validate_list_values(data): raise ValueError("every msg element must be less 256 and bigger or equal to 0")


    @staticmethod
    def __split_message(msg: list[int]) -> list[list[int]]:
        return [msg[int(i*512*len(msg)/2048):int((i+1)*512*len(msg)/2048)] for i in range(4)]


    @staticmethod
    def __encode_value(value: input_type) -> list[int]:
        if isinstance(value, str): return list(value.encode())
        elif isinstance(value, bytes): return list(value)
        elif isinstance(value, list): return value.copy()
        else: raise TypeError("argument must be str | bytes | list[int]")


    @staticmethod
    def __validate_list_values(lst: list[int]) -> bool:
        for i in lst:
            if i < 0 or i > 255: return False
        return True


    @staticmethod
    def __cut_message(msg: list[int]) -> list[int]:
        additional_len = (msg[0] << 8) | msg[1]
        return msg[2:len(msg) - additional_len]

__all__ = ["NALEnc"]