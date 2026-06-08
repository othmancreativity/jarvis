"""
JARVIS 4.5 — Security Agent
============================
Monitors all operations for security threats.
Enforces policies, detects anomalies, manages emergency stops.
"""

import logging
from typing import Any
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage, MessageType, message_bus
from security.permissions import permission_engine, PermissionRequest
from security.audit import audit_logger, AuditEventType, SecuritySeverity

logger = logging.getLogger("jarvis.agents.security")


class SecurityAgent(BaseAgent):
    """
    Security Agent: Monitors and enforces security policies.
    Capabilities: threat_detection, anomaly_detection, policy_enforcement,
                  emergency_response, audit_management
    """

    def __init__(self):
        super().__init__(
            agent_id="security",
            name="Security Agent",
            description="Security monitoring and enforcement",
        )
        self.register_capability("threat_detection")
        self.register_capability("anomaly_detection")
        self.register_capability("policy_enforcement")
        self.register_capability("emergency_response")
        self.register_capability("audit_logging")
        self._threat_count = 0
        self._last_threat_time = 0
        self._auto_stop_threshold = 5  # Auto emergency stop after N threats

    async def handle_command(self, message: AgentMessage) -> None:
        """Handle security commands."""
        payload = message.payload
        command = payload.get("command", "")

        if command == "check_permission":
            request = PermissionRequest(
                request_id=payload.get("request_id", ""),
                tool_name=payload.get("tool_name", ""),
                action=payload.get("action", ""),
                target=payload.get("target", ""),
                risk_level=payload.get("risk_level", "medium"),
                permission_level=payload.get("permission_level", "confirm"),
                params=payload.get("params", {}),
                source=payload.get("source", "unknown"),
                user_id=payload.get("user_id", "default"),
            )
            result = permission_engine.check_permission(request)
            await self.send_response(
                message.sender,
                {"decision": result.decision.value, "confirmed": result.confirmed, "reason": result.reason},
                message.correlation_id,
            )

        elif command == "log_event":
            audit_logger.log(
                event_type=AuditEventType(payload.get("event_type", "system_event")),
                action=payload.get("action", ""),
                target=payload.get("target", ""),
                source=payload.get("source", "agent"),
                decision=payload.get("decision", ""),
                result=payload.get("result", ""),
                details=payload.get("details", {}),
                severity=SecuritySeverity(payload.get("severity", "info")),
            )
            await self.send_response(message.sender, {"status": "logged"}, message.correlation_id)

        elif command == "emergency_stop":
            triggered_by = payload.get("triggered_by", "unknown")
            permission_engine.trigger_emergency_stop()
            audit_logger.log_emergency_stop(triggered_by)
            # Broadcast emergency to all agents
            await message_bus.send(AgentMessage(
                sender=self.agent_id,
                recipient="*",
                type=MessageType.BROADCAST,
                payload={"event": "emergency_stop", "triggered_by": triggered_by},
            ))
            await self.send_response(message.sender, {"status": "emergency_stop_activated"}, message.correlation_id)

        elif command == "clear_emergency":
            permission_engine.clear_emergency_stop()
            await self.send_response(message.sender, {"status": "emergency_stop_cleared"}, message.correlation_id)

        elif command == "get_stats":
            stats = permission_engine.get_stats()
            audit_stats = audit_logger.get_stats()
            await self.send_response(
                message.sender,
                {"permissions": stats, "audit": audit_stats, "threats": self._threat_count},
                message.correlation_id,
            )

    async def handle_event(self, message: AgentMessage) -> None:
        """Monitor all events for security threats."""
        # Check for suspicious patterns
        payload = message.payload

        # Count rapid threats
        if payload.get("event") in ("permission_denied", "command_blocked", "error"):
            self._threat_count += 1
            self._last_threat_time = logging._startTime

            if self._threat_count >= self._auto_stop_threshold:
                logger.critical(f"Auto emergency stop triggered: {self._threat_count} threats")
                permission_engine.trigger_emergency_stop()
                audit_logger.log_emergency_stop("auto_threshold")
