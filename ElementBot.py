

import asyncio
from nio import (AsyncClient, RoomMessageText)
import datetime;
from src.bcolors import bcolors;
#
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.mastermind.mastermind_bot import mastermind_bot ;
from modules.quotes.quotes import quotes ;

#######################################
# Vraiment Basique pour le moment ;-) #
#######################################

class elementBot(object):
    #
    def __init__(self, host, login, gaming_room):
        self.gaming_id = None;
        self.client = AsyncClient(host, login);
        self.gaming_room = gaming_room;
        self.toggle = False;
        self.login = login;
        self.module_array = [];
        self.launch_at = datetime.datetime.now();
    #
    async def send_message(self, message):
        await self.client.room_send(
            room_id=self.gaming_id,
            message_type="m.room.message",
            content = {
                "msgtype": "m.text",
                "format": "org.matrix.custom.html",
                "body": message,
                "formatted_body": message
            }
        ) ;
    #
    async def connect(self, password):
        await self.client.login(password);
        gaming_id_tmp = await self.client.join(self.gaming_room);
        self.gaming_id = gaming_id_tmp.room_id;
        self.is_running = True;
        self.client.add_event_callback(self.message_cb, RoomMessageText);
    #
    async def start_listening(self, msg=None):
        if msg:
            await self.send_message(msg);
        self.launch_at = datetime.datetime.now();
        self.is_running = True ;
        while(self.is_running):
            await asyncio.gather(self.tick(), self.client.sync(timeout=30000));
    #
    async def message_cb(self, room, event):
        # On ignore les messages pendant 5 secondes ...
        if not(self.toggle):
            if ((datetime.datetime.now()-self.launch_at).seconds > 5):
                self.toggle = True;
        if (self.toggle and event.sender != self.login and room.room_id == self.gaming_id):
            tmp_log = "Event" + bcolors.OKGREEN + " at " + str(datetime.datetime.now())+ bcolors.ENDC + " by "+ bcolors.OKBLUE + event.sender +bcolors.ENDC ;
            print(tmp_log);
            msg = event.body;
            sender = event.sender;
            await self.parse_msg(msg, sender);
    #
    async def parse_msg(self, msg, sender):
        answer_array = [];
        loop = asyncio.get_event_loop();
        for module in self.module_array:
            tmp_answer = await loop.run_in_executor(None, module.process_msg_active, msg, sender);
            if tmp_answer:
                answer_array.append(tmp_answer);
        if answer_array:
            clean = lambda m : m.replace("\n", "<br>");
            for answer in answer_array:
                await self.send_message(clean(answer));
    #
    def add_module(self, module):
        if not(module in self.module_array):
            self.module_array.append(module);
    #
    async def tick(self, delay=1):
        await asyncio.sleep(delay);
        answer_array = [];
        loop = asyncio.get_event_loop();
        for module in self.module_array:
            await loop.run_in_executor(None, module.clock_update);
            tmp_answer = await loop.run_in_executor(None, module.run_on_clock);
            if tmp_answer:
                answer_array.append(tmp_answer);
        if answer_array:
            clean = lambda m : m.replace("\n", "<br>");
            for answer in answer_array:
                await self.send_message(clean(answer));
#
async def main():
    host = "https://mandragot.org";
    login = "@tersa_bot:mandragot.org";
    gaming_room = "#papotage_gaming_unlock:mandragot.org";
    elementBot_inst = elementBot(host, login, gaming_room);
    #
    my_pendu = pendu_bot(); elementBot_inst.add_module(my_pendu);
    my_mastermind = mastermind_bot(); elementBot_inst.add_module(my_mastermind);
    my_quotes = quotes() ; elementBot_inst.add_module(my_quotes)
    #
    await elementBot_inst.connect("XXX");
    await elementBot_inst.start_listening("Hello, I'm Tbot!");


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
