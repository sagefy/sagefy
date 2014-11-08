"""
Primary learning sequencer.
"""


def next():
    """
    Main function of the sequencer. Returns what should be displayed next.
    Returns meta information, pointing to one of the following:
    - Specific card.
    - A set tree.
    - Unit selection.
    - Diagnosis overview.
    Also should return progress.
    """
