# events/dispatcher.py
# Event signals — kept for future Django signal-based integrations.
# The primary event mechanism is the Outbox pattern via events.publishers.
from django.dispatch import Signal

lead_created = Signal()
content_published = Signal()
ai_decision_made = Signal()
