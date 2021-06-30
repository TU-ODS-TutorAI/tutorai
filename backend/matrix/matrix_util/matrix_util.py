def get_body(json):
    return json["content"]["body"]


def get_sender(json):
    return json["sender"]


def get_type(json):
    return json["type"]


def get_msgtype(json):
    return json["content"]["msgtype"]


def valid_text_msg(json):
    return (json["type"] == "m.room.message" and json["content"]["msgtype"] == "m.text" and "m.relates_to" not in json[
        "content"])


async def send_text_reply(self, room_id, message, event_id):
    await self.async_client.room_send(room_id=room_id,
                                      message_type="m.room.message",
                                      content={
                                          "msgtype": "m.text",
                                          "body": message,
                                          "m.relates_to": {
                                              "m.in_reply_to": {
                                                  "event_id": event_id
                                              }
                                          }
                                      })


async def send_notice_reply(self, room_id, message, event_id):
    await self.async_client.room_send(room_id=room_id,
                                      message_type="m.room.message",
                                      content={
                                          "msgtype": "m.notice",
                                          "body": message,
                                          "m.relates_to": {
                                              "m.in_reply_to": {
                                                  "event_id": event_id
                                              }
                                          }
                                      })


async def send_notice_message(self, room_id, message):
    await self.async_client.room_send(room_id=room_id,
                                      message_type="m.room.message",
                                      content={
                                          "msgtype": "m.notice",
                                          "body": message
                                      })
