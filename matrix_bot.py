

import asyncio
from nio import (AsyncClient, RoomMessageText)
from datetime import datetime;
#
from modules.pendu_bot.pendu_bot import pendu_bot ;


class element_Bot(object):

    def __init__(self, host, login, gaming_room):
        self.gaming_id = None;
        self.client = AsyncClient(host, login);
        self.gaming_room = gaming_room;
        self.toggle = False;
        self.login = login.split(":")[0];
        self.module_array = [];

    async def send_message(self, message):
        await self.client.room_send(
            room_id=self.gaming_id,
            message_type="m.room.message",
            content = {
                "msgtype": "m.text",
                "body": message
            }
        ) ;

    async def connect(self, password):
        await self.client.login(password);
        gaming_id_tmp = await self.client.join(self.gaming_room);
        self.gaming_id = gaming_id_tmp.room_id;
        self.client.add_event_callback(self.message_cb, RoomMessageText);
        self.is_running = True;


    async def start_listening(self, msg=None):
        if msg:
            await self.send_message(msg);
        self.launch_at = datetime.now();
        self.is_running = True ;
        while(self.is_running):
            await asyncio.gather(self.client.sync(timeout=30000));
    #
    async def message_cb(self, room, event):
        # On ignore les messages pendant 5 secondes ...
        if not(self.toggle):
            now = datetime.now();
            if (now-self.launch_at).seconds > 2:
                self.toggle = True;
        if (self.toggle and event.sender != self.login and room.room_id == self.gaming_id):
            msg = event.body;
            await self.parse_msg(msg);

    #
    async def parse_msg(self, msg):
        answer_array = [];
        loop = asyncio.get_event_loop();
        for module in self.module_array:
            print(module)
            tmp_answer = await loop.run_in_executor(None, module.process_msg_active, msg);
            print(tmp_answer);
            if tmp_answer:
                answer_array.append(tmp_answer);
            tmp_answer = await loop.run_in_executor(None, module.process_msg_passive, msg);
            if tmp_answer:
                answer_array.append(tmp_answer);
        if answer_array:
            for answer in answer_array:
                await self.send_message(answer);
    #
    def add_module(self, module):
        if not(module in self.module_array):
            self.module_array.append(module);

async def main():
    host = "https://mandragot.org";
    login = "@tersa_bot:mandragot.org";
    gaming_room = "#papotage_gaming_unlock:mandragot.org";
    element_Bot_instance = element_Bot(host, login, gaming_room);
    #
    my_pendu = pendu_bot(); element_Bot_instance.add_module(my_pendu);
    #
    await element_Bot_instance.connect("blaireaux35");
    await element_Bot_instance.start_listening("Hello, I'm Tbot!");


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
