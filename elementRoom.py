import asyncio;
from src.bcolors import bcolors;
import datetime;

class elementRoom(object):
    #
    def __init__(self, client, room_id):
        self.room_id = room_id;
        self.client = client;
        self.real_id = None;
        self.module_set = set();
        self.mailbox = [];
    #
    def add_module(self, module):
        self.module_set.add(module);
    #
    def remove_module(self, module):
        if module in self.module_set:
            self.module_set.remove(module);
    #
    async def connect(self):
        tmp_real_id = await self.client.join(self.room_id);
        self.real_id = tmp_real_id.room_id;
    #
    async def send_message(self, message):
        await self.client.room_send(
            room_id=self.real_id,
            message_type="m.room.message",
            content = {
                "msgtype": "m.text",
                "format": "org.matrix.custom.html",
                "body": message,
                "formatted_body": message
            }
        ) ;
    #
    async def message_cb(self, room, event):
        if (room.room_id == self.real_id):
            tmp_log = "Event from Room " + bcolors.OKGREEN + str(self.room_id) + bcolors.ENDC + \
             " at " + bcolors.OKGREEN + str(datetime.datetime.now())+ bcolors.ENDC + " by "+ bcolors.OKBLUE + event.sender +bcolors.ENDC ;
            print(tmp_log);
            msg = event.body;
            sender = event.sender;
            await self.check_module(msg, sender);
    #
    async def check_module(self, msg, sender):
        answer_array = [];
        loop = asyncio.get_event_loop();
        for module in self.module_set:
            tmp_answer = await loop.run_in_executor(None, module.process_msg_active, msg, sender);
            if tmp_answer:
                answer_array.append(tmp_answer);
        if answer_array:
            clean = lambda m : m.replace("\n", "<br>");
            for answer in answer_array:
                await self.send_message(clean(answer));
    # (Les fonctions se ressemblent beaucoup mais je préfère laisser cela ainsi, les interfaces étant assez différentes).
    async def check_module_on_tick(self):
        answer_array = [];
        loop = asyncio.get_event_loop();
        for module in self.module_set:
            tmp_answer = await loop.run_in_executor(None, module.run_on_clock);
            if tmp_answer:
                answer_array.append(tmp_answer);
        if answer_array:
            clean = lambda m : m.replace("\n", "<br>");
            for answer in answer_array:
                await self.send_message(clean(answer));
    #
    async def check_module_on_start(self):
        answer_array = [];
        loop = asyncio.get_event_loop();
        for module in self.module_set:
            tmp_answer = await loop.run_in_executor(None, module.on_start);
            if tmp_answer:
                answer_array.append(tmp_answer);
        if answer_array:
            clean = lambda m : m.replace("\n", "<br>");
            for answer in answer_array:
                await self.send_message(clean(answer));
