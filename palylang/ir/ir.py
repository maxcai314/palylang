
# The intermediate representation (IR) language for Palylang
# This language uses SSA form for easier optimization and analysis
# Using a 3-address code style for instructions

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union

@dataclass(frozen=True)
class IRType:
    """
    Represents a type in the intermediate representation.
    This dataclass will evolve as we add more features.
    """
    name: str
    size: int  # in bytes


DEFAULT_INT_TYPE = IRType(name='int', size=4)


@dataclass(frozen=True)
class IRVariable:
    """
    Represents a variable in the intermediate representation.
    """
    name: str
    type: IRType


@dataclass(frozen=True)
class IRLiteral:
    """
    Represents a literal value in the intermediate representation.
    """
    value: int
    type: IRType


class Statement(ABC):
    """
    Abstract base class for all IR statements.
    Most statements use the three-address code format.
    3AC Format: result = operand1 op operand2
    """
    @abstractmethod
    def __str__(self) -> str:
        pass


class DirectAssignmentStatement(Statement):
    """
    Represents a direct assignment statement in the IR.
    Example: x = y
    """
    def __init__(self, result: IRVariable, operand: Union[IRVariable, IRLiteral]):
        self.result = result
        self.operand = operand

    def __str__(self) -> str:
        return f"{self.result.name} = {self.operand.name}"


class OperatorAssignmentStatement(Statement):
    """
    Represents an assignment statement in the IR.
    Example: x = y + z
    """
    def __init__(self, result: IRVariable, operand1: Union[IRVariable, IRLiteral], operator: str, operand2: Union[IRVariable, IRLiteral]):
        self.result = result
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2

    def __str__(self) -> str:
        return f"{self.result.name} = {self.operand1.name} {self.operator} {self.operand2.name}"


class PhiAssignmentStatement(Statement):
    """
    Represents a phi-assignment statement in SSA form.
    Example: x = phi(y1, y2)
    """
    def __init__(self, result: IRVariable, operands: list[IRVariable]):
        self.result = result
        self.operands = operands

    def __str__(self) -> str:
        operand_names = ', '.join(op.name for op in self.operands)
        return f"{self.result.name} = phi({operand_names})"

# todo: load/store statements not implemented
# for now, let's compile a side-effect free subset of palylang

class Terminator(ABC):
    """
    Abstract base class for IR code block terminators.
    A terminator can either be a branch, goto, or a return statement.
    """
    @abstractmethod
    def __str__(self) -> str:
        pass


class BasicBlock:
    """
    Represents a basic block in the IR.
    A basic block contains a sequence of statements and ends with a terminator.
    This class is mutable because it may require modifications in order to add phi-nodes.
    """
    def __init__(self, label: str):
        self.label = label
        self.statements: list[Statement] = []
        self.terminator: Union[Terminator, None] = None

    def __str__(self) -> str:
        statements_str = '\n  '.join(str(stmt) for stmt in self.statements)
        terminator_str = str(self.terminator) if self.terminator else ''
        return f"{self.label}:\n  {statements_str}\n  {terminator_str}"


class BranchTerminator(Terminator):
    """
    Represents a branch terminator in the IR.
    Example: br label1, label2
    """
    def __init__(self, branch_cond_var: Union[IRVariable, IRLiteral], true_block: BasicBlock, false_block: BasicBlock):
        self.branch_cond_var = branch_cond_var
        self.true_block = true_block
        self.false_block = false_block

    def __str__(self) -> str:
        return f"br {self.branch_cond_var.name} ? {self.true_block.label} : {self.false_block.label}"


class GotoTerminator(Terminator):
    """
    Represents a goto terminator in the IR.
    Example: goto label
    """
    def __init__(self, target_block: BasicBlock):
        self.target_block = target_block

    def __str__(self) -> str:
        return f"goto {self.target_block.label}"


class ReturnTerminator(Terminator):
    """
    Represents a return terminator in the IR.
    Example: return x
    """
    def __init__(self, return_var: Union[IRVariable, IRLiteral]):
        self.return_var = return_var

    def __str__(self) -> str:
        return f"return {self.return_var.name}"
