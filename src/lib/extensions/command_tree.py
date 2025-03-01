import traceback

import discord
from discord import app_commands

from lib import errors
from translation import _


class CommandTree(app_commands.CommandTree):
    def __init__(self, bot):
        super().__init__(bot)

    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.CommandNotFound):
            await interaction.response.send_message(_(interaction.locale, "errors.command_not_found"), ephemeral=True)
        elif isinstance(error, errors.ModuleDisabled):
            await interaction.response.send_message(error, ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                _(interaction.locale, "errors.bot_missing_permissions", errors=", ".join(error.missing_permissions))
            )
        elif isinstance(error, app_commands.TransformerError):
            await interaction.response.send_message(error, ephemeral=True)
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                _(interaction.locale, "errors.command_on_cooldown", retry_after=round(error.retry_after)),
                ephemeral=True,
            )
        else:
            traceback.print_exc()
