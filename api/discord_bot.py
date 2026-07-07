from __future__ import annotations

import discord
from discord import app_commands
from loguru import logger

from api.constants import CodeStatus, GAME_NAMES, Game
from api.db import db


class CodeButtons(discord.ui.View):
    def __init__(self, code_id: int, code: str, game: str, *, timeout: float = 300):
        super().__init__(timeout=timeout)
        self.code_id = code_id
        self.code = code
        self.game = game

    @discord.ui.button(label="✅ Working", style=discord.ButtonStyle.green)
    async def mark_ok(self, interaction: discord.Interaction, _: discord.ui.Button):
        await db.redeemcode.update(
            where={"id": self.code_id},
            data={"status": CodeStatus.OK},
        )
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            content=f"**{self.code}** marked as ✅ **OK**", view=self
        )
        logger.info(f"Discord: {interaction.user} verified {self.code} for {self.game}")

    @discord.ui.button(label="❌ Expired", style=discord.ButtonStyle.red)
    async def mark_expired(self, interaction: discord.Interaction, _: discord.ui.Button):
        await db.redeemcode.update(
            where={"id": self.code_id},
            data={"status": CodeStatus.NOT_OK},
        )
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            content=f"**{self.code}** marked as ❌ **Expired**", view=self
        )
        logger.info(f"Discord: {interaction.user} expired {self.code} for {self.game}")


class CodeBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self._synced = False

    async def on_ready(self):
        logger.info(f"Discord bot logged in as {self.user}")
        if not self._synced:
            await self.tree.sync()
            self._synced = True
            logger.info("Discord slash commands synced")

    async def setup_hook(self):
        @self.tree.command(name="codes", description="Show redeem codes for a game")
        @app_commands.describe(game="Which game?")
        @app_commands.choices(game=[
            app_commands.Choice(name=GAME_NAMES[slug], value=slug)
            for slug in Game.values()
        ])
        async def codes_cmd(interaction: discord.Interaction, game: str):
            await interaction.response.defer()

            active = await db.redeemcode.find_many(
                where={"game": game, "status": CodeStatus.OK},
                order={"id": "desc"},
            )
            unverified = await db.redeemcode.find_many(
                where={"game": game, "status": CodeStatus.UNVERIFIED},
                order={"id": "desc"},
            )

            name = GAME_NAMES.get(game, game)
            lines = [f"# {name} Codes\n"]

            if active:
                lines.append("## ✅ Working")
                for c in active:
                    lines.append(f"**`{c.code}`** — {c.rewards or 'no info'}")
                lines.append("")

            if unverified:
                lines.append("## ❓ Unverified")
                for c in unverified:
                    lines.append(f"**`{c.code}`** — {c.rewards or 'no info'}")
                lines.append("")

            if not active and not unverified:
                lines.append("No codes found.")

            content = "\n".join(lines)

            view: discord.ui.View | None = None
            if unverified:
                view = CodeButtons(
                    code_id=unverified[0].id,
                    code=unverified[0].code,
                    game=game,
                )

            await interaction.followup.send(content[:2000], view=view)
