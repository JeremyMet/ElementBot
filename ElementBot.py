#
import asyncio
from nio import (AsyncClient, RoomMessageText)
import datetime;
import json;
#
from src.bcolors import bcolors;
from elementRoom import elementRoom;
#
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.mastermind.mastermind_bot import mastermind_bot ;
from modules.quotes.quotes import quotes ;
#
#######################################
# Vraiment Basique pour le moment ;-) #
#######################################
#
class elementBot(object):
    #
    def __init__(self, host, login):
        self.gaming_id = None;
        self.client = AsyncClient(host, login);
        self.login = login;
        self.module_array = [];
        self.room_set = set();
        # (pour éviter d'écouter les premiers messages).
        self.launch_at = datetime.datetime.now();
        self.toggle = False;
    #
    def add_room(self, room_id):
        room = elementRoom(self.client, room_id);
        self.room_set.add(room);
        return room;
    #
    def remove_room(self, roomObject):
        if (roomObject in self.room_set):
            self.room_set.remove(roomObject);
    #
    async def connect(self, password):
        await self.client.login(password);
        for roomObject in self.room_set:
            await roomObject.connect();
            await roomObject.check_module_on_start();
        self.is_running = True;
        self.client.add_event_callback(self.message_cb, RoomMessageText);
    #
    async def start_listening(self):
        self.launch_at = datetime.datetime.now();
        self.is_running = True ;
        while(self.is_running):
            await asyncio.gather(self.tick(), self.client.sync(timeout=30000));
    #
    async def message_cb(self, room, event):
        # On ignore les messages pendant 2 secondes ...
        if not(self.toggle):
            if ((datetime.datetime.now()-self.launch_at).seconds > 2):
                self.toggle = True;
        if (self.toggle):
            for roomObject in self.room_set:
                await roomObject.message_cb(room, event);
    #
    async def tick(self, delay=1):
        await asyncio.sleep(delay);
        for roomObject in self.room_set:
            await roomObject.check_module_on_tick();

async def main():
    with open("config.json", "r") as f:
        config = json.load(f);
    #
    host = config["host"];
    login = config["login"];
    rooms = config["rooms"];
    password = config["password"];
    print(host, login, rooms, password);
    #
    elementBot_inst = elementBot(host, login);
    room_array = []
    for room in rooms:
        room_array.append(elementBot_inst.add_room(room))
    #
    my_pendu = pendu_bot(); room_array[0].add_module(my_pendu);
    my_mastermind = mastermind_bot(); room_array[0].add_module(my_mastermind);
    my_quote = quotes(); room_array[0].add_module(my_quote);
    #
    await elementBot_inst.connect(password);
    await elementBot_inst.start_listening();


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
