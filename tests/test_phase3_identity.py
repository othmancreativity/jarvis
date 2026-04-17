"""Phase 3 tests: Identity system (Jarvis profile, prompt builder, model awareness)."""

from __future__ import annotations

import pytest


class TestJarvisIdentity:
    def test_load_identity(self):
        from core.identity.jarvis_profile import load_jarvis_identity

        identity = load_jarvis_identity()
        assert identity.name == "Jarvis"
        assert identity.role != ""
        assert len(identity.capabilities) > 0

    def test_identity_block(self):
        from core.identity.jarvis_profile import load_jarvis_identity

        identity = load_jarvis_identity()
        block = identity.identity_block()
        assert "Jarvis" in block
        assert len(block) > 50

    def test_safety_block(self):
        from core.identity.jarvis_profile import load_jarvis_identity

        identity = load_jarvis_identity()
        safety = identity.safety_block()
        assert "Safety" in safety or len(safety) == 0

    def test_framing_block(self):
        from core.identity.jarvis_profile import load_jarvis_identity

        identity = load_jarvis_identity()
        framing = identity.framing_block()
        assert "component" in framing.lower() or len(framing) == 0


class TestIdentityUserProfile:
    def test_from_dict(self):
        from core.identity.user_profile import IdentityUserProfile

        profile = IdentityUserProfile({
            "display_name": "Othman",
            "preferred_language": "ar",
            "response_style": "detailed",
            "formality": "formal",
            "technical_level": "expert",
        })
        assert profile.display_name == "Othman"
        assert profile.language == "ar"
        assert profile.style == "detailed"

    def test_prompt_fragment(self):
        from core.identity.user_profile import IdentityUserProfile

        profile = IdentityUserProfile({"display_name": "Othman"})
        fragment = profile.prompt_fragment()
        assert "Othman" in fragment
        assert "User profile:" in fragment

    def test_from_memory_profile(self, tmp_path):
        from core.memory.user_profile import UserProfile
        from core.identity.user_profile import IdentityUserProfile

        mem_profile = UserProfile(user_id="test", profiles_dir=tmp_path)
        id_profile = IdentityUserProfile.from_memory_profile(mem_profile)
        assert id_profile.language == "ar"


class TestModelAwareness:
    def test_identity_context(self):
        from core.identity.jarvis_profile import load_jarvis_identity
        from core.identity.model_awareness import ModelAwarenessLayer

        identity = load_jarvis_identity()
        awareness = ModelAwarenessLayer(identity)
        ctx = awareness.identity_context()
        assert "Jarvis" in ctx
        assert "User profile:" in ctx

    def test_system_context(self):
        from core.identity.jarvis_profile import JarvisIdentity
        from core.identity.model_awareness import ModelAwarenessLayer

        awareness = ModelAwarenessLayer(JarvisIdentity())
        summary = awareness.system_context_summary()
        assert "runtime" in summary.lower()


class TestSystemPromptBuilder:
    def test_build_default(self):
        from core.identity.jarvis_profile import load_jarvis_identity
        from core.identity.model_awareness import ModelAwarenessLayer
        from core.identity.prompt_builder import SystemPromptBuilder

        identity = load_jarvis_identity()
        awareness = ModelAwarenessLayer(identity)
        builder = SystemPromptBuilder(awareness)

        prompt = builder.build(mode="normal", language="ar")
        assert "Jarvis" in prompt
        assert "NORMAL" in prompt
        assert "Arabic" in prompt

    def test_build_with_context(self):
        from core.identity.jarvis_profile import load_jarvis_identity
        from core.identity.model_awareness import ModelAwarenessLayer
        from core.identity.prompt_builder import SystemPromptBuilder

        identity = load_jarvis_identity()
        awareness = ModelAwarenessLayer(identity)
        builder = SystemPromptBuilder(awareness)

        prompt = builder.build(
            mode="deep",
            language="en",
            task_context="User uploaded a PDF document",
            memory_snippet="User prefers code examples",
        )
        assert "DEEP" in prompt
        assert "PDF" in prompt
        assert "code examples" in prompt

    def test_all_modes(self):
        from core.identity.jarvis_profile import JarvisIdentity
        from core.identity.model_awareness import ModelAwarenessLayer
        from core.identity.prompt_builder import SystemPromptBuilder

        awareness = ModelAwarenessLayer(JarvisIdentity())
        builder = SystemPromptBuilder(awareness)

        for mode in ("fast", "normal", "deep", "planning", "research"):
            prompt = builder.build(mode=mode, language="en")
            assert mode.upper() in prompt

    def test_deterministic_ordering(self):
        from core.identity.jarvis_profile import load_jarvis_identity
        from core.identity.model_awareness import ModelAwarenessLayer
        from core.identity.prompt_builder import SystemPromptBuilder

        identity = load_jarvis_identity()
        awareness = ModelAwarenessLayer(identity)
        builder = SystemPromptBuilder(awareness)

        p1 = builder.build(mode="normal", language="ar")
        p2 = builder.build(mode="normal", language="ar")
        assert p1 == p2  # deterministic


class TestSystemAwareness:
    def test_environment_summary(self):
        from core.identity.system_awareness import SystemAwareness

        sa = SystemAwareness()
        summary = sa.environment_summary()
        assert "Python" in summary

    def test_tools_summary(self):
        from core.identity.system_awareness import SystemAwareness

        sa = SystemAwareness()
        summary = sa.tools_summary(["web_search", "file_ops"])
        assert "web_search" in summary

    def test_no_secrets_in_project_summary(self):
        from core.identity.system_awareness import SystemAwareness

        sa = SystemAwareness()
        summary = sa.project_summary(max_depth=1)
        assert ".env" not in summary
        assert ".git" not in summary
