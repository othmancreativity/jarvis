"""
JARVIS 4.5 — Google Services Agent
====================================
Unified interface to all Google services with REAL HTTP API calls.
Handles: YouTube, Drive, Gmail, Calendar, Docs, Sheets, Slides, Tasks, Contacts, Translate.
"""

from __future__ import annotations

import logging
import json
from typing import Any
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage
from config import config

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

logger = logging.getLogger("jarvis.agents.google")


class GoogleAgent(BaseAgent):
    """
    Google Agent: Production-ready interface to all Google services.
    Uses Google API Key + OAuth access tokens for authentication.
    """

    def __init__(self):
        super().__init__(
            agent_id="google",
            name="Google Services Agent",
            description="Unified Google services interface with real API calls",
        )
        self.register_capability("youtube_search")
        self.register_capability("drive_list")
        self.register_capability("drive_search")
        self.register_capability("gmail_search")
        self.register_capability("gmail_read")
        self.register_capability("calendar_list")
        self.register_capability("calendar_create")
        self.register_capability("translate")
        self.register_capability("contacts_list")
        self.register_capability("contacts_search")
        self.register_capability("docs_create")
        self.register_capability("docs_read")
        self.register_capability("sheets_read")
        self.register_capability("sheets_write")
        self.register_capability("sheets_create")
        self.register_capability("tasks_list")
        self.register_capability("tasks_create")
        self.register_capability("slides_create")

    def _get_headers(self) -> dict:
        """Build auth headers."""
        headers = {"Content-Type": "application/json"}
        if config.google_access_token:
            headers["Authorization"] = f"Bearer {config.google_access_token}"
        elif config.google_api_key:
            headers["X-Goog-Api-Key"] = config.google_api_key
        return headers

    def _api_key_param(self) -> str:
        """Get API key query parameter."""
        return f"key={config.google_api_key}" if config.google_api_key else ""

    async def handle_command(self, message: AgentMessage) -> None:
        """Handle Google service commands with real API calls."""
        payload = message.payload
        service = payload.get("service", "")
        action = payload.get("action", "")

        try:
            handler_name = f"_{service}_{action}" if service else f"_{payload.get('command', '')}"
            handler = getattr(self, handler_name, None)

            if handler:
                result = await handler(payload)
            else:
                # Try intent-based routing
                result = await self._handle_intent(payload)

            await self.send_response(message.sender, result, message.correlation_id)

        except Exception as e:
            logger.error(f"Google agent error [{service}/{action}]: {e}")
            await self.send_response(
                message.sender,
                {"status": "error", "error": str(e)},
                message.correlation_id,
            )

    async def _handle_intent(self, payload: dict) -> dict:
        """Route by command name if service/action not specified."""
        command = payload.get("command", "")
        routing = {
            "youtube": self._youtube_search,
            "gmail_search": self._gmail_search,
            "gmail_read": self._gmail_read,
            "drive_list": self._drive_list,
            "drive_search": self._drive_search,
            "calendar_list": self._calendar_list,
            "calendar_create": self._calendar_create,
            "translate": self._translate,
            "contacts_list": self._contacts_list,
            "contacts_search": self._contacts_search,
            "docs_create": self._docs_create,
            "docs_read": self._docs_read,
            "sheets_read": self._sheets_read,
            "sheets_write": self._sheets_write,
            "sheets_create": self._sheets_create,
            "tasks_list": self._tasks_list,
            "tasks_create": self._tasks_create,
            "slides_create": self._slides_create,
        }
        handler = routing.get(command)
        if handler:
            return await handler(payload)
        return {"status": "error", "error": f"Unknown Google command: {command}"}

    # ── YouTube ──────────────────────────────────────────────────────────

    async def _youtube_search(self, params: dict) -> dict:
        api_key = config.google_api_key
        if not api_key:
            return {"status": "error", "error": "GOOGLE_API_KEY not configured"}

        query = params.get("query", params.get("q", ""))
        max_results = min(params.get("max_results", 5), 50)

        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            r = requests.get(url, params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "key": api_key,
            }, timeout=15)
            r.raise_for_status()
            data = r.json()

            videos = []
            for item in data.get("items", []):
                snip = item.get("snippet", {})
                videos.append({
                    "title": snip.get("title", ""),
                    "channel": snip.get("channelTitle", ""),
                    "video_id": item.get("id", {}).get("videoId", ""),
                    "url": f"https://youtube.com/watch?v={item.get('id', {}).get('videoId', '')}",
                    "published": snip.get("publishedAt", ""),
                })

            return {"status": "success", "videos": videos, "count": len(videos),
                    "responseText": self._format_youtube_results(videos)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _format_youtube_results(self, videos: list) -> str:
        if not videos:
            return "No videos found."
        lines = [f"Found {len(videos)} video(s):"]
        for v in videos[:5]:
            lines.append(f"\n📺 {v['title']}\n   Channel: {v['channel']}\n   {v['url']}")
        return "\n".join(lines)

    # ── Drive ────────────────────────────────────────────────────────────

    async def _drive_list(self, params: dict) -> dict:
        if not HAS_REQUESTS:
            return {"status": "error", "error": "requests library not installed"}

        try:
            headers = self._get_headers()
            page_size = min(params.get("page_size", 10), 100)
            url = "https://www.googleapis.com/drive/v3/files"
            r = requests.get(url, headers=headers, params={
                "pageSize": page_size,
                "fields": "files(id,name,mimeType,modifiedTime,size)",
                "orderBy": "modifiedTime desc",
            }, timeout=15)
            r.raise_for_status()
            data = r.json()
            files = data.get("files", [])
            return {"status": "success", "files": files, "count": len(files),
                    "responseText": self._format_drive_results(files)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _drive_search(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            query_str = params.get("query", params.get("q", ""))
            url = "https://www.googleapis.com/drive/v3/files"
            r = requests.get(url, headers=headers, params={
                "pageSize": min(params.get("max_results", 10), 100),
                "q": f"name contains '{query_str}'",
                "fields": "files(id,name,mimeType,modifiedTime)",
            }, timeout=15)
            r.raise_for_status()
            files = r.json().get("files", [])
            return {"status": "success", "files": files, "count": len(files),
                    "responseText": self._format_drive_results(files)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _format_drive_results(self, files: list) -> str:
        if not files:
            return "No files found in Google Drive."
        lines = [f"Found {len(files)} file(s):"]
        for f in files[:10]:
            size = f.get("size", "—")
            lines.append(f"\n📄 {f['name']} ({f.get('mimeType', 'unknown')})")
        return "\n".join(lines)

    # ── Gmail ────────────────────────────────────────────────────────────

    async def _gmail_search(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            q = params.get("q", params.get("query", ""))
            url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
            r = requests.get(url, headers=headers, params={
                "maxResults": min(params.get("max_results", 10), 50),
                "q": q,
            }, timeout=15)
            r.raise_for_status()
            msgs = r.json().get("messages", [])

            # Fetch details for each message
            results = []
            for m in msgs[:5]:
                try:
                    detail = requests.get(
                        f"{url}/{m['id']}",
                        headers=headers,
                        params={"format": "metadata", "metadataHeaders": "Subject,From,Date"},
                        timeout=10,
                    ).json()
                    headers_list = detail.get("payload", {}).get("headers", [])
                    info = {h["name"]: h["value"] for h in headers_list}
                    results.append({
                        "id": m["id"],
                        "subject": info.get("Subject", "(no subject)"),
                        "from": info.get("From", ""),
                        "date": info.get("Date", ""),
                    })
                except Exception:
                    results.append({"id": m["id"], "subject": "(unable to fetch)"})

            return {"status": "success", "messages": results, "count": len(results),
                    "responseText": self._format_gmail_results(results)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _gmail_read(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            msg_id = params.get("message_id", params.get("id", ""))
            url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}"
            r = requests.get(url, headers=headers, params={
                "format": "full",
            }, timeout=15)
            r.raise_for_status()
            data = r.json()
            headers_list = data.get("payload", {}).get("headers", [])
            info = {h["name"]: h["value"] for h in headers_list}
            return {"status": "success", "subject": info.get("Subject"), "from": info.get("From"),
                    "date": info.get("Date"), "responseText": f"📧 {info.get('Subject', 'No Subject')}\nFrom: {info.get('From', '')}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _format_gmail_results(self, messages: list) -> str:
        if not messages:
            return "No emails found."
        lines = [f"Found {len(messages)} email(s):"]
        for m in messages:
            lines.append(f"\n📧 {m.get('subject', 'No Subject')}\n   From: {m.get('from', 'Unknown')}")
        return "\n".join(lines)

    # ── Calendar ─────────────────────────────────────────────────────────

    async def _calendar_list(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            calendar_id = params.get("calendar_id", "primary")
            url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
            from datetime import datetime, timedelta
            now = datetime.utcnow().isoformat() + "Z"
            week_later = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"

            r = requests.get(url, headers=headers, params={
                "maxResults": min(params.get("max_results", 10), 50),
                "timeMin": params.get("time_min", now),
                "timeMax": params.get("time_max", week_later),
                "orderBy": "startTime",
                "singleEvents": "true",
            }, timeout=15)
            r.raise_for_status()
            events = r.json().get("items", [])

            results = []
            for e in events:
                start = e.get("start", {})
                start_time = start.get("dateTime", start.get("date", ""))
                results.append({
                    "summary": e.get("summary", "(no title)"),
                    "start": start_time,
                    "location": e.get("location", ""),
                })

            return {"status": "success", "events": results, "count": len(results),
                    "responseText": self._format_calendar_results(results)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _calendar_create(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            calendar_id = params.get("calendar_id", "primary")
            url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
            body = {
                "summary": params.get("summary", "New Event"),
                "start": {"dateTime": params.get("start_time"), "timeZone": params.get("timezone", "UTC")},
                "end": {"dateTime": params.get("end_time"), "timeZone": params.get("timezone", "UTC")},
            }
            if params.get("location"):
                body["location"] = params["location"]
            if params.get("description"):
                body["description"] = params["description"]

            r = requests.post(url, headers=headers, json=body, timeout=15)
            r.raise_for_status()
            data = r.json()
            return {"status": "success", "event_id": data.get("id"),
                    "html_link": data.get("htmlLink"),
                    "responseText": f"✅ Event created: {data.get('summary')}\n{data.get('htmlLink', '')}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _format_calendar_results(self, events: list) -> str:
        if not events:
            return "No upcoming events found."
        lines = [f"Found {len(events)} event(s):"]
        for e in events:
            lines.append(f"\n📅 {e['summary']}\n   Start: {e['start']}")
            if e.get("location"):
                lines.append(f"   Location: {e['location']}")
        return "\n".join(lines)

    # ── Translate ────────────────────────────────────────────────────────

    async def _translate(self, params: dict) -> dict:
        api_key = config.google_api_key
        if not api_key:
            return {"status": "error", "error": "GOOGLE_API_KEY not configured for translation"}

        try:
            url = "https://translation.googleapis.com/language/translate/v2"
            r = requests.post(url, params={"key": api_key}, json={
                "q": params.get("text", ""),
                "target": params.get("target_language", "en"),
                "source": params.get("source_language", ""),
                "format": "text",
            }, timeout=10)
            r.raise_for_status()
            data = r.json()
            result = data.get("data", {}).get("translations", [{}])[0]

            return {
                "status": "success",
                "translated_text": result.get("translatedText", ""),
                "detected_source": result.get("detectedSourceLanguage", ""),
                "responseText": f"🌐 Translation:\n{result.get('translatedText', '')}",
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ── Contacts ─────────────────────────────────────────────────────────

    async def _contacts_list(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            url = "https://people.googleapis.com/v1/people/me/connections"
            r = requests.get(url, headers=headers, params={
                "pageSize": min(params.get("page_size", 10), 100),
                "personFields": "names,emailAddresses,phoneNumbers",
            }, timeout=15)
            r.raise_for_status()
            connections = r.json().get("connections", [])

            results = []
            for c in connections:
                names = c.get("names", [{}])
                emails = c.get("emailAddresses", [{}])
                phones = c.get("phoneNumbers", [{}])
                results.append({
                    "name": names[0].get("displayName", "") if names else "",
                    "email": emails[0].get("value", "") if emails else "",
                    "phone": phones[0].get("value", "") if phones else "",
                })

            return {"status": "success", "contacts": results, "count": len(results),
                    "responseText": self._format_contacts_results(results)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _contacts_search(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            url = "https://people.googleapis.com/v1/people:searchContacts"
            r = requests.get(url, headers=headers, params={
                "query": params.get("query", ""),
                "pageSize": 10,
                "readMask": "names,emailAddresses,phoneNumbers",
            }, timeout=15)
            r.raise_for_status()
            results = r.json().get("results", [])
            contacts = []
            for rslt in results:
                person = rslt.get("person", {})
                names = person.get("names", [{}])
                emails = person.get("emailAddresses", [{}])
                contacts.append({
                    "name": names[0].get("displayName", "") if names else "",
                    "email": emails[0].get("value", "") if emails else "",
                })
            return {"status": "success", "contacts": contacts, "count": len(contacts),
                    "responseText": self._format_contacts_results(contacts)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _format_contacts_results(self, contacts: list) -> str:
        if not contacts:
            return "No contacts found."
        lines = [f"Found {len(contacts)} contact(s):"]
        for c in contacts:
            lines.append(f"\n👤 {c.get('name', 'Unknown')}\n   📧 {c.get('email', '—')}")
        return "\n".join(lines)

    # ── Docs ─────────────────────────────────────────────────────────────

    async def _docs_create(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            url = "https://docs.googleapis.com/v1/documents"
            r = requests.post(url, headers=headers, json={
                "title": params.get("title", "Untitled Document"),
            }, timeout=15)
            r.raise_for_status()
            data = r.json()
            return {"status": "success", "document_id": data.get("documentId"),
                    "title": data.get("title"),
                    "url": f"https://docs.google.com/document/d/{data.get('documentId')}/edit",
                    "responseText": f"📝 Document created: {data.get('title')}\nhttps://docs.google.com/document/d/{data.get('documentId')}/edit"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _docs_read(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            doc_id = params.get("document_id", params.get("id", ""))
            url = f"https://docs.googleapis.com/v1/documents/{doc_id}"
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            data = r.json()
            return {"status": "success", "title": data.get("title"),
                    "responseText": f"📝 {data.get('title')}\n(Document has {len(data.get('body', {}).get('content', []))} content elements)"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ── Sheets ───────────────────────────────────────────────────────────

    async def _sheets_read(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            spreadsheet_id = params.get("spreadsheet_id", params.get("id", ""))
            range_name = params.get("range", "Sheet1!A1:C10")
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}"
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            data = r.json()
            values = data.get("values", [])
            return {"status": "success", "values": values, "range": data.get("range"),
                    "responseText": self._format_sheet_values(values)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _sheets_write(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            spreadsheet_id = params.get("spreadsheet_id", params.get("id", ""))
            range_name = params.get("range", "Sheet1!A1")
            values = params.get("values", [[]])
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}"
            r = requests.put(url, headers=headers, params={"valueInputOption": "RAW"}, json={
                "values": values,
            }, timeout=15)
            r.raise_for_status()
            data = r.json()
            return {"status": "success", "updated_cells": data.get("updatedCells", 0),
                    "responseText": f"✅ Updated {data.get('updatedCells', 0)} cells"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _sheets_create(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            url = "https://sheets.googleapis.com/v4/spreadsheets"
            r = requests.post(url, headers=headers, json={
                "properties": {"title": params.get("title", "New Spreadsheet")},
            }, timeout=15)
            r.raise_for_status()
            data = r.json()
            return {"status": "success", "spreadsheet_id": data.get("spreadsheetId"),
                    "url": data.get("spreadsheetUrl"),
                    "responseText": f"📊 Spreadsheet created: {data.get('properties', {}).get('title')}\n{data.get('spreadsheetUrl', '')}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _format_sheet_values(self, values: list) -> str:
        if not values:
            return "Sheet is empty."
        lines = ["📊 Sheet data:"]
        for row in values[:20]:
            lines.append(" | ".join(str(c) for c in row))
        if len(values) > 20:
            lines.append(f"... ({len(values) - 20} more rows)")
        return "\n".join(lines)

    # ── Tasks ────────────────────────────────────────────────────────────

    async def _tasks_list(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            tasklist_id = params.get("tasklist_id", "@default")
            url = f"https://tasks.googleapis.com/tasks/v1/lists/{tasklist_id}/tasks"
            r = requests.get(url, headers=headers, params={
                "showCompleted": str(params.get("show_completed", True)).lower(),
                "maxResults": 20,
            }, timeout=15)
            r.raise_for_status()
            items = r.json().get("items", [])

            results = []
            for t in items:
                results.append({
                    "title": t.get("title", ""),
                    "completed": t.get("status") == "completed",
                    "due": t.get("due", ""),
                })

            return {"status": "success", "tasks": results, "count": len(results),
                    "responseText": self._format_tasks_results(results)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _tasks_create(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            tasklist_id = params.get("tasklist_id", "@default")
            url = f"https://tasks.googleapis.com/tasks/v1/lists/{tasklist_id}/tasks"
            body = {"title": params.get("title", "New Task")}
            if params.get("due"):
                body["due"] = params["due"]
            if params.get("notes"):
                body["notes"] = params["notes"]

            r = requests.post(url, headers=headers, json=body, timeout=15)
            r.raise_for_status()
            data = r.json()
            return {"status": "success", "task_id": data.get("id"),
                    "responseText": f"✅ Task created: {data.get('title')}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _format_tasks_results(self, tasks: list) -> str:
        if not tasks:
            return "No tasks found."
        lines = [f"Found {len(tasks)} task(s):"]
        for t in tasks:
            status = "✅" if t.get("completed") else "⬜"
            lines.append(f"\n{status} {t.get('title', '')}")
            if t.get("due"):
                lines.append(f"   Due: {t['due']}")
        return "\n".join(lines)

    # ── Slides ───────────────────────────────────────────────────────────

    async def _slides_create(self, params: dict) -> dict:
        try:
            headers = self._get_headers()
            url = "https://slides.googleapis.com/v1/presentations"
            r = requests.post(url, headers=headers, json={
                "title": params.get("title", "Untitled Presentation"),
            }, timeout=15)
            r.raise_for_status()
            data = r.json()
            return {"status": "success", "presentation_id": data.get("presentationId"),
                    "url": f"https://docs.google.com/presentation/d/{data.get('presentationId')}/edit",
                    "responseText": f"🎬 Presentation created: {data.get('title')}\nhttps://docs.google.com/presentation/d/{data.get('presentationId')}/edit"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
