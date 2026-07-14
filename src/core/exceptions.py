"""
Custom exceptions used throughout ProfitPilot.

Having project-specific exceptions makes debugging easier
and allows higher-level modules to handle errors cleanly.
"""


class ProfitPilotError(Exception):
    """
    Base class for all ProfitPilot exceptions.
    """

    pass


# ------------------------------------------------------------------ #
# Excel Engine Exceptions
# ------------------------------------------------------------------ #

class InvalidFileError(ProfitPilotError):
    """
    Raised when an invalid or unsupported file is supplied.
    """

    pass


class FileReadError(ProfitPilotError):
    """
    Raised when a dataset cannot be read.
    """

    pass


class EmptyFileError(ProfitPilotError):
    """
    Raised when the supplied dataset is empty.
    """

    pass


# ------------------------------------------------------------------ #
# Schema Exceptions
# ------------------------------------------------------------------ #

class SchemaExtractionError(ProfitPilotError):
    """
    Raised when schema extraction fails.
    """

    pass


# ------------------------------------------------------------------ #
# Audit Exceptions
# ------------------------------------------------------------------ #

class AuditError(ProfitPilotError):
    """
    Raised when dataset auditing fails.
    """

    pass


# ------------------------------------------------------------------ #
# Business State Exceptions
# ------------------------------------------------------------------ #

class BusinessStateError(ProfitPilotError):
    """
    Raised when BusinessState encounters an invalid operation.
    """

    pass


# ------------------------------------------------------------------ #
# Agent Exceptions
# ------------------------------------------------------------------ #

class AgentExecutionError(ProfitPilotError):
    """
    Raised when an AI agent fails during execution.
    """

    pass


# ------------------------------------------------------------------ #
# LLM Exceptions
# ------------------------------------------------------------------ #

class LLMError(ProfitPilotError):
    """
    Raised when communication with the LLM fails.
    """

    pass