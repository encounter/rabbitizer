#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022-2024 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

from .Enum import Enum
from .InstrCategory import InstrCategory
from .TrinaryValue import TrinaryValue


class Instruction:
    rs: Enum
    """The value of the `rs` register for this instruction.
    The type of this attribute will be either a `RegGprO32` or a `RegGprN32` depending on the current `config.regNames_gprAbiNames` value.
    If the current instruction does not use the `rs` register, then a Runtime exception will be raised.
    Read-only."""
    rt: Enum
    """The value of the `rt` register for this instruction.
    The type of this attribute will be either a `RegGprO32` or a `RegGprN32` depending on the current `config.regNames_gprAbiNames` value.
    If the current instruction does not use the `rt` register, then a Runtime exception will be raised.
    Read-only."""
    rd: Enum
    """The value of the `rd` register for this instruction.
    The type of this attribute will be either a `RegGprO32` or a `RegGprN32` depending on the current `config.regNames_gprAbiNames` value.
    If the current instruction does not use the `rd` register, then a Runtime exception will be raised.
    Read-only."""
    sa: int
    """The value of the `sa` field for this instruction.
    If the current instruction does not have a `sa` field, then a Runtime exception will be raised.
    Read-only."""
    fs: Enum
    """The value of the `fs` register for this instruction.
    The type of this attribute will be either a `RegGprO32`, `RegGprN32` or a `RegGprN64` depending on the current `config.regNames_gprAbiNames` value.
    If the current instruction does not use the `fs` register, then a Runtime exception will be raised.
    Read-only."""
    ft: Enum
    """The value of the `ft` register for this instruction.
    The type of this attribute will be either a `RegGprO32`, `RegGprN32` or a `RegGprN64` depending on the current `config.regNames_gprAbiNames` value.
    If the current instruction does not use the `ft` register, then a Runtime exception will be raised.
    Read-only."""
    fd: Enum
    """The value of the `fd` register for this instruction.
    The type of this attribute will be either a `RegGprO32`, `RegGprN32` or a `RegGprN64` depending on the current `config.regNames_gprAbiNames` value.
    If the current instruction does not use the `fd` register, then a Runtime exception will be raised.
    Read-only."""

    uniqueId: Enum
    """An unique identificator for the opcode of this instruction.
    The type is an `InstrId` enum.
    Read-only."""

    instrIdType: Enum
    """An identificator for the general type for the opcode of this instruction.
    The type is an `InstrIdType` enum.
    Read-only."""

    vram: int = 0
    """The vram (virtual ram) address for this instruction"""
    inHandwrittenFunction: bool = False
    """Boolean value indicating if the current instruction is used on a handwritten function. This is intended to be determined by the user."""

    flag_r5900DisasmAsData: Enum = TrinaryValue.NONE
    """Flag to override the r5900DisasmAsData global configuration.

    - This flag allows to fine-tune R5900 instruction set that are affected by the global `gnuMode` option.
        - Currently these instructions are: `trunc.w.s` (r5900 mode), `cvt.w.s` (r5900 mode), `vclipw` and `vsqrt`.

    - `TrinaryValue.TRUE` forces the instruction to be disassembled as data.
    - `TrinaryValue.FALSE` bypasses the global checks for disassembling a word as data. A word will still be disassembled as data if it can't be decoded.
    - `TrinaryValue.NONE` leaves this decision to the global settings.
    """
    flag_r5900UseDollar: Enum = TrinaryValue.NONE
    """Flag to override the disasmAsData global configuration.

    - `TrinaryValue.TRUE` forces the use of dollar signs ($) on R5900's VU instructions.
    - `TrinaryValue.FALSE` forces disassembling to not use of dollar signs ($) on R5900's VU instructions.
    - `TrinaryValue.NONE` leaves this decision to the global settings.
    """


    def __init__(self, word: int, vram: int=0, category: Enum=InstrCategory.CPU) -> None:
        """Decode an Instruction encoded as the 4 bytes `word`, located at `vram`.

        `vram` is used to decode jump instructions that use the PC value to get the upper bits of the target address.
        """

    def getRaw(self) -> int:
        """Get the word value encoding the instruction"""
    def getImmediate(self) -> int: #! deprecated
        """Use `getProcessedImmediate()` instead"""
    def getProcessedImmediate(self) -> int:
        """Get the (possibly signed) immediate value for this instruction.

        This only makes sense for an instruction with an immediate,
        which can be checked with `hasOperandAlias(OperandType.cpu_immediate)`

        An exception will be raised if the instruction does not contain an immediate field.
        """
    def getInstrIndexAsVram(self) -> int:
        """Get the target vram address this instruction jumps to.

        This only makes sense if the instruction is a jump,
        which can be checked with `instr.isJumpWithAddress()`

        An exception will be raised if the instruction is not a jump instruction.
        """
    def getBranchOffset(self) -> int:
        """Returns the offset (in bytes) that the branch instruction would branch,
        relative to the instruction itself.

        The returned value can be negative, meaning the branch instructions does
        a backwards branch.

        This only makes sense for an instruction is a branch,
        which can be checked with `instr.isBranch()`

        An exception will be raised if the instruction is not a branch instruction.
        """
    def getGenericBranchOffset(self, currentVram: int) -> int: #! deprecated
        """Use `getBranchOffsetGeneric()` instead"""
    def getBranchOffsetGeneric(self) -> int: ...
    def getBranchVramGeneric(self) -> int: ...
    def getDestinationGpr(self) -> Enum|None: ...
    def outputsToGprZero(self) -> bool: ...
    def getOpcodeName(self) -> str: ...

    def blankOut(self) -> None: ...

    def isImplemented(self) -> bool: ...
    def isLikelyHandwritten(self) -> bool: ...
    def isNop(self) -> bool: ...
    def isUnconditionalBranch(self) -> bool: ...

    def isReturn(self) -> bool: ...
    def isJumptableJump(self) -> bool: ...

    def isJrRa(self) -> bool: ... #! deprecated
    def isJrNotRa(self) -> bool: ... #! deprecated

    def hasDelaySlot(self) -> bool: ...
    def mapInstrToType(self) -> str|None: ... #! deprecated

    def sameOpcode(self, other: Instruction) -> bool: ...
    def sameOpcodeButDifferentArguments(self, other: Instruction) -> bool: ...

    def hasOperand(self, operand: Enum) -> bool:
        """Check if the instruction has specifically the `operand`.
        `operand` should be from the `OperandType` enum.
        """
    def hasOperandAlias(self, operand: Enum) -> bool:
        """Check if the instruction has the `operand` or an alias of it.
        (if unsure whether to use `hasOperand` or `hasOperandAlias`, use `hasOperandAlias`)
        `operand` should be from the `OperandType` enum.
        """

    def isValid(self) -> bool: ...

    #! deprecated
    def isUnknownType(self) -> bool: ...
    #! deprecated
    def isJType(self) -> bool:
        """Use `isJumpWithAddress()` instead"""
    #! deprecated
    def isIType(self) -> bool: ...
    #! deprecated
    def isRType(self) -> bool: ...
    #! deprecated
    def isRegimmType(self) -> bool:
        """Use `hasOperandAlias(OperandType.cpu_immediate)` instead"""

    def isBranch(self) -> bool: ...
    def isBranchLikely(self) -> bool: ...
    def isJump(self) -> bool: ...
    def isJumpWithAddress(self) -> bool: ...
    def isTrap(self) -> bool: ...
    def isFloat(self) -> bool: ...
    def isDouble(self) -> bool: ...
    def isUnsigned(self) -> bool: ...
    def modifiesRs(self) -> bool: ...
    def modifiesRt(self) -> bool: ...
    def modifiesRd(self) -> bool: ...
    def readsRs(self) -> bool: ...
    def readsRt(self) -> bool: ...
    def readsRd(self) -> bool: ...
    def readsHI(self) -> bool: ...
    def readsLO(self) -> bool: ...
    def modifiesHI(self) -> bool: ...
    def modifiesLO(self) -> bool: ...
    def modifiesFs(self) -> bool: ...
    def modifiesFt(self) -> bool: ...
    def modifiesFd(self) -> bool: ...
    def readsFs(self) -> bool: ...
    def readsFt(self) -> bool: ...
    def readsFd(self) -> bool: ...
    def notEmitedByCompilers(self) -> bool: ... #! deprecated
    def notEmittedByCompilers(self) -> bool: ...
    def canBeHi(self) -> bool: ...
    def canBeLo(self) -> bool: ...
    def doesLink(self) -> bool: ...
    def doesDereference(self) -> bool: ...
    def doesLoad(self) -> bool: ...
    def doesStore(self) -> bool: ...
    def maybeIsMove(self) -> bool: ...
    def isPseudo(self) -> bool: ...
    def getAccessType(self) -> Enum: ...
    def doesUnsignedMemoryAccess(self) -> bool: ...

    def disassemble(self, immOverride: str|None=None, extraLJust: int=0) -> str:
        """Returns a string that can be assembled back to the instruction raw word.
        `immOverride` can be a string that replaces the immediate in the disassembly,
        or the jump target, if any. If the instruction has neither, it is ignored.
        Examples:
        >>> Instruction(0x3C0A0042).disassemble()
        'lui         $t2, 0x42'
        >>> Instruction(0x3C0A0042).disassemble("hex_answer")
        'lui         $t2, hex_answer'
        >>> Instruction(0x0C000042).disassemble()
        'jal         func_80000108'
        >>> Instruction(0x0C000042).disassemble("my_target")
        'jal         my_target'
        """

    def __reduce__(self) -> tuple: ...

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
