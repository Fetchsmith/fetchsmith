#!/root/agent/venv/bin/python
"""Minimal inbound SMTP server for *@fetchsmith.com. Stores each message as JSON in /root/agent/mail/inbox."""
import asyncio, json, os, time, email, email.policy, uuid
from aiosmtpd.controller import Controller
INBOX = "/root/agent/mail/inbox"
DOMAINS = {"fetchsmith.com"}
class Handler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if address.split("@")[-1].lower() not in DOMAINS:
            return "550 not relaying"
        envelope.rcpt_tos.append(address); return "250 OK"
    async def handle_DATA(self, server, session, envelope):
        msg = email.message_from_bytes(envelope.content, policy=email.policy.default)
        body = msg.get_body(preferencelist=("plain","html"))
        rec = {"id": uuid.uuid4().hex, "ts": int(time.time()), "from": envelope.mail_from,
               "to": envelope.rcpt_tos, "subject": msg.get("subject",""),
               "text": body.get_content() if body else "", "peer": session.peer[0]}
        os.makedirs(INBOX, exist_ok=True)
        with open(f"{INBOX}/{rec['ts']}-{rec['id']}.json","w") as f: json.dump(rec, f)
        return "250 Message accepted"
if __name__ == "__main__":
    c = Controller(Handler(), hostname="0.0.0.0", port=25); c.start()
    try:
        while True: time.sleep(3600)
    except KeyboardInterrupt: c.stop()
