import os
from io import BytesIO
from dotenv import load_dotenv
import discord

from match import Match
import strings as STR

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()
matches = {}
number_emojis = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5, "6️⃣": 6}


class CreatedView(discord.ui.View):

    def __init__(self, channel_id):
        super().__init__()
        self.channel_id = channel_id

    @discord.ui.button(label="Join Game", style=discord.ButtonStyle.primary, emoji="👋")
    async def on_join(self, button, interaction):
        if interaction.user.bot:
            return
        print("Adding player", interaction.user.name)
        if matches[self.channel_id]:
            matches[self.channel_id].append(interaction.user.name)
            self.children[1].disabled = False  # type: ignore
            await self.message.edit(view=self)  # type: ignore
        else:
            matches[self.channel_id] = [interaction.user.name]
        await interaction.response.edit_message(content=f"A game of Cribbage!\nPlayers: {', '.join(matches[self.channel_id])}")
        print(matches[self.channel_id])

    @discord.ui.button(label="Start", style=discord.ButtonStyle.primary, disabled=True, emoji="🏁")
    async def on_start(self, button, interaction):
        players = matches[self.channel_id]
        if len(players) < 2:
            await interaction.response.send_message("Not enough players to start!", ephemeral=True)
        else:
            matches[self.channel_id] = await Match(bot, interaction.channel, players)
            msg = await interaction.response.send_message(STR.GAME_STARTED, view=GetCardsView(matches[self.channel_id]))
            await matches[self.channel_id].begin()


@bot.command(description="Creates a new game of Cribbage.")
async def cribbage(ctx):
    matches[ctx.channel_id] = {}
    await ctx.respond("A game of Cribbage!\nNo one has joined.", view=CreatedView(ctx.channel_id))


class PeggingView(discord.ui.View):
    def __init__(self, match):
        super().__init__()
        self.match = match
        self.currentMessage = None
        for i in range(len(self.children[1:])):
            h = self.match.game.pegging.players[self.match.game.pegging.to_play].pegging_cards
            self.children[i+1].disabled = True  # type: ignore
            if i < len(h):
                if self.match.game.pegging.pegging_count + h[i].value <= 31:
                    self.children[i+1].disabled = False  # type: ignore

    @discord.ui.button(label="Peek Hand", row=0, style=discord.ButtonStyle.primary, emoji="🃏")
    async def on_peek(self, button, interaction):
        await peek_hand(interaction, self.match, pegging=True)

    @discord.ui.button(label="Play", row=1, style=discord.ButtonStyle.grey, emoji="1️⃣")
    async def on_play1(self, button, interaction):
        await play_card(button, self, interaction, self.match, 0)
        await send_pegging_msg(self.match)

    @discord.ui.button(label="Play", row=1, style=discord.ButtonStyle.grey, emoji="2️⃣")
    async def on_play2(self, button, interaction):
        await play_card(button, self, interaction, self.match, 1)
        await send_pegging_msg(self.match)

    @discord.ui.button(label="Play", row=1, style=discord.ButtonStyle.grey, emoji="3️⃣")
    async def on_play3(self, button, interaction):
        await play_card(button, self, interaction, self.match, 2)
        await send_pegging_msg(self.match)

    @discord.ui.button(label="Play", row=1, style=discord.ButtonStyle.grey, emoji="4️⃣")
    async def on_play4(self, button, interaction):
        await play_card(button, self, interaction, self.match, 3)
        await send_pegging_msg(self.match)


class GetCardsView(discord.ui.View):
    def __init__(self, match):
        super().__init__()
        self.match = match
        self.currentMessage = None

    @discord.ui.button(label="Peek Hand", row=0, style=discord.ButtonStyle.primary, emoji="🃏")
    async def on_peek(self, button, interaction):
        await peek_hand(interaction, self.match)

    @discord.ui.button(label="Toss", row=1, style=discord.ButtonStyle.grey, emoji="1️⃣")
    async def on_toss1(self, button, interaction):
        await toss_card(button, self, interaction, self.match, 0)

    @discord.ui.button(label="Toss", row=1, style=discord.ButtonStyle.grey, emoji="2️⃣")
    async def on_toss2(self, button, interaction):
        await toss_card(button, self, interaction, self.match, 1)

    @discord.ui.button(label="Toss", row=1, style=discord.ButtonStyle.grey, emoji="3️⃣")
    async def on_toss3(self, button, interaction):
        await toss_card(button, self, interaction, self.match, 2)

    @discord.ui.button(label="Toss", row=2, style=discord.ButtonStyle.grey, emoji="4️⃣")
    async def on_toss4(self, button, interaction):
        await toss_card(button, self, interaction, self.match, 3)

    @discord.ui.button(label="Toss", row=2, style=discord.ButtonStyle.grey, emoji="5️⃣")
    async def on_toss5(self, button, interaction):
        await toss_card(button, self, interaction, self.match, 4)

    @discord.ui.button(label="Toss", row=2, style=discord.ButtonStyle.grey, emoji="6️⃣")
    async def on_toss6(self, button, interaction):
        await toss_card(button, self, interaction, self.match, 5)


async def peek_hand(interaction, match, tossed=False, pegging=False):
    hand = next(h for h in match.game.hands if h.name == interaction.user.name)
    if not tossed or len(hand.cards) % 2 == 0:
        with BytesIO() as image_binary:
            hand.show_hand(hand.name, pegging=pegging).save(
                image_binary, 'PNG')
            image_binary.seek(0)
            await interaction.response.send_message("Your hand: " + str(hand.pegging_cards if pegging else hand.cards) + ' No one else can see this 🤫', file=discord.File(fp=image_binary, filename=hand.name+'_hand.png'), ephemeral=True)
    else:
        await interaction.response.defer(ephemeral=True)


async def toss_card(button, view, interaction, match, index):
    view.currentMessage = view.currentMessage or view.message.content
    view.currentMessage += '\n > ' + \
        interaction.user.name+' tossed card '+str(index+1)
    await view.message.edit(content=view.currentMessage, view=view)
    r = await match.game.discard(interaction.user.name, index)
    await peek_hand(interaction, match, True)
    if r:
        # discarding finished, start pegging
        await send_pegging_msg(match)


async def send_pegging_msg(match):
    p = match.game.pegging.to_play
    n = match.game.pegging.players[p].name
    count = match.game.pegging.pegging_count
    await match.channel.send(STR.PEGGING + "\n" + str(count) + ' to ' + n, view=PeggingView(match))


async def play_card(button, view, interaction, match, index):
    await match.game.pegging.play_card(interaction.user.name, index)


bot.run(TOKEN)
